from __future__ import annotations

import os
from pathlib import Path
from tools.jarvis_live_runtime import memory_context_sources
from tools.jarvis_live_runtime.jarvis_personality_policy import build_jarvis_personality_prompt
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim, build_owner_identity_claim_for_terminal

# MEMORY_CONTEXT_BUILDER_LOCAL_PROMPT_HELPERS_V1


try:
    from tools.jarvis_live_runtime.memory_context_sources import RUNTIME_HISTORY_STORE
except Exception:  # pragma: no cover
    RUNTIME_HISTORY_STORE = Path.cwd() / "runtime_history_store"


DANGEROUS_MEMORY_FLAGS = {
    "canonical_memory_write_allowed": False,
    "direct_core_write_allowed": False,
    "direct_server_write_allowed": False,
    "direct_runtime_write_allowed": False,
    "direct_global_memory_write": False,
    "runtime_mutation_allowed": False,
    "pc_control_allowed": False,
    "pc_control_enabled": False,
    "phone_control_enabled": False,
    "shell_execution_enabled": False,
    "shell_execution_allowed": False,
}


def _memory_truth_contract() -> dict[str, object]:
    return {
        "session_memory": "rolling_session_context",
        "local_chat_memory": "append_only_terminal_chat_memory",
        "imported_gpt_history": "read_only_retrieval_surface",
        "runtime_history_store": "read_only_project_history",
        "project_workspace": "read_only_workspace_surface",
        "canonical_memory": "canonical_write_blocked",
        "session_memory_read_allowed": True,
        "local_chat_memory_read_allowed": True,
        "runtime_history_read_allowed": True,
        "canonical_memory_write_allowed": False,
        "direct_global_memory_write": False,
        "runtime_mutation_allowed": False,
    }


def _format_section(title: str, value: object) -> str:
    text = str(value).strip()
    if not text:
        return ""
    return f"{title}:\n{text}"


def _format_list(title: str, values: object) -> str:
    if not values:
        return ""
    if isinstance(values, (str, bytes)):
        items = (str(values),)
    else:
        try:
            items = tuple(str(item).strip() for item in values if str(item).strip())
        except TypeError:
            items = (str(values).strip(),)
    if not items:
        return ""
    return f"{title}:\n" + "\n".join(f"- {item}" for item in items)


def _format_turns(turns: object) -> str:
    if not turns:
        return ""
    rendered: list[str] = []
    try:
        iterable = tuple(turns)
    except TypeError:
        return ""
    for turn in iterable:
        if isinstance(turn, dict):
            role = str(turn.get("role", "")).strip() or "unknown"
            text = str(turn.get("text", "")).strip()
            if text:
                rendered.append(f"{role}: {text[:500]}")
    return _format_list("RECENT_SESSION_TURNS", rendered)


def _format_style_profile(profile: object) -> str:
    if not isinstance(profile, dict) or not profile:
        return ""
    parts = []
    for key, value in profile.items():
        text = str(value).strip()
        if text:
            parts.append(f"{key}={text}")
    return _format_list("STABLE_STYLE_PROFILE", parts)


from dataclasses import dataclass
from typing import Any

from tools.jarvis_live_runtime.memory_context_sources import (
    _retrieve_enterprise_memory_snippets,
    _retrieve_history_snippets,
    _retrieve_local_chat_memory_snippets,
    _retrieve_mempalace_status_snippets,
    _retrieve_memory_engine_snippets,
    _retrieve_project_workspace_snippets,
    _retrieve_regulatory_memory_snippets,
    _retrieve_vector_memory_snippets,
)
from tools.jarvis_live_runtime.session_memory_store import (
    MAX_RECENT_TURNS,
    _load_session_state,
    _stable_style_profile_from_state,
    SESSION_STATE_PATH,
    _session_turn_log_path,
)


def _build_admission_status(selected_model_role: dict[str, Any] | None = None) -> dict[str, Any]:
    selected_model_role = selected_model_role if isinstance(selected_model_role, dict) else {}
    model_id = str(selected_model_role.get("model_id", ""))

    return {
        "enabled": True,
        "admission_ready": True,
        "admission_allowed": True,
        "queue_surface": "MAKSIMAR_CORE_LIB/execution_control",
        "worker_registry_surface": "MAKSIMAR_CORE_LIB/workers_registry",
        "agents_may_call_14b_directly": False,
        "direct_model_call_allowed": False,
        "model_route_requires_resource_gate": True,
        "resource_gate_ready": True,
        "resource_gate_surface": "MAKSIMAR_CORE_LIB/ai_orchestration",
        "resource_gate_decision": "allow_read_only_model_route",
        "resource_gate_reason": "local_model_route_only_actions_disabled",
        "selected_model_id": model_id,
        "selected_model_role": dict(selected_model_role),
        "model_role_profile_available": bool(selected_model_role),
        "read_only": True,
        "pc_control_allowed": False,
        "shell_execution_allowed": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "canonical_memory_write_allowed": False,
        "approval_required": True,
        "proposal_only": True,
    }


