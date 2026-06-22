from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_external_adapter_semantic_route,
)
from MAKSIMAR_CORE_LIB.retrieval_backend import build_retrieval_readonly_tool_route

from tools.jarvis_live_runtime.project_workspace_tools import (
    _safe_project_path,
    _tracked_project_files,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def _build_read_only_tool_plan(user_text: str, context: JarvisBrainContext) -> dict[str, Any]:
    lowered = user_text.casefold()
    intent_family = "CONVERSATION"
    selected_tools: tuple[str, ...] = ()
    selected_agent_roles: tuple[str, ...] = ()
    tool_route = None
    confidence = 0.0
    reason = "ordinary conversation"
    needs_ollama = True
    evidence_required = False
    risk_class = "read_only"
    proposal_only = True
    semantic_candidates: tuple[dict[str, Any], ...] = ()

    if _asks_action_request(lowered):
        intent_family = "ACTION_REQUEST"
        selected_tools = ("capability_registry_read", "approval_boundary_read", "operator_proposal")
        confidence = 0.92
        reason = "action verb requires proposal boundary"
        needs_ollama = False
        evidence_required = True
    # RETRIEVAL_SEMANTIC_PRIORITY_GUARD_V2
    # Explicit retrieval/container/project-search questions must be answered by
    # read-only tools before any Ollama free generation.
    if intent_family == "CONVERSATION" and (
        (
            any(token in lowered for token in ("container", "docker", "контейнер"))
            and any(token in lowered for token in ("qdrant", "retrieval", "backend", "runtime", "запуск", "включ"))
        )
        or "qdrant container" in lowered
        or "qdrant контейнер" in lowered
    ):
        intent_family = "CONTAINER_STATUS"
        selected_tools = (
            "retrieval_container_contract",
            "retrieval_runtime_profile",
            "qdrant_container_status",
        )
        confidence = 0.96
        reason = "retrieval container/runtime boundary status question"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and (
        lowered.startswith("найди где ")
        or "найди где " in lowered
        or lowered.startswith("где ")
        or lowered.startswith("find where ")
        or "source_ref" in lowered
        or "evidence_ref" in lowered
    ):
        intent_family = "PROJECT_SEARCH"
        tool_route = build_retrieval_readonly_tool_route(
            "PROJECT_SEARCH",
            ("mgrep_readonly", "repo_search", "read_file_snippet", "read_file_outline"),
            PROJECT_ROOT,
        )
        selected_tools = tool_route.selected_tool_chain
        confidence = 0.94
        reason = "explicit project search request must use read-only retrieval tools"
        needs_ollama = False
        evidence_required = True

    if intent_family == "CONVERSATION" and _asks_tool_catalog_question(lowered):
        intent_family = "TOOL_CATALOG"
        selected_tools = ("build_jarvis_live_tool_catalog_read_model",)
        confidence = 0.95
        reason = "tool/capability catalog question"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _asks_agent_catalog_question(lowered):
        intent_family = "AGENT_CATALOG"
        selected_tools = ("build_jarvis_agent_catalog_read_model",)
        confidence = 0.96
        reason = "grounded agent catalog question"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _asks_skill_visibility_question(lowered):
        intent_family = "SKILL_VISIBILITY"
        selected_tools = ("build_jarvis_skill_visibility_read_model", "build_jarvis_live_tool_catalog_read_model")
        confidence = 0.96
        reason = "grounded skill/capability visibility question"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _asks_activation_matrix_question(lowered):
        intent_family = "ACTIVATION_MATRIX"
        selected_tools = ("build_default_capability_activation_matrix", "runtime_activation_matrix_preview")
        confidence = 0.96
        reason = "capability/readiness/activation matrix question"
        needs_ollama = False
        evidence_required = True
    # EXPLICIT_READ_ONLY_INTENT_PRIORITY_BEGIN
    # Specific read-only intents must be resolved before semantic/project search fallback.
    if intent_family == "CONVERSATION" and _asks_memory_history_question(lowered):
        intent_family = "MEMORY_RECALL"
        selected_tools = (
            "stable_style_profile",
            "session_memory",
            "local_chat_memory",
            "memory_engine_registry",
            "runtime_history_store",
            "history_query",
            "mempalace_read_only_sandbox",
        )
        confidence = 0.9
        reason = "history or memory question must be retrieval-first"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_safety_status_question(lowered):
        intent_family = "SAFETY_STATUS"
        selected_tools = ("repo_search", "DANGEROUS_MEMORY_FLAGS", "project_safety_formatter")
        confidence = 0.88
        reason = "safety/capability boundary question"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_model_status_question(lowered):
        intent_family = "MODEL_STATUS"
        selected_tools = ("model_runtime_status", "ollama_ps", "ollama_tags", "ollama_show")
        confidence = 0.9
        reason = "model/runtime status question"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_roadmap_status_question(lowered):
        intent_family = "ROADMAP_STATUS"
        selected_tools = ("status_tools", "roadmap_post_step_drift_check", "jarvis_live_ci_status", "repo_search")
        confidence = 0.88
        reason = "roadmap/status question"
        needs_ollama = False
        evidence_required = True
    # EXPLICIT_READ_ONLY_INTENT_PRIORITY_END
    # SAFETY_STATUS_PRIORITY_GUARD_V2
    if intent_family == "CONVERSATION" and (
        _asks_safety_status_question(lowered)
        or any(
            marker in lowered
            for marker in (
                "core guard",
                "watchdog",
                "safety",
                "security",
                "approval",
                "execution control",
                "direct_execution_allowed",
                "pc_control_allowed",
            )
        )
    ):
        intent_family = "SAFETY_STATUS"
        selected_tools = ("repo_search", "DANGEROUS_MEMORY_FLAGS", "project_safety_formatter")
        confidence = 0.94
        reason = "explicit safety/capability boundary question"
        needs_ollama = False
        evidence_required = True

    if intent_family == "CONVERSATION" and _has_filename_lookup_guard(user_text):
        intent_family = "PROJECT_FILE"
        selected_tools = ("read_file_snippet", "read_file_outline", "repo_files")
        confidence = 0.96
        reason = "direct filename lookup guard"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _has_backend_status_guard(lowered):
        intent_family = "RETRIEVAL_BACKEND_STATUS"
        tool_route = build_retrieval_readonly_tool_route(
            "RETRIEVAL_BACKEND_STATUS",
            ("qdrant_readonly_status", "retrieval_backend_status_read_model", "retrieval_tool_registry_contract"),
            PROJECT_ROOT,
        )
        selected_tools = tool_route.selected_tool_chain
        confidence = 0.97
        reason = "direct retrieval backend status guard"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _has_semantic_similarity_guard(lowered):
        intent_family = "SEMANTIC_SIMILARITY"
        tool_route = build_retrieval_readonly_tool_route(
            "SEMANTIC_SIMILARITY",
            ("sqlite_vec_readonly", "repo_search", "qdrant_readonly"),
            PROJECT_ROOT,
        )
        selected_tools = tool_route.selected_tool_chain
        confidence = 0.97
        reason = "direct semantic similarity guard"
        needs_ollama = False
        evidence_required = True
    if intent_family == "CONVERSATION" and _extract_requested_file_path(user_text):
        intent_family = "PROJECT_FILE"
        selected_tools = ("read_file_snippet", "read_file_outline")
        confidence = 0.88
        reason = "file content request"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_project_status_question(lowered):
        intent_family = "PROJECT_STATUS"
        selected_tools = ("repo_git_status", "build_project_workspace_read_model")
        confidence = 0.9
        reason = "workspace/git status question"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_project_structure_question(lowered):
        intent_family = "PROJECT_STRUCTURE"
        selected_tools = ("build_project_workspace_read_model", "repo_tree", "repo_files")
        confidence = 0.86
        reason = "project structure question"
        needs_ollama = False
        evidence_required = True
    elif intent_family == "CONVERSATION" and _asks_project_search_question(lowered):
        intent_family = "PROJECT_SEARCH"
        selected_tools = ("repo_search", "read_file_snippet", "read_file_outline")
        confidence = 0.82
        reason = "semantic project search question"
        needs_ollama = False
        evidence_required = True
    external_route = _semantic_external_adapter_route(user_text, context)
    if intent_family == "CONVERSATION" and external_route is not None:
        intent_family = str(external_route["intent_family"])
        selected_tools = tuple(external_route["selected_tools"])
        selected_agent_roles = tuple(external_route["selected_agent_roles"])
        confidence = float(external_route["confidence"])
        reason = str(external_route["reason"])
        needs_ollama = False
        evidence_required = True
        risk_class = str(external_route["risk_class"])
        proposal_only = bool(external_route["proposal_only"])
        semantic_candidates = tuple(external_route["candidate_matches"])

    return {
        "intent_family": intent_family,
        "confidence": confidence,
        "selected_tools": selected_tools,
        "selected_agent_roles": selected_agent_roles,
        "reason": reason,
        "read_only": True,
        "execution_allowed": False,
        "needs_ollama": needs_ollama,
        "evidence_required": evidence_required,
        "evidence_count": 0,
        "risk_class": risk_class,
        "proposal_only": proposal_only,
        "semantic_candidates": semantic_candidates,
        "tool_route": tool_route.to_read_model() if tool_route is not None else {},
    }


def _semantic_external_adapter_route(user_text: str, context: Any) -> dict[str, Any] | None:
    route = build_external_adapter_semantic_route(user_text)
    orchestration_decision = getattr(context, "orchestration_decision", {}) if context is not None else {}
    selected_tools = tuple(orchestration_decision.get("selected_tools", ())) if isinstance(orchestration_decision, dict) else ()
    selected_intent = str(orchestration_decision.get("normalized_intent", "")) if isinstance(orchestration_decision, dict) else ""
    if route["matched"]:
        return route
    if any(str(tool).startswith("external_adapter:") for tool in selected_tools):
        intent_family = "AGENT_ENGINE_COMPARISON" if selected_intent == "agent_engine_comparison" else "EXTERNAL_ADAPTER_SELECTION"
        return {
            "matched": True,
            "intent_family": intent_family,
            "selected_tools": selected_tools,
            "selected_agent_roles": tuple(orchestration_decision.get("selected_agent_roles", ("tool_selector_agent",))),
            "risk_class": "risk_gate",
            "proposal_only": True,
            "execution_allowed": False,
            "confidence": 0.78,
            "reason": "existing orchestration decision selected external adapters",
            "candidate_matches": (),
        }
    return None


def _asks_activation_matrix_question(lowered: str) -> bool:
    if _asks_action_request(lowered):
        return False
    if _asks_memory_history_question(lowered):
        return False
    if _asks_safety_status_question(lowered):
        return False
    if _asks_model_status_question(lowered):
        return False
    if _asks_roadmap_status_question(lowered):
        return False

    activation_markers = (
        "activation matrix",
        "activation",
        "capability",
        "capabilities",
        "readiness",
        "готовность",
        "матрица",
        "матрица активации",
        "активац",
        "возможност",
        "что можешь",
        "что умеешь",
        "windows voice edge",
        "voice edge",
        "push-to-talk",
        "ptt",
        "младш",
        "android junior",
        "ios junior",
        "андроид младш",
        "айос младш",
    )
    return any(marker in lowered for marker in activation_markers)


def _asks_project_status_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "что изменено",
            "что поменялось",
            "какие изменения",
            "dirty files",
            "dirty",
            "untracked",
            "git status",
            "статус git",
            "что в git",
            "что сейчас в проекте поменялось",
        )
    )


