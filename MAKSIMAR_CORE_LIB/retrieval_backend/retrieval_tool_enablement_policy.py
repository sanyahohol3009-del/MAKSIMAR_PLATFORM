from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_vendor_gate_contract import (
    RetrievalVendorGateContract,
    build_retrieval_vendor_gate_contract,
)


RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID = "retrieval_tool_enablement_policy_v1"
SEMANTIC_INTENT_GROUPS: tuple[str, ...] = (
    "project_delta",
    "file_lookup",
    "project_code_search",
    "memory_history",
    "semantic_similarity",
    "backend_status",
    "roadmap_readiness",
    "test_validation",
    "source_evidence_audit",
    "architecture_docs",
    "vendor_quarantine",
    "container_runtime_boundary",
    "autonomous_read_only_tool_use",
)
TYPO_ALIAS_MAP: dict[str, str] = {
    "mgreo": "mgrep",
    "mgreep": "mgrep",
    "grep search": "mgrep search",
    "aqlite": "sqlite",
    "aqlite vec": "sqlite vec",
    "aqlite-vec": "sqlite vec",
    "sqlite-vec": "sqlite vec",
    "sqlite_vec": "sqlite vec",
    "sqllite": "sqlite",
    "qdran": "qdrant",
    "qdrnt": "qdrant",
    "qudrant": "qdrant",
    "retrival": "retrieval",
    "evidense": "evidence",
    "source-ref": "source_ref",
    "source ref": "source_ref",
    "докер": "docker",
    "контейнер": "container",
    "джарвис": "jarvis",
}
INTENT_MATCH_STOPWORDS: frozenset[str] = frozenset(
    {
        "and",
        "или",
        "есть",
        "где",
        "как",
        "какие",
        "какой",
        "ли",
        "либо",
        "лишь",
        "можно",
        "нас",
        "по",
        "что",
        "это",
    }
)