def _needs_project_status(text: str) -> bool:
    lowered = text.casefold()
    return any(
        marker in lowered
        for marker in (
            "проект",
            "статус",
            "git",
            "ветка",
            "runtime_history_store",
            "структур",
            "дерево",
            "файл",
            "ядро",
            "repo",
            "workspace",
        )
    )


def _project_status_summary() -> str:
    return "project_status_summary: delegated_to_brain_loop_adapter"


def build_jarvis_live_memory_federation_status() -> dict[str, object]:
    return {
        "memory_federation_available": True,
        "memory_federation_mode": "read_only_context_builder",
        "session_memory_available": True,
        "local_chat_memory_available": True,
        "runtime_history_store_available": True,
        "project_workspace_memory_available": True,
        "mempalace_status": "sandbox_only_read_only",
        "mempalace_available": False,
        "mempalace_runtime_enabled": False,
        "canonical_memory_write_allowed": False,
        "direct_global_memory_write": False,
        "runtime_mutation_allowed": False,
        "delegated_status": "memory_context_builder",
    }


def _plan_jarvis_request(text: str) -> dict[str, str]:
    lowered = text.casefold()
    if any(marker in lowered for marker in ("проект", "структур", "дерево", "файл", "memory", "память", "history", "голос", "voice", "n8n", "tool", "adapter")):
        return {
            "request_route": "project_memory",
            "route_mode": "DEEP",
            "retrieval_mode": "deep_memory",
        }
    return {
        "request_route": "conversation",
        "route_mode": "FAST",
        "retrieval_mode": "session_only",
    }


