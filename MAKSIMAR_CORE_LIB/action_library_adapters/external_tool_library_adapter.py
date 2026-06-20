from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    UniversalToolManifest,
    build_universal_tool_manifest,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_registry import (
    UniversalToolRegistry,
    build_universal_tool_registry,
)


_MANIFEST_ROOT = Path("EXTERNAL_BACKENDS/agent_tooling/manifests")
_LEGACY_AUTOGEN_TOOL_ID = "external_adapter:autogen"
_PREFERRED_AUTOGEN_TOOL_IDS = (
    "external_adapter:autogen_agentchat",
    "external_adapter:autogen_ext",
)
_PREFERRED_EXTERNAL_ADAPTER_ORDER = (
    "external_adapter:openai_agents_sdk",
    "external_adapter:mcp_python_sdk",
    "external_adapter:autogen_agentchat",
    "external_adapter:autogen_ext",
    "external_adapter:langgraph",
    _LEGACY_AUTOGEN_TOOL_ID,
)
_SEMANTIC_TOKEN_RE = re.compile(r"[a-z0-9_]+|[а-яё0-9_]+", flags=re.IGNORECASE)
_SEMANTIC_STOP_TOKENS = {
    "и",
    "в",
    "на",
    "для",
    "или",
    "the",
    "a",
    "an",
    "to",
    "with",
    "sdk",
}
_COMPARISON_HINTS = (
    "compare",
    "comparison",
    "сравни",
    "сравнение",
    "vs",
    "versus",
    "difference",
    "отлич",
)
_DIRECT_WORKFLOW_HINTS = (
    "workflow",
    "workflow",
    "orchestrat",
    "graph",
    "граф",
)
_AGENT_HINTS = (
    "agent",
    "agents",
    "агент",
    "агентов",
    "агентн",
)
_CHAIN_HINTS = (
    "цепоч",
    "последователь",
)
_TOOL_HINTS = (
    "tool",
    "tools",
    "tooling",
    "instrument",
    "инструмент",
    "инструментов",
    "protocol",
    "протокол",
    "adapter",
    "адаптер",
    "sdk",
)


@dataclass(frozen=True, slots=True)
class ExternalAdapterSemanticCandidate:
    tool_id: str
    score: float
    reason: str
    selection_enabled: bool
    availability_status: str
    provider_kind: str
    risk_class: str

    def to_read_model(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "score": self.score,
            "reason": self.reason,
            "selection_enabled": self.selection_enabled,
            "availability_status": self.availability_status,
            "provider_kind": self.provider_kind,
            "risk_class": self.risk_class,
        }


@dataclass(frozen=True, slots=True)
class ExternalToolAdapterStatus:
    tool_id: str
    source_library: str
    capability_id: str
    adapter_mode: str
    provider_kind: str
    installed: bool
    activation_blocked_reason: str
    import_probe_worked: bool
    requires_verified_owner: bool
    safe_direct_allowed: bool
    risk_gate_required: bool
    visible_to_jarvis: bool
    not_canonical_truth: bool
    availability_status: str
    selection_enabled: bool
    legacy_alias: bool
    runtime_python: str
    runtime_package_name: str
    runtime_import_name: str
    runtime_version_if_available: str
    runtime_errors: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "source_library": self.source_library,
            "capability_id": self.capability_id,
            "adapter_mode": self.adapter_mode,
            "provider_kind": self.provider_kind,
            "installed": self.installed,
            "activation_blocked_reason": self.activation_blocked_reason,
            "import_probe_worked": self.import_probe_worked,
            "requires_verified_owner": self.requires_verified_owner,
            "safe_direct_allowed": self.safe_direct_allowed,
            "risk_gate_required": self.risk_gate_required,
            "visible_to_jarvis": self.visible_to_jarvis,
            "not_canonical_truth": self.not_canonical_truth,
            "availability_status": self.availability_status,
            "selection_enabled": self.selection_enabled,
            "legacy_alias": self.legacy_alias,
            "runtime_python": self.runtime_python,
            "runtime_package_name": self.runtime_package_name,
            "runtime_import_name": self.runtime_import_name,
            "runtime_version_if_available": self.runtime_version_if_available,
            "runtime_errors": self.runtime_errors,
        }