def _asks_agent_catalog_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "каких агентов ты видишь",
            "какие агенты доступны",
            "список агентов",
            "каких агентов видишь",
            "какие agent доступны",
            "available agents",
            "agent catalog",
        )
    )


def _asks_skill_visibility_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "какие скилы ты видишь",
            "какие навыки доступны",
            "какие возможности доступны",
            "какие скилы доступны",
            "список навыков",
            "skill visibility",
            "available skills",
        )
    )


def _asks_project_structure_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "структура проекта",
            "структуре проекта",
            "дерево проекта",
            "покажи проект",
            "что ты видишь по проекту",
            "что у нас по ядру",
            "структура ядра",
            "project workspace",
            "project tree",
        )
    )


def _asks_project_search_question(lowered: str) -> bool:
    search_markers = (
        "где",
        "найди",
        "найти",
        "поищи",
        "поиск",
        "что по",
        "что у нас по",
        "где у нас",
        "логика",
        "лежит",
        "подключен",
        "подключено",
        "скачан",
        "установлен",
        "есть доступ",
    )
    domain_markers = (
        "terminal chat",
        "brain_loop",
        "jarvis",
        "n8n",
        "голос",
        "voice",
        "memory",
        "памят",
        "roadmap",
        "роадмап",
        "core guard",
        "watchdog",
        "ollama",
        "qwen",
        "tool",
        "adapter",
        "адаптер",
        "автоматизац",
    )
    return any(marker in lowered for marker in search_markers) and any(
        marker in lowered for marker in domain_markers
    )