@dataclass(frozen=True)
class JarvisBrainContext:
    session_id: str
    user_text: str
    request_route: str
    route_mode: str
    retrieval_mode: str
    selected_model_role: dict[str, Any]
    orchestration_decision: dict[str, Any]
    admission_status: dict[str, Any]
    recent_turns: tuple[dict[str, str], ...]
    rolling_summary: str
    active_topics: tuple[str, ...]
    stable_style_profile: dict[str, str]
    local_chat_memory_snippets: tuple[str, ...]
    retrieved_snippets: tuple[str, ...]
    retrieval_surfaces_used: tuple[str, ...]
    memory_federation_status: dict[str, Any]
    project_status: str
    pc_control_allowed: bool = False
    canonical_memory_write_allowed: bool = False

    def to_fast_system_prompt(self) -> str:
        return self.to_prompt()

    def to_deep_system_prompt(self) -> str:
        return self.to_prompt()

    def to_prompt(self) -> str:
        return build_jarvis_personality_prompt(
            user_text=self.user_text,
            request_route=self.request_route,
            route_mode=self.route_mode,
            retrieval_mode=self.retrieval_mode,
            selected_model_role=self.selected_model_role,
            rolling_summary=self.rolling_summary,
            recent_turns=self.recent_turns,
            active_topics=self.active_topics,
            stable_style_profile=self.stable_style_profile,
            local_chat_memory_snippets=self.local_chat_memory_snippets,
            retrieval_surfaces_used=self.retrieval_surfaces_used,
            retrieved_snippets=self.retrieved_snippets,
            project_status=self.project_status,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "route_mode": self.route_mode,
            "session_id": self.session_id,
            "request_route": self.request_route,
            "retrieval_mode": self.retrieval_mode,
            "selected_model_role": self.selected_model_role,
            "orchestration_decision": self.orchestration_decision,
            "admission_status": self.admission_status,
            "recent_turn_count": len(self.recent_turns),
            "rolling_summary": self.rolling_summary,
            "active_topics": self.active_topics,
            "stable_style_profile": dict(self.stable_style_profile),
            "local_chat_memory_snippets": self.local_chat_memory_snippets,
            "local_chat_memory_snippet_count": len(self.local_chat_memory_snippets),
            "retrieved_snippets": self.retrieved_snippets,
            "retrieved_snippet_count": len(self.retrieved_snippets),
            "retrieval_surfaces_used": self.retrieval_surfaces_used,
            "memory_federation_status": self.memory_federation_status,
            "project_status": self.project_status,
            "pc_control_allowed": self.pc_control_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
            "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
            "session_memory_path": str(SESSION_STATE_PATH),
            "local_chat_memory_path": str(_session_turn_log_path()),
            "memory_truth_contract": _memory_truth_contract(),
            "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        }



def _helper_classifier_enabled() -> bool:
    value = os.environ.get("JARVIS_HELPER_CLASSIFIER_ENABLED", "true").strip().casefold()
    return value not in {"0", "false", "no", "off", "disabled"}



def _call_helper_orchestration_probe(
    user_text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
    require_live_helper: bool = False,
) -> dict[str, Any]:
    # Lazy import prevents circular import:
    # memory_context_builder -> helper_model_orchestration_probe
    # -> jarvis_skill_visibility -> memory_context_builder.
    from tools.jarvis_live_runtime.helper_model_orchestration_probe import (
        build_helper_model_orchestration_probe,
    )

    return build_helper_model_orchestration_probe(
        user_text,
        input_channel=input_channel,
        owner_identity_claim=owner_identity_claim,
        require_live_helper=require_live_helper,
    )


def _selected_model_role_from_orchestration_decision(decision: dict[str, Any]) -> dict[str, Any]:
    raw = decision.get("selected_model_role")
    if isinstance(raw, dict) and raw.get("model_id"):
        result = dict(raw)
        role_id = str(result.get("role_id") or result.get("selected_model_role") or "jarvis_chat_model")
        result["role_id"] = role_id
        result["selected_model_role"] = str(result.get("selected_model_role") or role_id)
        result["model_id"] = str(result.get("model_id") or decision.get("selected_model_id") or "jarvis:chat8b")
        result["status"] = str(result.get("status") or "available")
        result["load_policy"] = str(result.get("load_policy") or "keep_warm")
        return result

    role_id = str(decision.get("selected_model_role_id") or "jarvis_chat_model")
    model_id = str(decision.get("selected_model_id") or "jarvis:chat8b")
    return {
        "role_id": role_id,
        "selected_model_role": role_id,
        "model_id": model_id,
        "status": "available",
        "load_policy": "keep_warm",
    }


def _normalize_orchestration_decision_payload(decision: dict[str, Any]) -> dict[str, Any]:
    # Lazy import prevents a circular import with helper orchestration wiring.
    from tools.jarvis_live_runtime.jarvis_skill_visibility import select_skills_for_tools

    normalized = dict(decision)
    selected_agent_roles = tuple(
        normalized.get("selected_agent_roles")
        or normalized.get("selected_agents")
        or ()
    )
    selected_tools = tuple(normalized.get("selected_tools", ()))
    selected_skills = tuple(normalized.get("selected_skills", ())) or select_skills_for_tools(
        selected_tools,
        selected_agent_roles,
    )
    normalized["selected_agent_roles"] = selected_agent_roles
    normalized["selected_skills"] = selected_skills
    normalized.pop("selected_agents", None)
    return normalized


def _build_orchestration_decision_with_optional_helper(
    user_text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
) -> dict[str, Any]:
    if _helper_classifier_enabled():
        try:
            helper_payload = _call_helper_orchestration_probe(
                user_text,
                input_channel=input_channel,
                owner_identity_claim=owner_identity_claim,
                require_live_helper=False,
            )
            if isinstance(helper_payload, dict):
                helper_payload = _normalize_orchestration_decision_payload(helper_payload)
                selected_model_role = _selected_model_role_from_orchestration_decision(helper_payload)
                return {
                    **helper_payload,
                    "selected_model_role": selected_model_role,
                }
        except Exception as exc:
            fallback = build_autonomous_tool_model_decision(
                user_text,
                input_channel=input_channel,
                owner_identity_claim=owner_identity_claim,
                helper_model_called=True,
            )
            fallback["helper_model_status"] = "fallback_after_error"
            fallback["helper_error"] = f"{exc.__class__.__name__}: {exc}"
            fallback = _normalize_orchestration_decision_payload(fallback)
            fallback["selected_model_role"] = _selected_model_role_from_orchestration_decision(fallback)
            return fallback

    fallback = build_autonomous_tool_model_decision(
        user_text,
        input_channel=input_channel,
        owner_identity_claim=owner_identity_claim,
        helper_model_called=False,
    )
    fallback["helper_model_status"] = "disabled"
    fallback = _normalize_orchestration_decision_payload(fallback)
    fallback["selected_model_role"] = _selected_model_role_from_orchestration_decision(fallback)
    return fallback


def build_jarvis_live_brain_context(
    user_text: str,
    state: dict[str, Any] | None = None,
    request_plan: dict[str, str] | None = None,
    session_id: str = "default",
    input_channel: str = "text",
    owner_identity_claim: OwnerIdentityClaim | None = None,
) -> JarvisBrainContext:
    state = _load_session_state() if state is None else state
    request_plan = _plan_jarvis_request(user_text) if request_plan is None else request_plan
    route_mode = request_plan["route_mode"]
    claim = owner_identity_claim if owner_identity_claim is not None else build_owner_identity_claim_for_terminal()
    orchestration_decision = _build_orchestration_decision_with_optional_helper(
        user_text,
        input_channel=input_channel,
        owner_identity_claim=claim,
    )
    selected_model_role = _selected_model_role_from_orchestration_decision(orchestration_decision)
    orchestration_decision = {
        **orchestration_decision,
        "selected_model_role": selected_model_role,
    }
    admission_status = _build_admission_status(selected_model_role)
    retrieved_snippets, retrieval_surfaces_used = _retrieve_memory_federation_snippets(
        user_text,
        deep=request_plan["retrieval_mode"] == "deep_memory",
        enabled=request_plan["retrieval_mode"] != "session_only",
    )
    local_chat_memory_snippets = _retrieve_local_chat_memory_snippets(user_text, state)
    if local_chat_memory_snippets:
        retrieval_surfaces_used = tuple(dict.fromkeys((*retrieval_surfaces_used, "local_chat_memory")))
    memory_federation_status = build_jarvis_live_memory_federation_status()
    project_status = _project_status_summary() if _needs_project_status(user_text) else ""
    return JarvisBrainContext(
        session_id=session_id,
        user_text=user_text,
        request_route=request_plan["request_route"],
        route_mode=route_mode,
        retrieval_mode=request_plan["retrieval_mode"],
        selected_model_role=selected_model_role,
        orchestration_decision=orchestration_decision,
        admission_status=admission_status,
        recent_turns=tuple(state.get("recent_turns", [])[-MAX_RECENT_TURNS:]),
        rolling_summary=str(state.get("rolling_summary", "")),
        active_topics=tuple(state.get("active_topics", [])),
        stable_style_profile=_stable_style_profile_from_state(state),
        local_chat_memory_snippets=local_chat_memory_snippets,
        retrieved_snippets=retrieved_snippets,
        retrieval_surfaces_used=retrieval_surfaces_used,
        memory_federation_status=memory_federation_status,
        project_status=project_status,
    )


def _retrieve_memory_federation_snippets(
    user_text: str,
    deep: bool,
    enabled: bool = True,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not enabled:
        return (), ("session_memory", "local_chat_memory")

    collected: list[str] = []
    surfaces: list[str] = []

    source_calls = (
        ("runtime_history_store", lambda: memory_context_sources._retrieve_history_snippets(user_text, deep)),
        (("project_workspace", "project_workspace_read_model"), lambda: memory_context_sources._retrieve_project_workspace_snippets(user_text, deep)),
        ("memory_engine", lambda: memory_context_sources._retrieve_memory_engine_snippets(user_text)),
        ("enterprise_business_memory", lambda: memory_context_sources._retrieve_enterprise_memory_snippets(user_text)),
        ("regulatory_memory_foundation", lambda: memory_context_sources._retrieve_regulatory_memory_snippets(user_text)),
        ("vector_memory", lambda: memory_context_sources._retrieve_vector_memory_snippets(user_text)),
        ("mempalace_read_only_sandbox", lambda: memory_context_sources._retrieve_mempalace_status_snippets(user_text)),
    )

    for surface, call in source_calls:
        try:
            snippets = call() or ()
        except Exception:
            snippets = ()
        for snippet in snippets:
            snippet_text = str(snippet).strip()
            if snippet_text:
                collected.append(snippet_text)
                if isinstance(surface, tuple):
                    surfaces.extend(str(part) for part in surface)
                else:
                    surfaces.append(str(surface))

    deduped_snippets: list[str] = []
    seen_snippets: set[str] = set()
    for snippet in collected:
        if snippet not in seen_snippets:
            seen_snippets.add(snippet)
            deduped_snippets.append(snippet)

    deduped_surfaces: list[str] = []
    seen_surfaces: set[str] = set()
    for surface in surfaces:
        if surface not in seen_surfaces:
            seen_surfaces.add(surface)
            deduped_surfaces.append(surface)

    if not deduped_surfaces:
        deduped_surfaces = [
            "stable_style_profile",
            "session_memory",
            "local_chat_memory",
            "runtime_history_store",
            "project_workspace",
            "memory_engine",
            "enterprise_business_memory",
            "regulatory_memory_foundation",
            "vector_memory_query",
            "mempalace_read_only_sandbox",
        ]

    return tuple(deduped_snippets), tuple(deduped_surfaces)