def _manifest_paths() -> tuple[Path, ...]:
    return tuple(sorted(_MANIFEST_ROOT.glob("*_manifest.json")))


def load_external_tool_manifests() -> tuple[UniversalToolManifest, ...]:
    manifests: list[UniversalToolManifest] = []
    for path in _manifest_paths():
        payload = json.loads(path.read_text(encoding="utf-8"))
        manifests.append(build_universal_tool_manifest(payload))
    return tuple(manifests)


def build_external_tool_registry() -> UniversalToolRegistry:
    return build_universal_tool_registry(load_external_tool_manifests())


def _semantic_tokens(text: str) -> tuple[str, ...]:
    lowered = str(text or "").casefold()
    tokens = []
    for token in _SEMANTIC_TOKEN_RE.findall(lowered):
        token = token.strip("_- ")
        if len(token) <= 1 or token in _SEMANTIC_STOP_TOKENS:
            continue
        tokens.append(token)
        if token.startswith("агент"):
            tokens.append("agent")
        if token.startswith("инстру"):
            tokens.append("tool")
        if token.startswith("протокол"):
            tokens.append("protocol")
        if token.startswith("граф"):
            tokens.append("graph")
        if token.startswith("срав"):
            tokens.append("compare")
    return tuple(dict.fromkeys(tokens))


def _tool_specific_semantic_hints(manifest: UniversalToolManifest) -> tuple[str, ...]:
    hints_by_tool_id = {
        "external_adapter:openai_agents_sdk": (
            "openai agents",
            "agents sdk",
            "agent orchestration",
            "агент оркестрация",
            "agent chain",
        ),
        "external_adapter:mcp_python_sdk": (
            "model context protocol",
            "tool protocol",
            "protocol tools",
            "протокол инструментов",
            "внешний инструмент",
        ),
        "external_adapter:autogen_agentchat": (
            "autogen workflow",
            "multi agent",
            "мультиагент",
            "agentchat",
            "agent conversation",
        ),
        "external_adapter:autogen_ext": (
            "autogen tool runtime",
            "tool extension",
            "расширение инструментов",
            "tool provider",
        ),
        "external_adapter:langgraph": (
            "graph workflow",
            "state graph",
            "графовый workflow",
            "graph agent",
        ),
        _LEGACY_AUTOGEN_TOOL_ID: (
            "legacy autogen",
            "pyautogen",
            "старый autogen",
        ),
    }
    return hints_by_tool_id.get(manifest.tool_id, ())


def _semantic_texts_for_manifest(manifest: UniversalToolManifest) -> tuple[str, ...]:
    metadata_hints = manifest.metadata.get("semantic_hints", ()) if isinstance(manifest.metadata, dict) else ()
    if isinstance(metadata_hints, str):
        metadata_hints = (metadata_hints,)
    return (
        manifest.tool_id,
        manifest.source_library,
        manifest.capability_id,
        manifest.description,
        manifest.semantic_fingerprint,
        manifest.module_import_name,
        manifest.package_name,
        *manifest.aliases,
        *_tool_specific_semantic_hints(manifest),
        *(str(item) for item in metadata_hints if str(item).strip()),
    )


def _manifest_token_index(manifest: UniversalToolManifest) -> tuple[str, ...]:
    tokens: list[str] = []
    for text in _semantic_texts_for_manifest(manifest):
        tokens.extend(_semantic_tokens(text))
    return tuple(dict.fromkeys(tokens))


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    lowered = str(text or "").casefold()
    return any(hint.casefold() in lowered for hint in hints)


def _comparison_requested(text: str, tokens: tuple[str, ...]) -> bool:
    return "compare" in tokens or _contains_any(text, _COMPARISON_HINTS)


def _agent_requested(text: str, tokens: tuple[str, ...]) -> bool:
    return "agent" in tokens or _contains_any(text, _AGENT_HINTS)


def _chain_requested(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token.startswith("цепоч") or token.startswith("последователь") for token in tokens) or _contains_any(
        text,
        _CHAIN_HINTS,
    )


