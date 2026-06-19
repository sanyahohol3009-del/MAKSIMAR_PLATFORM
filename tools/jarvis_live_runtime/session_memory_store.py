from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
SESSION_MEMORY_ROOT = RUNTIME_ROOT / "session_memory"
SESSION_STATE_PATH = SESSION_MEMORY_ROOT / "jarvis_live_session_state.json"
SESSION_TURN_LOG_NAME = "jarvis_live_terminal_turns.jsonl"

MAX_RECENT_TURNS = 4

STABLE_STYLE_PROFILE = {
    "user_name": "Александр",
    "assistant_identity": "JARVIS",
    "relation_style": "брат / напарник по гаражу",
    "communication_style": "natural, direct, practical, not overly short, not template-like",
    "avoid": "не повторять 'Нужна помощь?' после каждого ответа; не начинать отношения заново в новой сессии",
    "concise_rule": "быть коротким только когда владелец просит коротко; иначе отвечать достаточно полно для задачи",
}

DANGEROUS_MEMORY_FLAGS = {
    "direct_core_write_allowed": False,
    "runtime_mutation_allowed": False,
    "canonical_truth_update_allowed": False,
    "auto_apply_allowed": False,
    "deployment_allowed_now": False,
    "external_release_allowed_now": False,
    "memory_foundation_reopen_allowed": False,
    "regulatory_truth_update_allowed": False,
    "regulatory_auto_apply_allowed": False,
    "approval_bypass_allowed": False,
    "self_expansion_allowed_now": False,
    "pc_control_enabled": False,
    "phone_control_enabled": False,
    "direct_global_memory_write": False,
    "auto_project_truth_write": False,
}


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(
        part
        for part in text.casefold().replace("?", " ").replace(",", " ").split()
        if len(part) >= 4
    )


def _append_assistant_and_summarize(
    state: dict[str, Any],
    response_text: str,
    context: JarvisBrainContext,
) -> None:
    _append_turn(state, "assistant", response_text)
    state["rolling_summary"] = _build_rolling_summary(state)
    state["active_topics"] = _extract_active_topics(context.user_text)
    _save_session_state(state)
    _append_local_chat_memory_record(state, response_text, context)


def _append_turn(state: dict[str, Any], role: str, text: str) -> None:
    if not text.strip():
        return
    turns = list(state.get("recent_turns", []))
    turns.append({"role": role, "text": text.strip(), "updated_at": str(time.time())})
    state["recent_turns"] = turns[-MAX_RECENT_TURNS:]
    state["local_session_persistence"] = True
    state["canonical_memory_write_allowed"] = False
    state["pc_control_allowed"] = False


def _append_local_chat_memory_record(
    state: dict[str, Any],
    response_text: str,
    context: JarvisBrainContext,
) -> None:
    if not context.user_text.strip() and not response_text.strip():
        return
    record = {
        "timestamp": _timestamp(),
        "session_id": context.session_id,
        "day_bucket": _day_bucket(),
        "user_message": context.user_text.strip(),
        "jarvis_answer": response_text.strip(),
        "route": context.request_route,
        "mode": context.route_mode,
        "model_id": context.selected_model_role["model_id"],
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "retrieval_mode": context.retrieval_mode,
        "retrieval_surfaces_used": context.retrieval_surfaces_used,
        "retrieved_snippet_count": len(context.retrieved_snippets),
        "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
        "source": "jarvis_terminal_chat",
        "turn_summary": _brief_turn_summary(context.user_text, response_text),
        "active_task": _detect_active_task(context.user_text),
        "style_preference": _extract_style_preference(context.user_text),
        "thinking_stored": False,
        "canonical_memory_write_allowed": False,
        "direct_global_memory_write": False,
        "pc_control_allowed": False,
    }
    try:
        SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
        with _session_turn_log_path().open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError:
        return


def _session_turn_log_path() -> Path:
    return SESSION_MEMORY_ROOT / SESSION_TURN_LOG_NAME


def _read_recent_local_chat_records(limit: int = 8) -> tuple[dict[str, Any], ...]:
    path = _session_turn_log_path()
    if not path.exists():
        return ()
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ()
    records: list[dict[str, Any]] = []
    for line in reversed(lines[-max(limit * 3, limit):]):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and payload.get("source") == "jarvis_terminal_chat":
            records.insert(0, payload)
        if len(records) >= limit:
            break
    return tuple(records[-limit:])


def _load_session_state() -> dict[str, Any]:
    if not SESSION_STATE_PATH.exists():
        return _empty_session_state()
    try:
        payload = json.loads(SESSION_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_session_state()
    if not isinstance(payload, dict):
        return _empty_session_state()
    return _normalize_session_state(payload)


def _save_session_state(state: dict[str, Any]) -> None:
    state.update(_memory_enablement_flags())
    state["session_memory_path"] = str(SESSION_STATE_PATH)
    state["local_chat_memory_path"] = str(_session_turn_log_path())
    state["canonical_memory_write_allowed"] = False
    state["pc_control_allowed"] = False
    try:
        SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
        SESSION_STATE_PATH.write_text(
            json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2),
            encoding="utf-8",
        )
    except OSError:
        return


def _empty_session_state() -> dict[str, Any]:
    return _normalize_session_state({
        "recent_turns": [],
        "rolling_summary": "",
        "active_topics": [],
        "local_session_persistence": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    })