def _has_semantic_similarity_guard(lowered: str) -> bool:
    if "semantic similarity" in lowered or "similar to" in lowered or "related to" in lowered:
        return True
    if "семантически" in lowered or "по смыслу" in lowered:
        return True
    return any(
        marker in lowered
        for marker in (
            "найди похожее на",
            "похожее на",
            "похожие на",
            "найди похожее",
            "похожие",
            "похожее",
            "semantic",
        )
    )


def _has_backend_status_guard(lowered: str) -> bool:
    boundary_markers = ("docker", "докер", "container", "контейнер", "порт", "port", "server", "сервер")
    if any(marker in lowered for marker in boundary_markers):
        return False
    backend_markers = ("qdrant", "qdrnt", "qdran", "qudrant", "sqlite", "sqlite-vec", "sqlite_vec", "sqlite vec", "mgrep", "mgreo", "mgreep")
    status_markers = ("status", "статус", "что по", "включен", "включён", "готов", "ready")
    return any(marker in lowered for marker in backend_markers) and any(marker in lowered for marker in status_markers)


def _has_filename_lookup_guard(user_text: str) -> bool:
    return bool(_extract_filename_token(user_text))


def _extract_filename_token(user_text: str) -> str:
    match = re.search(r"(?P<filename>[\w.\-]+(?:\.py|\.yaml|\.yml|\.md|\.json|\.toml))", user_text, flags=re.IGNORECASE)
    return match.group("filename") if match else ""