@dataclass(frozen=True, slots=True)
class RetrievalSemanticIntentRule:
    intent_group: str
    route_key: str
    read_only_tools: tuple[str, ...]
    phrases: tuple[str, ...]

    def __post_init__(self) -> None:
        intent_group = _require_text(self.intent_group, "intent_group")
        route_key = _require_text(self.route_key, "route_key")
        if intent_group not in SEMANTIC_INTENT_GROUPS:
            raise ValueError(f"unsupported intent_group: {intent_group}")
        if not isinstance(self.read_only_tools, tuple) or not self.read_only_tools:
            raise ValueError("read_only_tools must be a non-empty tuple")
        if not isinstance(self.phrases, tuple) or not self.phrases:
            raise ValueError("phrases must be a non-empty tuple")
        normalized_tools = tuple(_require_text(tool, "read_only_tools") for tool in self.read_only_tools)
        normalized_phrases = tuple(_normalize_intent_text(_require_text(phrase, "phrases")) for phrase in self.phrases)
        if len(set(normalized_phrases)) != len(normalized_phrases):
            raise ValueError(f"phrases must not contain duplicates for {intent_group}")
        object.__setattr__(self, "intent_group", intent_group)
        object.__setattr__(self, "route_key", route_key)
        object.__setattr__(self, "read_only_tools", normalized_tools)
        object.__setattr__(self, "phrases", normalized_phrases)

    def match_score(self, normalized_text: str) -> int:
        score = 0
        text_tokens = set(normalized_text.split())
        for phrase in self.phrases:
            if phrase in normalized_text:
                score = max(score, 100 + len(phrase.split()))
                continue
            phrase_tokens = tuple(
                token for token in phrase.split() if len(token) > 2 and token not in INTENT_MATCH_STOPWORDS
            )
            if phrase_tokens and set(phrase_tokens).issubset(text_tokens):
                score = max(score, 70 + len(phrase_tokens))
            elif phrase_tokens:
                overlap = sum(1 for token in phrase_tokens if token in text_tokens)
                if overlap >= max(2, (len(phrase_tokens) + 1) // 2):
                    score = max(score, 40 + overlap)
        return score

    def to_read_model(self) -> dict[str, object]:
        return {
            "intent_group": self.intent_group,
            "route_key": self.route_key,
            "read_only_tools": self.read_only_tools,
            "phrases": self.phrases,
        }


@dataclass(frozen=True, slots=True)
class RetrievalSemanticIntentClassification:
    normalized_text: str
    intent_group: str
    route_key: str
    read_only_tools: tuple[str, ...]
    score: int
    matched: bool
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    read_only: bool = True
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        normalized_text = _require_text(self.normalized_text, "normalized_text")
        intent_group = _require_text(self.intent_group, "intent_group")
        route_key = _require_text(self.route_key, "route_key")
        if intent_group != "conversation" and intent_group not in SEMANTIC_INTENT_GROUPS:
            raise ValueError(f"unsupported intent_group: {intent_group}")
        if not isinstance(self.read_only_tools, tuple):
            raise TypeError("read_only_tools must be a tuple")
        for field_name in (
            "matched",
            "source_ref_required",
            "evidence_binding_required",
            "read_only",
            "direct_execution_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)
        if self.score < 0:
            raise ValueError("score must be non-negative")
        if self.matched and not self.read_only_tools:
            raise ValueError("matched classification must include read_only_tools")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        object.__setattr__(self, "normalized_text", normalized_text)
        object.__setattr__(self, "intent_group", intent_group)
        object.__setattr__(self, "route_key", route_key)

    def to_read_model(self) -> dict[str, object]:
        return {
            "normalized_text": self.normalized_text,
            "intent_group": self.intent_group,
            "route_key": self.route_key,
            "read_only_tools": self.read_only_tools,
            "score": self.score,
            "matched": self.matched,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "read_only": self.read_only,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


def _normalize_intent_text(text: str) -> str:
    normalized = text.casefold().replace("_", " ").replace("-", " ")
    for alias, canonical in sorted(TYPO_ALIAS_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        alias_pattern = re.escape(alias.casefold().replace("_", " ").replace("-", " "))
        normalized = re.sub(
            rf"(?<![0-9a-zа-яё]){alias_pattern}(?![0-9a-zа-яё])",
            canonical,
            normalized,
        )
    normalized = re.sub(r"[^0-9a-zа-яё]+", " ", normalized)
    return " ".join(normalized.split())


def _rule(
    intent_group: str,
    route_key: str,
    read_only_tools: tuple[str, ...],
    phrases: tuple[str, ...],
) -> RetrievalSemanticIntentRule:
    return RetrievalSemanticIntentRule(
        intent_group=intent_group,
        route_key=route_key,
        read_only_tools=read_only_tools,
        phrases=phrases,
    )


def build_retrieval_semantic_intent_rules() -> tuple[RetrievalSemanticIntentRule, ...]:
    return (
        _rule(
            "project_delta",
            "PROJECT_STATUS",
            ("repo_git_status", "build_project_workspace_read_model"),
            (
                "что изменено",
                "что изменилось после",
                "что поменялось",
                "что мы только что сделали",
                "что добавилось",
                "что было изменено в последнем батче",
                "какие файлы изменились",
                "покажи изменения",
                "покажи последние правки",
                "что кодекс поменял",
                "что сделал кодекс",
                "какие новые файлы",
                "какие файлы модифицированы",
                "что в git status",
                "что в diff",
                "что не закоммичено",
                "что осталось грязным",
                "unrelated dirty files",
                "что висит в untracked",
                "проверь рабочее дерево",
                "проверь текущую ветку",
                "show current delta",
                "what changed",
                "latest changes",
                "current git status",
            ),
        ),
        _rule(
            "file_lookup",
            "PROJECT_STRUCTURE",
            ("repo_tree", "repo_files", "repo_search"),
            (
                "где файл",
                "где лежит файл",
                "найди файл",
                "найди путь",
                "где этот контракт",
                "где тест",
                "где документ",
                "где acceptance doc",
                "где preview tool",
                "где roadmap registry",
                "где находится qdrant contract",
                "где находится sqlite vec contract",
                "где находится mgrep adapter",
                "покажи путь к файлу",
                "найди файл по названию",
                "найди все retrieval файлы",
                "найди все tests по retrieval",
                "найди все container yaml",
                "найди все runtime profile",
                "покажи дерево папки",
                "покажи структуру retrieval_backend",
                "repo tree",
                "where is file",
                "find file",
                "locate contract",
                "find tests",
            ),
        ),
        _rule(
            "project_code_search",
            "PROJECT_SEARCH",
            ("mgrep_readonly", "repo_search", "read_file_snippet", "read_file_outline"),
            (
                "найди по проекту",
                "поиск по проекту",
                "найди в коде",
                "найди строку",
                "найди функцию",
                "найди класс",
                "найди dataclass",
                "найди import",
                "найди где используется",
                "найди где source_ref",
                "найди все упоминания",
                "найди source_of_truth",
                "найди evidence_binding_required",
                "найди network_allowed_by_default",
                "найди runtime_mutation_allowed",
                "найди direct_execution_allowed",
                "найди qdrant_server_required_now",
                "найди docker_required_now",
                "найди vendor_gate_required",
                "проверь где есть TODO",
                "проверь где есть pass",
                "проверь где есть NotImplemented",
                "проверь где есть subprocess",
                "проверь где есть requests httpx socket",
                "проверь где есть docker qdrant n8n",
                "find references",
                "find usage",
                "search project",
                "search codebase",
                "grep project",
                "code search",
            ),
        ),
        _rule(
            "memory_history",
            "MEMORY_RECALL",
            ("session_memory", "local_chat_memory", "history_query", "memory_engine_registry"),
            (
                "что мы обсуждали",
                "что мы решили",
                "что было в памяти",
                "найди в памяти",
                "найди в истории",
                "найди в переписке",
                "что мы говорили про qdrant",
                "что мы говорили про sqlite vec",
                "что мы говорили про mgrep",
                "что мы говорили про n8n",
                "что мы решили по docker",
                "что мы решили по контейнерам",
                "что мы решили по source of truth",
                "что мы решили по evidence binding",
                "что было в прошлом чате",
                "найди прошлое решение",
                "найди архитектурное правило",
                "восстанови контекст",
                "recall project memory",
                "search memory",
                "search history",
                "previous decision",
                "architecture decision",
            ),
        ),
        _rule(
            "semantic_similarity",
            "SEMANTIC_SIMILARITY",
            ("sqlite_vec_readonly", "repo_search", "qdrant_readonly"),
            (
                "найди похожее",
                "найди похожий файл",
                "найди похожий контракт",
                "найди похожий тест",
                "найди похожую логику",
                "найди дубликат",
                "проверь семантический дубль",
                "похоже ли это на уже существующее",
                "есть ли уже такой adapter",
                "есть ли уже такой contract",
                "не создаём ли мы дубль",
                "куда это лучше встроить",
                "create or extend",
                "extend or create",
                "semantic duplicate risk",
                "duplicate risk",
                "semantic search",
                "duplicate check",
                "related files",
                "similar contract",
            ),
        ),
        _rule(
            "backend_status",
            "RETRIEVAL_BACKEND_STATUS",
            (
                "qdrant_readonly_status",
                "retrieval_backend_status_read_model",
                "retrieval_backend_status_preview",
                "retrieval_tool_registry_contract",
            ),
            (
                "что по qdrant",
                "что по sqlite",
                "что по sqlite vec",
                "что по mgrep",
                "статус qdrant",
                "статус sqlite vec",
                "статус mgrep",
                "qdrant включен",
                "sqlite включен",
                "mgrep включен",
                "retrieval backend status",
                "какие retrieval tools доступны",
                "какие backend включены",
                "какие backend отключены",
                "можно ли запускать qdrant",
                "можно ли запускать docker",
                "можно ли запускать sqlite db",
                "можно ли запускать mgrep binary",
                "vendor gate пройден",
                "source verified",
                "manifest ready",
                "tools enabled",
                "jarvis может ими пользоваться",
                "backend status",
                "qdrant status",
                "sqlite vec status",
                "mgrep status",
            ),
        ),
        _rule(
            "roadmap_readiness",
            "ROADMAP_STATUS",
            ("status_tools", "project_file_readiness_map", "roadmap_post_step_drift_check"),
            (
                "какой следующий батч",
                "что дальше",
                "где мы в roadmap",
                "какой phase сейчас",
                "какой batch сейчас",
                "7.1 закрыт",
                "7.2 закрыт",
                "7.3 закрыт",
                "7.4 закрыт",
                "phase 7 закрыта",
                "readiness status",
                "batch status",
                "project_file_readiness",
                "roadmap drift",
                "post-step drift",
                "какие expected files",
                "что missing",
                "что ready",
                "roadmap status",
                "next batch",
                "phase status",
            ),
        ),
        _rule(
            "test_validation",
            "TEST_STATUS",
            ("status_tools", "jarvis_live_ci_status", "roadmap_post_step_drift_check"),
            (
                "какие тесты запускались",
                "что прошло",
                "сколько passed",
                "есть ли failed",
                "drift зеленый",
                "py_compile прошел",
                "diff check прошел",
                "readiness прошел",
                "какие warnings",
                "какой exit code",
                "покажи последний результат тестов",
                "validate batch",
                "test status",
                "pytest status",
                "ci status",
                "checks result",
            ),
        ),
        _rule(
            "source_evidence_audit",
            "SOURCE_EVIDENCE",
            ("repo_search", "read_file_snippet", "evidence_binding_contract"),
            (
                "на чем основан ответ",
                "покажи источник",
                "покажи evidence",
                "откуда ты это взял",
                "где proof",
                "где trace",
                "покажи source_ref",
                "покажи evidence_id",
                "покажи audit",
                "покажи acceptance proof",
                "чем подтверждено",
                "где документировано",
                "show evidence",
                "cite source",
                "source_ref",
                "audit proof",
                "trace id",
            ),
        ),
        _rule(
            "architecture_docs",
            "DOCS_CONTRACTS",
            ("repo_search", "read_file_snippet", "repo_files"),
            (
                "покажи архитектуру",
                "где architecture doc",
                "где acceptance",
                "где contract",
                "где policy",
                "где gate",
                "где read model",
                "где preview",
                "где container contract",
                "где runtime profile",
                "что написано в документе",
                "объясни contract",
                "объясни policy gate",
                "объясни read model",
                "contract docs",
                "policy docs",
                "architecture docs",
            ),
        ),
        _rule(
            "vendor_quarantine",
            "VENDOR_STATUS",
            ("retrieval_vendor_gate_contract", "retrieval_backend_manifest", "repo_search"),
            (
                "скачан ли n8n",
                "где quarantine",
                "что в vendor quarantine",
                "можно ли скачать mgrep",
                "можно ли скачать sqlite vec",
                "можно ли скачать qdrant",
                "license checked",
                "vendor gate passed",
                "scan passed",
                "можно ли install",
                "можно ли commit external code",
                "что в manifest",
                "внешний код безопасен",
                "vendor acquisition status",
                "quarantine status",
                "external backend status",
            ),
        ),
        _rule(
            "container_runtime_boundary",
            "CONTAINER_STATUS",
            ("container_contract.yaml", "runtime_profile.yaml", "retrieval_backend_status_read_model"),
            (
                "готово к контейнерам",
                "container ready",
                "docker нужен",
                "docker можно запускать",
                "runtime включен",
                "qdrant container включен",
                "network разрешен",
                "ports открыты",
                "service enabled",
                "runtime profile status",
                "container contract status",
                "можно ли поднимать сервис",
                "можно ли открывать порт",
                "можно ли запускать сервер",
                "network boundary",
                "container readiness",
                "runtime boundary",
            ),
        ),
        _rule(
            "autonomous_read_only_tool_use",
            "AUTO_TOOL_USE",
            ("semantic_intent_classifier", "read_only_tool_router", "repo_search"),
            (
                "сам найди",
                "сам проверь",
                "сам посмотри по проекту",
                "сам найди в памяти",
                "сам выбери инструмент",
                "не заставляй меня помнить команды",
                "проверь без команды",
                "разберись что нужно вызвать",
                "используй tools",
                "используй retrieval",
                "используй поиск",
                "используй память",
                "найди доказательства",
                "сначала проверь источники",
                "не гадай",
                "не галлюцинируй",
                "answer grounded",
                "use tools automatically",
                "choose tool automatically",
            ),
        ),
    )


def classify_retrieval_semantic_intent(text: str) -> RetrievalSemanticIntentClassification:
    normalized_text = _normalize_intent_text(_require_text(text, "text"))
    best_rule: RetrievalSemanticIntentRule | None = None
    best_score = 0
    for rule in build_retrieval_semantic_intent_rules():
        score = rule.match_score(normalized_text)
        if score > best_score:
            best_rule = rule
            best_score = score
    if best_rule is None or best_score < 42:
        return RetrievalSemanticIntentClassification(
            normalized_text=normalized_text,
            intent_group="conversation",
            route_key="CONVERSATION",
            read_only_tools=(),
            score=best_score,
            matched=False,
        )
    return RetrievalSemanticIntentClassification(
        normalized_text=normalized_text,
        intent_group=best_rule.intent_group,
        route_key=best_rule.route_key,
        read_only_tools=best_rule.read_only_tools,
        score=best_score,
        matched=True,
    )


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalToolEnablementPolicy:
    policy_id: str
    vendor_gate: RetrievalVendorGateContract
    semantic_intent_groups: tuple[str, ...] = SEMANTIC_INTENT_GROUPS
    semantic_intent_rules: tuple[RetrievalSemanticIntentRule, ...] = ()
    read_only_tool_contracts_allowed: bool = True
    read_only_tool_routing_enabled: bool = True
    auto_routing_readonly_enabled: bool = True
    backend_runtime_enabled: bool = False
    runtime_tool_execution_enabled: bool = False
    auto_routing_contract_allowed: bool = True
    auto_routing_runtime_enabled: bool = False
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    output_requires_normalization: bool = True
    source_of_truth: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        policy_id = _require_text(self.policy_id, "policy_id")
        if not isinstance(self.vendor_gate, RetrievalVendorGateContract):
            raise TypeError("vendor_gate must be RetrievalVendorGateContract")
        if not isinstance(self.semantic_intent_groups, tuple):
            raise TypeError("semantic_intent_groups must be a tuple")
        if self.semantic_intent_groups != SEMANTIC_INTENT_GROUPS:
            raise ValueError("semantic_intent_groups must match canonical RTE groups")
        semantic_intent_rules = self.semantic_intent_rules or build_retrieval_semantic_intent_rules()
        if not isinstance(semantic_intent_rules, tuple):
            raise TypeError("semantic_intent_rules must be a tuple")
        if len(semantic_intent_rules) != len(SEMANTIC_INTENT_GROUPS):
            raise ValueError("semantic_intent_rules must cover every canonical RTE group")
        if tuple(rule.intent_group for rule in semantic_intent_rules) != SEMANTIC_INTENT_GROUPS:
            raise ValueError("semantic_intent_rules must be ordered by canonical RTE groups")

        for field_name in (
            "read_only_tool_contracts_allowed",
            "read_only_tool_routing_enabled",
            "auto_routing_readonly_enabled",
            "backend_runtime_enabled",
            "runtime_tool_execution_enabled",
            "auto_routing_contract_allowed",
            "auto_routing_runtime_enabled",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "pc_control_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)

        for field_name in (
            "read_only_tool_contracts_allowed",
            "read_only_tool_routing_enabled",
            "auto_routing_readonly_enabled",
            "auto_routing_contract_allowed",
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "runtime_tool_execution_enabled",
            "backend_runtime_enabled",
            "auto_routing_runtime_enabled",
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "pc_control_allowed",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")
        if self.vendor_gate.runtime_enabled:
            raise ValueError("vendor gate runtime must remain disabled")

        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "semantic_intent_rules", semantic_intent_rules)

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "semantic_intent_groups": self.semantic_intent_groups,
            "semantic_intent_rules": tuple(rule.to_read_model() for rule in self.semantic_intent_rules),
            "read_only_tool_contracts_allowed": self.read_only_tool_contracts_allowed,
            "read_only_tool_routing_enabled": self.read_only_tool_routing_enabled,
            "auto_routing_readonly_enabled": self.auto_routing_readonly_enabled,
            "backend_runtime_enabled": self.backend_runtime_enabled,
            "runtime_tool_execution_enabled": self.runtime_tool_execution_enabled,
            "auto_routing_contract_allowed": self.auto_routing_contract_allowed,
            "auto_routing_runtime_enabled": self.auto_routing_runtime_enabled,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "output_requires_normalization": self.output_requires_normalization,
            "source_of_truth": self.source_of_truth,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "pc_control_allowed": self.pc_control_allowed,
            "vendor_gate": self.vendor_gate.to_read_model(),
        }


def build_retrieval_tool_enablement_policy() -> RetrievalToolEnablementPolicy:
    return RetrievalToolEnablementPolicy(
        policy_id=RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID,
        vendor_gate=build_retrieval_vendor_gate_contract(),
    )


__all__ = [
    "RETRIEVAL_TOOL_ENABLEMENT_POLICY_ID",
    "SEMANTIC_INTENT_GROUPS",
    "TYPO_ALIAS_MAP",
    "RetrievalSemanticIntentClassification",
    "RetrievalSemanticIntentRule",
    "RetrievalToolEnablementPolicy",
    "build_retrieval_semantic_intent_rules",
    "build_retrieval_tool_enablement_policy",
    "classify_retrieval_semantic_intent",
]