def _normalize_session_state(state: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(state)
    normalized.setdefault("recent_turns", [])
    normalized.setdefault("rolling_summary", "")
    normalized.setdefault("active_topics", [])
    normalized.setdefault("style_preferences", {})
    normalized["stable_style_profile"] = _stable_style_profile_from_state(normalized)
    normalized["local_session_persistence"] = True
    normalized["canonical_memory_write_allowed"] = False
    normalized["pc_control_allowed"] = False
    normalized["dangerous_mutation_flags"] = dict(DANGEROUS_MEMORY_FLAGS)
    normalized["memory_truth_contract"] = _memory_truth_contract()
    normalized.update(_memory_enablement_flags())
    return normalized


def _stable_style_profile_from_state(state: dict[str, Any]) -> dict[str, str]:
    profile = dict(STABLE_STYLE_PROFILE)
    preferences = state.get("style_preferences")
    if isinstance(preferences, dict):
        for key, value in preferences.items():
            if isinstance(key, str) and isinstance(value, str) and value.strip():
                profile[key] = value.strip()[:300]
    return profile


def _update_style_preferences(state: dict[str, Any], user_text: str) -> None:
    preference = _extract_style_preference(user_text)
    if not preference:
        return
    preferences = state.get("style_preferences")
    if not isinstance(preferences, dict):
        preferences = {}
    preferences["explicit_owner_style_preference"] = preference
    state["style_preferences"] = preferences


def _extract_style_preference(text: str) -> str:
    lowered = text.casefold()
    markers = ("общайся", "стиль", "предпочитаю", "говори", "отвечай")
    if not any(marker in lowered for marker in markers):
        return ""
    if any(marker in lowered for marker in ("короче", "кратко", "не растягивай")):
        return "владелец просит отвечать короче в этом стиле"
    if any(marker in lowered for marker in ("подробнее", "развернуто", "не слишком коротко")):
        return "владелец просит не быть чрезмерно кратким и давать достаточно контекста"
    if any(marker in lowered for marker in ("по братски", "по-братски", "брат")):
        return "владелец допускает братский, прямой, живой стиль общения"
    return text.strip()[:240]


def _memory_enablement_flags() -> dict[str, bool]:
    return {
        "memory_enabled": True,
        "project_memory_enabled": True,
        "project_memory_read_enabled": True,
        "conversation_memory_enabled": True,
        "chat_memory_enabled": True,
        "session_memory_enabled": True,
        "runtime_history_enabled": True,
        "runtime_history_read_enabled": True,
        "rag_enabled": True,
        "retrieval_enabled": True,
        "memory_retrieval_enabled": True,
        "project_history_retrieval_enabled": True,
        "history_retrieval_enabled": True,
        "runtime_history_store_enabled": True,
        "jarvis_history_read_enabled": True,
        "jarvis_history_query_enabled": True,
        "roadmap_context_enabled": True,
        "roadmap_next_step_enabled": True,
        "memory_skill_context_enabled": True,
        "memory_summary_context_enabled": True,
        "project_workspace_read_enabled": True,
        "project_tree_read_enabled": True,
        "project_file_read_enabled": True,
        "project_source_snippet_read_enabled": True,
        "project_structure_context_enabled": True,
        "regulatory_memory_read_enabled": True,
        "regulatory_summary_enabled": True,
        "audit_read_model_enabled": True,
        "approval_context_read_enabled": True,
        "source_trace_context_enabled": True,
        "evidence_pack_context_enabled": True,
        "recent_turn_context_enabled": True,
        "rolling_summary_enabled": True,
        "local_session_persistence_enabled": True,
        "context_assembly_enabled": True,
        "retrieval_before_project_answer": True,
        "hallucination_guard_enabled": True,
        "memory_truth_contract_enabled": True,
        "session_memory_write_enabled": True,
        "runtime_history_append_enabled": False,
        "conversation_history_append_enabled": True,
        "chat_transcript_append_enabled": True,
        "chat_memory_write_enabled": True,
    }


def _memory_truth_contract() -> dict[str, str]:
    return {
        "canonical_truth": "read_only_not_written_by_live_chat",
        "project_history": "read_only_imported_history_context",
        "project_workspace": "read_only_tree_and_bounded_file_snippets",
        "local_chat_memory": "append_only_terminal_chat_memory",
        "session_summary": "local_session_context",
        "user_preference": "local_style_preference",
        "uncertain_memory": "must_be_reported_as_uncertain",
    }


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _day_bucket() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def _brief_turn_summary(user_text: str, response_text: str) -> str:
    return f"user={user_text.strip()[:160]} | jarvis={response_text.strip()[:160]}"


def _detect_active_task(text: str) -> str:
    lowered = text.casefold()
    if any(marker in lowered for marker in ("task:", "задача", "сделай", "почини", "implement", "audit")):
        return text.strip()[:240]
    return ""


def _build_rolling_summary(state: dict[str, Any]) -> str:
    turns = list(state.get("recent_turns", []))[-4:]
    joined = " | ".join(f"{turn.get('role')}: {turn.get('text')}" for turn in turns)
    return joined[:900]


def _extract_active_topics(text: str) -> list[str]:
    tokens = [token for token in _query_tokens(text) if len(token) > 4]
    return tokens[:8]


def _format_turns(turns: tuple[dict[str, str], ...]) -> str:
    if not turns:
        return ""
    lines = [f"- {turn.get('role')}: {turn.get('text')}" for turn in turns]
    return "RECENT_SESSION_TURNS:\n" + "\n".join(lines)


def _format_style_profile(profile: dict[str, str]) -> str:
    if not profile:
        return ""
    lines = [f"- {key}: {value}" for key, value in profile.items()]
    return "STABLE_STYLE_PROFILE:\n" + "\n".join(lines)