def _workflow_requested(text: str, tokens: tuple[str, ...]) -> bool:
    return (
        "workflow" in tokens
        or _contains_any(text, _DIRECT_WORKFLOW_HINTS)
        or (_agent_requested(text, tokens) and _chain_requested(text, tokens))
    )


def _tooling_requested(text: str, tokens: tuple[str, ...]) -> bool:
    return "tool" in tokens or "protocol" in tokens or _contains_any(text, _TOOL_HINTS)


def _score_manifest_for_request(
    user_text: str,
    request_tokens: tuple[str, ...],
    manifest: UniversalToolManifest,
    status: ExternalToolAdapterStatus,
) -> tuple[float, list[str]]:
    lowered = str(user_text or "").casefold()
    reasons: list[str] = []
    score = 0.0
    manifest_tokens = set(_manifest_token_index(manifest))

    matched_aliases = [alias for alias in manifest.aliases if alias.casefold() in lowered]
    if matched_aliases:
        score += 7.5 + (len(matched_aliases) - 1) * 1.5
        reasons.append(f"alias_match={','.join(matched_aliases)}")

    library_match = manifest.source_library.casefold() in lowered
    if library_match:
        score += 5.0
        reasons.append(f"library_match={manifest.source_library}")

    if manifest.package_name and manifest.package_name.casefold() in lowered:
        score += 4.0
        reasons.append(f"package_match={manifest.package_name}")
    if manifest.module_import_name and manifest.module_import_name.casefold() in lowered:
        score += 4.0
        reasons.append(f"import_match={manifest.module_import_name}")

    overlap = sorted(set(request_tokens) & manifest_tokens)
    if overlap:
        score += min(4.5, float(len(overlap)) * 1.2)
        reasons.append(f"token_overlap={','.join(overlap[:8])}")

    comparison_requested = _comparison_requested(user_text, request_tokens)
    workflow_requested = _workflow_requested(user_text, request_tokens)
    tooling_requested = _tooling_requested(user_text, request_tokens)
    if comparison_requested and status.provider_kind == "agent_provider":
        score += 1.8
        reasons.append("comparison_agent_provider")
    if workflow_requested and status.provider_kind == "agent_provider":
        score += 2.4
        reasons.append("workflow_agent_provider")
    if tooling_requested and status.provider_kind == "tool_provider":
        score += 2.4
        reasons.append("tooling_tool_provider")
    if tooling_requested and manifest.tool_id == "external_adapter:mcp_python_sdk":
        score += 2.8
        reasons.append("mcp_protocol_match")
    if workflow_requested and manifest.tool_id in _PREFERRED_AUTOGEN_TOOL_IDS:
        score += 1.2
        reasons.append("autogen_workflow_companion")
    if not status.selection_enabled:
        score -= 0.35
        reasons.append(f"selection_disabled={status.availability_status}")
    elif status.import_probe_worked:
        score += 0.75
        reasons.append("runtime_import_ok")

    return score, reasons


def _load_agent_tooling_runtime_probe_read_model() -> dict[str, Any]:
    from tools.jarvis_live_runtime.agent_tooling_runtime_probe import build_agent_tooling_runtime_probe_read_model

    try:
        return build_agent_tooling_runtime_probe_read_model()
    except Exception:
        return {
            "runtime_python": "",
            "probe_results": (),
            "installed": (),
            "import_probe_passed": (),
            "errors": ("runtime_probe_unavailable",),
        }


def _ordered_tool_ids(tool_ids: tuple[str, ...]) -> tuple[str, ...]:
    preferred_rank = {tool_id: index for index, tool_id in enumerate(_PREFERRED_EXTERNAL_ADAPTER_ORDER)}
    return tuple(sorted(tool_ids, key=lambda tool_id: (preferred_rank.get(tool_id, len(preferred_rank)), tool_id)))


def _ordered_manifests(manifests: tuple[UniversalToolManifest, ...]) -> tuple[UniversalToolManifest, ...]:
    ordered_ids = _ordered_tool_ids(tuple(manifest.tool_id for manifest in manifests))
    manifest_by_id = {manifest.tool_id: manifest for manifest in manifests}
    return tuple(manifest_by_id[tool_id] for tool_id in ordered_ids if tool_id in manifest_by_id)