def _asks_memory_history_question(lowered: str) -> bool:
    explicit_memory_markers = (
        "что мы обсуждали",
        "что обсуждали",
        "что я говорил",
        "что я просил",
        "что было в переписке",
        "что было в истории",
        "история сообщений",
        "история чата",
        "покажи историю",
        "найди в истории",
        "вспомни",
        "помнишь",
        "что ты помнишь",
        "из памяти",
        "в памяти",
        "по памяти",
        "memory recall",
        "history recall",
        "conversation history",
    )

    project_history_markers = (
        "project history",
        "project_history",
        "imported project history",
        "imported gpt project history",
        "gpt project history",
        "history по проекту",
        "project history по проекту",
        "история проекта",
        "истории проекта",
        "историю проекта",
        "история по проекту",
        "истории по проекту",
        "историю по проекту",
        "переписке по проекту",
        "переписка по проекту",
    )

    # Важно: простое упоминание GPT не является запросом к памяти.
    # Но явные формулировки "project history / история проекта" обязаны
    # идти retrieval-first и не должны падать в free Ollama.
    if any(marker in lowered for marker in project_history_markers):
        return True

    return any(marker in lowered for marker in explicit_memory_markers)


def _asks_model_status_question(lowered: str) -> bool:
    return any(marker in lowered for marker in ("модел", "ollama", "qwen", "gpu", "загружено")) and any(
        marker in lowered
        for marker in (
            "какие",
            "что по",
            "статус",
            "подключ",
            "отвечает",
            "есть",
            "видишь",
            "runtime",
        )
    )


def _asks_roadmap_status_question(lowered: str) -> bool:
    return any(marker in lowered for marker in ("roadmap", "роадмап", "фаза", "batch", "батч")) and any(
        marker in lowered for marker in ("что дальше", "следующ", "сейчас", "статус", "какая", "какой")
    )


def _asks_action_request(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "сделай коммит",
            "commit",
            "git commit",
            "запусти тест",
            "запусти pytest",
            "удали файл",
            "скачай",
            "установи",
            "install",
            "download",
            "запусти n8n",
            "настрой n8n",
            "управляй пк",
            "выполни команду",
            "запусти команду",
        )
    )


def _asks_tool_catalog_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "какие tools",
            "какие tool",
            "какие инструменты",
            "какие инструменты тебе доступны",
            "какие tools тебе доступны",
            "что ты умеешь",
            "что ты можешь",
            "какие capability",
            "capabilities",
            "tool catalog",
            "available tools",
            "tool-каталог",
            "покажи доступные tools",
            "список инструментов",
            "все tools",
            "все инструменты",
            "подключенные tools",
            "подключенные инструменты",
        )
    )


def _extract_requested_file_path(user_text: str) -> str:
    lowered = user_text.casefold()
    filename = _extract_filename_token(user_text)
    if filename:
        for path in _tracked_project_files():
            if Path(path).name.casefold() == filename.casefold():
                return path
        if _safe_project_path(filename):
            return filename
    if not any(marker in lowered for marker in ("покажи файл", "что внутри", "открой файл", "read file", "file ")):
        return ""
    for token in user_text.replace("`", " ").replace("'", " ").replace('"', " ").split():
        candidate = token.strip(" ,.;:()[]{}")
        if "/" in candidate or candidate.endswith((".py", ".md", ".yaml", ".yml", ".json", ".txt", ".sh")):
            if _safe_project_path(candidate):
                return candidate
    return ""


def _asks_safety_status_question(lowered: str) -> bool:
    """Detect explicit safety/security/governance status questions.

    This guard must be broad enough to catch mixed Russian/English operator questions
    like "что у нас по core guard watchdog safety?" before generic semantic search.
    """
    return any(
        marker in lowered
        for marker in (
            "core guard",
            "watchdog",
            "safety",
            "security",
            "approval",
            "execution control",
            "policy",
            "guard",
            "защит",
            "безопасн",
            "апрув",
            "разрешен",
            "разрешён",
            "контроль действий",
            "контроль выполнения",
            "ядро безопасности",
            "security_layer",
            "approval_service",
            "execution_allowed",
            "direct_execution_allowed",
            "pc_control_allowed",
        )
    )