def _normalize_errors(errors: Any) -> tuple[str, ...]:
    if isinstance(errors, str):
        return (errors,) if errors.strip() else ()
    if not isinstance(errors, (list, tuple)):
        return ()
    return tuple(str(error) for error in errors if str(error).strip())


def _build_probe_result_index(probe_read_model: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_package: dict[str, dict[str, Any]] = {}
    by_import: dict[str, dict[str, Any]] = {}
    for result in probe_read_model.get("probe_results", ()):
        if not isinstance(result, dict):
            continue
        package_name = str(result.get("package_name", "")).strip()
        import_name = str(result.get("import_name", "")).strip()
        if package_name:
            by_package[package_name] = result
        if import_name:
            by_import[import_name] = result
    return by_package, by_import


def _probe_result_for_manifest(
    manifest: UniversalToolManifest,
    probe_read_model: dict[str, Any],
    by_package: dict[str, dict[str, Any]],
    by_import: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if manifest.package_name and manifest.package_name in by_package:
        return by_package[manifest.package_name]
    if manifest.module_import_name and manifest.module_import_name in by_import:
        return by_import[manifest.module_import_name]
    return {
        "package_name": manifest.package_name,
        "import_name": manifest.module_import_name,
        "runtime_python": str(probe_read_model.get("runtime_python", "")),
        "installed": False,
        "import_probe_passed": False,
        "version_if_available": "",
        "errors": ("runtime_probe_missing_result",),
    }


def probe_external_tool_adapters(probe_read_model: dict[str, Any] | None = None) -> tuple[ExternalToolAdapterStatus, ...]:
    probe_payload = probe_read_model or _load_agent_tooling_runtime_probe_read_model()
    by_package, by_import = _build_probe_result_index(probe_payload)
    statuses: list[ExternalToolAdapterStatus] = []
    for manifest in _ordered_manifests(load_external_tool_manifests()):
        probe_result = _probe_result_for_manifest(manifest, probe_payload, by_package, by_import)
        installed = bool(probe_result.get("installed"))
        import_probe_worked = bool(probe_result.get("import_probe_passed"))
        legacy_alias = manifest.tool_id == _LEGACY_AUTOGEN_TOOL_ID and not import_probe_worked
        selection_enabled = import_probe_worked and not legacy_alias
        runtime_errors = _normalize_errors(probe_result.get("errors", ()))
        if selection_enabled:
            availability_status = "available"
            activation_blocked_reason = ""
        elif legacy_alias:
            availability_status = "legacy_unavailable"
            activation_blocked_reason = "legacy_alias_requires_importable_autogen_runtime"
        else:
            availability_status = "unavailable"
            activation_blocked_reason = runtime_errors[0] if runtime_errors else "runtime_probe_failed"
        statuses.append(
            ExternalToolAdapterStatus(
                tool_id=manifest.tool_id,
                source_library=manifest.source_library,
                capability_id=manifest.capability_id,
                adapter_mode=manifest.adapter_mode,
                provider_kind=manifest.provider_kind,
                installed=installed,
                activation_blocked_reason=activation_blocked_reason,
                import_probe_worked=import_probe_worked,
                requires_verified_owner=manifest.requires_verified_owner,
                safe_direct_allowed=manifest.safe_direct_allowed,
                risk_gate_required=manifest.risk_class == "risk_gate",
                visible_to_jarvis=True,
                not_canonical_truth=manifest.not_canonical_truth,
                availability_status=availability_status,
                selection_enabled=selection_enabled,
                legacy_alias=legacy_alias,
                runtime_python=str(probe_result.get("runtime_python", "")),
                runtime_package_name=str(probe_result.get("package_name", manifest.package_name)),
                runtime_import_name=str(probe_result.get("import_name", manifest.module_import_name)),
                runtime_version_if_available=str(probe_result.get("version_if_available", "")),
                runtime_errors=runtime_errors,
            )
        )
    return tuple(statuses)


def list_active_external_adapter_tool_ids(probe_read_model: dict[str, Any] | None = None) -> tuple[str, ...]:
    statuses = probe_external_tool_adapters(probe_read_model)
    return tuple(status.tool_id for status in statuses if status.selection_enabled)


def normalize_external_adapter_tool_ids(
    tool_ids: tuple[str, ...],
    probe_read_model: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    status_by_id = {status.tool_id: status for status in probe_external_tool_adapters(probe_read_model)}
    normalized: list[str] = []
    for tool_id in tool_ids:
        if not tool_id.startswith("external_adapter:"):
            normalized.append(tool_id)
            continue
        status = status_by_id.get(tool_id)
        if status is None:
            continue
        if status.selection_enabled:
            normalized.append(tool_id)
            continue
        if tool_id == _LEGACY_AUTOGEN_TOOL_ID:
            for preferred_tool_id in _PREFERRED_AUTOGEN_TOOL_IDS:
                preferred_status = status_by_id.get(preferred_tool_id)
                if preferred_status is not None and preferred_status.selection_enabled:
                    normalized.append(preferred_tool_id)
    return tuple(dict.fromkeys(normalized))


def rank_external_adapter_candidates_for_text(
    user_text: str,
    probe_read_model: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...]:
    probe_payload = probe_read_model or _load_agent_tooling_runtime_probe_read_model()
    statuses = probe_external_tool_adapters(probe_payload)
    status_by_id = {status.tool_id: status for status in statuses}
    request_tokens = _semantic_tokens(user_text)
    candidates: list[ExternalAdapterSemanticCandidate] = []
    for manifest in _ordered_manifests(load_external_tool_manifests()):
        status = status_by_id[manifest.tool_id]
        score, reasons = _score_manifest_for_request(user_text, request_tokens, manifest, status)
        if score <= 0:
            continue
        candidates.append(
            ExternalAdapterSemanticCandidate(
                tool_id=manifest.tool_id,
                score=round(score, 3),
                reason="; ".join(reasons) if reasons else "semantic_match",
                selection_enabled=status.selection_enabled,
                availability_status=status.availability_status,
                provider_kind=status.provider_kind,
                risk_class="risk_gate" if status.risk_gate_required else "read_only",
            )
        )
    return tuple(
        candidate.to_read_model()
        for candidate in sorted(
            candidates,
            key=lambda item: (-item.score, 0 if item.selection_enabled else 1, item.tool_id),
        )
    )


def build_external_adapter_semantic_route(
    user_text: str,
    probe_read_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = rank_external_adapter_candidates_for_text(user_text, probe_read_model)
    lowered = str(user_text or "").casefold()
    request_tokens = _semantic_tokens(user_text)
    comparison_requested = _comparison_requested(lowered, request_tokens)
    workflow_requested = _workflow_requested(lowered, request_tokens)
    tooling_requested = _tooling_requested(lowered, request_tokens)
    matched = bool(candidates)
    top_score = float(candidates[0]["score"]) if candidates else 0.0

    active_candidates = tuple(candidate for candidate in candidates if bool(candidate.get("selection_enabled", False)))
    unavailable_candidates = tuple(candidate for candidate in candidates if not bool(candidate.get("selection_enabled", False)))

    if not matched or (top_score < 3.4 and not (comparison_requested or workflow_requested or tooling_requested)):
        return {
            "matched": False,
            "intent_family": "CONVERSATION",
            "selected_tools": (),
            "selected_agent_roles": (),
            "risk_class": "read_only",
            "proposal_only": True,
            "execution_allowed": False,
            "confidence": top_score,
            "reason": "no confident external adapter semantic route",
            "candidate_matches": candidates,
            "unavailable_matches": unavailable_candidates,
        }

    if comparison_requested:
        intent_family = "AGENT_ENGINE_COMPARISON"
        selected_tools = tuple(candidate["tool_id"] for candidate in active_candidates[:5])
        reason = "semantic comparison route from external adapter registry"
    elif tooling_requested and active_candidates and str(active_candidates[0].get("provider_kind", "")) == "tool_provider":
        intent_family = "EXTERNAL_ADAPTER_SELECTION"
        if len(active_candidates) >= 2 and float(active_candidates[0]["score"]) >= float(active_candidates[1]["score"]) + 1.0:
            selected_tools = (active_candidates[0]["tool_id"],)
        else:
            selected_tools = tuple(candidate["tool_id"] for candidate in active_candidates[:3])
        reason = "semantic tool/protocol selection from external adapter registry"
    elif workflow_requested:
        intent_family = "EXTERNAL_AGENT_WORKFLOW_PLAN"
        workflow_candidates = tuple(
            candidate
            for candidate in active_candidates
            if str(candidate.get("provider_kind", "")) == "agent_provider"
        )
        selected_tools = tuple(candidate["tool_id"] for candidate in workflow_candidates[:4])
        if "external_adapter:autogen_agentchat" in selected_tools and "external_adapter:autogen_ext" not in selected_tools:
            selected_tools = normalize_external_adapter_tool_ids((*selected_tools, "external_adapter:autogen_ext"))
        reason = "semantic workflow-plan route from external adapter registry"
    else:
        intent_family = "EXTERNAL_ADAPTER_SELECTION"
        if len(active_candidates) >= 2 and float(active_candidates[0]["score"]) >= float(active_candidates[1]["score"]) + 1.5:
            selected_tools = (active_candidates[0]["tool_id"],)
        else:
            selected_tools = tuple(candidate["tool_id"] for candidate in active_candidates[:3])
        reason = "semantic external adapter selection from registry metadata"

    selected_tools = normalize_external_adapter_tool_ids(tuple(selected_tools), probe_read_model)
    if not selected_tools and active_candidates:
        selected_tools = tuple(candidate["tool_id"] for candidate in active_candidates[:1])

    return {
        "matched": bool(selected_tools),
        "intent_family": intent_family,
        "selected_tools": selected_tools,
        "selected_agent_roles": ("tool_selector_agent",),
        "risk_class": "risk_gate",
        "proposal_only": True,
        "execution_allowed": False,
        "confidence": max(top_score, 0.0),
        "reason": reason,
        "candidate_matches": candidates,
        "unavailable_matches": unavailable_candidates,
    }


def select_external_adapter_tools_for_text(
    user_text: str,
    probe_read_model: dict[str, Any] | None = None,
) -> tuple[UniversalToolManifest, ...]:
    lowered = str(user_text).casefold()
    manifests = _ordered_manifests(load_external_tool_manifests())
    manifest_by_id = {manifest.tool_id: manifest for manifest in manifests}
    selected_tool_ids: list[str] = []
    for manifest in manifests:
        aliases = tuple(alias.casefold() for alias in manifest.aliases)
        if any(alias in lowered for alias in aliases) or manifest.source_library.casefold() in lowered:
            selected_tool_ids.append(manifest.tool_id)
    if "autogen" in lowered or "pyautogen" in lowered:
        selected_tool_ids.extend(_PREFERRED_AUTOGEN_TOOL_IDS)
        selected_tool_ids.append(_LEGACY_AUTOGEN_TOOL_ID)
    normalized_ids = normalize_external_adapter_tool_ids(tuple(selected_tool_ids), probe_read_model)
    return tuple(manifest_by_id[tool_id] for tool_id in normalized_ids if tool_id in manifest_by_id)


def build_jarvis_external_adapter_visibility_read_model(probe_read_model: dict[str, Any] | None = None) -> dict[str, Any]:
    probe_payload = probe_read_model or _load_agent_tooling_runtime_probe_read_model()
    adapter_statuses = probe_external_tool_adapters(probe_payload)
    active_adapter_ids = tuple(status.tool_id for status in adapter_statuses if status.selection_enabled)
    unavailable_adapter_ids = tuple(status.tool_id for status in adapter_statuses if not status.selection_enabled)
    legacy_adapter_ids = tuple(status.tool_id for status in adapter_statuses if status.legacy_alias)
    return {
        "registry": build_external_tool_registry().to_read_model(),
        "adapters": tuple(status.to_read_model() for status in adapter_statuses),
        "active_adapter_ids": active_adapter_ids,
        "visible_adapter_ids": active_adapter_ids,
        "unavailable_adapter_ids": unavailable_adapter_ids,
        "legacy_adapter_ids": legacy_adapter_ids,
        "runtime_python": str(probe_payload.get("runtime_python", "")),
        "probe": probe_payload,
    }
