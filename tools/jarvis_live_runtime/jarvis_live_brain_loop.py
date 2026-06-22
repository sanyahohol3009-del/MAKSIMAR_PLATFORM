from __future__ import annotations

import json
import os
import re
import subprocess
import time
import asyncio
import ast
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import httpx

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_read_model,
    select_jarvis_live_model_role,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader import (
    run_jarvis_history_query,
)
from MAKSIMAR_CORE_LIB.memory_engine.memory_accessor import list_memory_definitions
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_CORE_LIB.runtime_activation import (
    build_default_capability_activation_matrix,
)

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_backend_status_read_model,
    build_retrieval_readonly_tool_route,
    build_retrieval_runtime_readonly_availability,
    build_retrieval_tool_enablement_policy,
    build_retrieval_tool_registry_contract,
    classify_retrieval_semantic_intent,
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_read_only_routing_integration import (
    build_mempalace_read_only_routing_integration_preview,
)

from tools.jarvis_live_runtime.jarvis_live_response_mode import (
    build_ollama_options,
    classify_response_mode,
)
from tools.jarvis_live_runtime.voice_response_cleaner import (
    clean_voice_response,
    contains_forbidden_generic_tail,
)
from tools.jarvis_live_runtime.ollama_transport import (
    BASE_HEAVY_CODER_MODEL_ID,
    DEFAULT_OLLAMA_MODEL_ID,
    FALLBACK_OLLAMA_MODEL_ID,
    HEAVY_CODER_MODEL_ID,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_URL,
    OLLAMA_FAST_CHAT_KEEP_ALIVE,
    OLLAMA_FAST_CHAT_NUM_PREDICT,
    OLLAMA_FAST_CHAT_TEMPERATURE,
    OLLAMA_FAST_CHAT_THINK,
    OLLAMA_FAST_CHAT_TOP_P,
    OLLAMA_URL,
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_get_json as _ollama_get_json,
    ollama_post_json as _ollama_post_json,
    timeout_policy_for_model_role,
)
from tools.jarvis_live_runtime.ollama_streaming import (
    _collect_chat_stream_events,
    _collect_generate_stream_events,
    _ollama_transport_plan,
    _parse_ollama_chat_stream_event,
    _split_chat_prompt,
    _stream_ollama_chat_model,
    _stream_ollama_generate_model,
    _stream_ollama_model,
)
from tools.jarvis_live_runtime.project_workspace_tools import (
    _domain_groups_for_paths,
    _important_paths_detected,
    _is_excluded_project_path,
    _is_safe_project_text_path,
    _project_tree_summary,
    _read_project_file_snippet,
    _repo_search_with_python,
    _repo_search_with_rg,
    _safe_project_path,
    _select_project_files_for_context,
    _top_level_entries_from_tracked_files,
    _tracked_project_files,
    read_file_outline,
    read_file_snippet,
    repo_files,
    repo_git_status,
    repo_import_graph,
    repo_search,
    repo_tree,
)
from tools.jarvis_live_runtime.session_memory_store import (
    SESSION_MEMORY_ROOT,
    SESSION_STATE_PATH,
    SESSION_TURN_LOG_NAME,
    _append_assistant_and_summarize,
    _append_local_chat_memory_record,
    _append_turn,
    _brief_turn_summary,
    _build_rolling_summary,
    _day_bucket,
    _detect_active_task,
    _empty_session_state,
    _extract_active_topics,
    _extract_style_preference,
    _format_style_profile,
    _format_turns,
    _load_session_state,
    _memory_enablement_flags,
    _memory_truth_contract,
    _normalize_session_state,
    _read_recent_local_chat_records,
    _save_session_state,
    _session_turn_log_path,
    _stable_style_profile_from_state,
    _timestamp,
    _update_style_preferences,
)
from tools.jarvis_live_runtime.memory_context_sources import (
    _asks_memory_recall,
    _asks_style_memory_recall,
    _build_memory_surface_inventory,
    _has_stored_memory_for_recall,
    _mempalace_status,
    _memory_query_terms,
    _needs_deep_memory,
    _needs_project_visibility,
    _retrieve_enterprise_memory_snippets,
    _retrieve_history_snippets,
    _retrieve_local_chat_memory_snippets,
    _retrieve_mempalace_status_snippets,
    _retrieve_memory_engine_snippets,
    _retrieve_project_workspace_snippets,
    _retrieve_regulatory_memory_snippets,
    _retrieve_vector_memory_snippets,
)
from tools.jarvis_live_runtime.memory_context_builder import (
    JarvisBrainContext,
    build_jarvis_live_brain_context,
    _retrieve_memory_federation_snippets,
)
from tools.jarvis_live_runtime.read_only_tool_router import (
    _asks_action_request,
    _asks_activation_matrix_question,
    _asks_memory_history_question,
    _asks_model_status_question,
    _asks_project_search_question,
    _asks_project_status_question,
    _asks_project_structure_question,
    _asks_roadmap_status_question,
    _asks_safety_status_question,
    _asks_tool_catalog_question,
    _build_read_only_tool_plan,
    _extract_filename_token,
    _extract_requested_file_path,
    _has_backend_status_guard,
    _has_filename_lookup_guard,
    _has_semantic_similarity_guard,
)
from tools.jarvis_live_runtime.jarvis_live_read_models import (
    _compact_json,
    _project_status_summary,
    _run_optional_read_only_command,
    _run_read_only_command,
    build_jarvis_live_memory_federation_status,
    build_jarvis_live_project_status_read_model,
    build_jarvis_live_tool_catalog_read_model,
    build_project_workspace_read_model,
    model_runtime_status,
    status_tools,
)
from tools.jarvis_live_runtime.jarvis_live_guarded_answer_engine import (
    _answer_conversation_style_complaint_if_grounded,
    _answer_style_memory_recall_if_grounded,
    _asks_casual_state_question,
    _asks_pc_action,
    _asks_permanent_memory_write,
    _asks_template_style_complaint,
    _asks_weather_or_current_facts,
    _is_forbidden_chat_template_response,
    _looks_like_keyboard_layout_noise,
    _repair_forbidden_chat_template_response,
)
from tools.jarvis_live_runtime.jarvis_live_project_answer_engine import (
    _answer_project_read_tool_request,
    _answer_project_workspace_summary_if_grounded,
    _answer_with_read_only_tools_if_grounded,
    _csv,
    _extract_semantic_similarity_query,
    _format_action_request_proposal_answer,
    _format_auto_tool_use_status_answer,
    _format_dirty_answer,
    _format_file_answer,
    _format_files_answer,
    _format_imports_answer,
    _format_list,
    _format_memory_history_grounded_answer,
    _format_outline_answer,
    _format_project_atlas_answer,
    _format_project_models_answer,
    _format_project_semantic_search_answer,
    _format_project_status_answer,
    _format_project_structure_grounded_answer,
    _format_retrieval_backend_status_answer,
    _format_retrieval_container_status_answer,
    _format_retrieval_vendor_status_answer,
    _format_roadmap_answer,
    _format_safety_answer,
    _format_search_answer,
    _format_section,
    _format_semantic_similarity_answer,
    _format_source_evidence_answer,
    _format_tests_answer,
    _format_tool_catalog_answer,
    _format_tree_answer,
    _parse_int,
    _plan_tool_route,
    _project_path_matches,
    _query_tokens,
    _semantic_search_query,
)
from tools.jarvis_live_runtime.jarvis_live_request_planner import (
    _is_deep_code_request,
    _is_simple_code_request,
    _needs_project_status,
    _plan_jarvis_request,
    _route_mode,
)
from tools.jarvis_live_runtime.jarvis_live_stream_events import (
    _build_admission_status,
    _candidate_model_ids_for_context,
    _command_error_payload,
    _command_timeout_seconds,
    _event,
    _filter_reasoning_chunk,
    _sanitize_model_output,
    _sentence_chunks,
    write_stream_event_safely,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
SESSION_MEMORY_ROOT = RUNTIME_ROOT / "session_memory"
SESSION_STATE_PATH = SESSION_MEMORY_ROOT / "jarvis_live_session_state.json"
SESSION_TURN_LOG_NAME = "jarvis_live_terminal_turns.jsonl"
RUNTIME_HISTORY_STORE = PROJECT_ROOT / "runtime_history_store"
RUNTIME_VECTOR_INDEX_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_vector_indexes"
RUNTIME_EMBEDDINGS_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_embeddings"
RUNTIME_RETRIEVAL_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_retrieval"
MAX_RECENT_TURNS = 4
MAX_LOCAL_CHAT_MEMORY_SNIPPETS = 4
MAX_PROJECT_TREE_ENTRIES = 80
MAX_PROJECT_FILE_SNIPPETS = 6
MAX_PROJECT_FILE_BYTES = 1800
PROJECT_FILES_PAGE_SIZE = 80
PROJECT_TREE_MAX_ENTRIES = 300
PROJECT_FILE_PAGE_LINES = 120
PROJECT_FILE_MAX_BYTES = 12000
PROJECT_SEARCH_MAX_RESULTS = 40
PROJECT_SEARCH_CONTEXT_LINES = 2
PROJECT_IMPORT_MAX_EDGES = 80
DEFAULT_TERMINAL_RESPONSE_MAX_CHARS = 131072
DEFAULT_GROUNDED_RESPONSE_MAX_CHARS = 262144


PROJECT_VISIBILITY_EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

PROJECT_VISIBILITY_KEY_FILES = (
    "CONTROL_PLANE/api_server.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py",
    "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py",
    "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py",
    "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
    "tools/jarvis_live_runtime/jarvis_personality_policy.py",
    "tools/jarvis_live_runtime/jarvis_live_response_mode.py",
    "tools/project_readiness_control/jarvis_live_ci_status.py",
    "tools/roadmap_post_step_drift_check.py",
)


STABLE_STYLE_PROFILE = {
    "user_name": "Александр",
    "assistant_identity": "JARVIS",
    "relation_style": "брат / напарник по гаражу",
    "communication_style": "natural, direct, practical, not overly short, not template-like",
    "avoid": "не повторять 'Нужна помощь?' после каждого ответа; не начинать отношения заново в новой сессии",
    "concise_rule": "быть коротким только когда владелец просит коротко; иначе отвечать достаточно полно для задачи",
}


def _apply_terminal_output_policy(response_text: str, *, grounded_answer: bool) -> tuple[str, bool, str]:
    text = str(response_text or "")
    limit = DEFAULT_GROUNDED_RESPONSE_MAX_CHARS if grounded_answer else DEFAULT_TERMINAL_RESPONSE_MAX_CHARS
    if len(text) <= limit:
        return text, False, ""
    marker = "[output_truncated=true reason=terminal_response_size_cap next_action=ask_continue]"
    trimmed = text[:limit].rstrip()
    if not trimmed.endswith("\n"):
        trimmed += "\n"
    return trimmed + marker, True, "terminal_response_size_cap"

FORBIDDEN_CHAT_TEMPLATE_MARKERS = (
    "долго не общались",
    "голова немного затуманилась",
    "что нужно сделать",
    "чем могу помочь",
    "нужна помощь",
    "готов помочь",
    "скажи, что нужно",
)


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
    "cross_tenant_retrieval_allowed": False,
    "cross_tenant_merge_allowed": False,
    "cross_jurisdiction_merge_allowed": False,
    "auto_routing_merge_allowed": False,
    "approval_bypass_allowed": False,
    "self_expansion_apply_allowed": False,
    "pc_control_enabled": False,
    "shell_execution_enabled": False,
    "dashboard_execution_allowed": False,
    "auto_project_truth_write": False,
    "direct_global_memory_write": False,
    "unsafe_auto_learning": False,
    "weight_finetune_from_chat": False,
    "auto_sync_without_policy": False,
}




def run_jarvis_live_brain_once(
    user_text: str,
    session_id: str = "default",
    command_timeout_seconds: float | None = None,
) -> dict[str, Any]:
    chunks: list[str] = []
    final_payload: dict[str, Any] = {}
    selected_model_role = select_jarvis_live_model_role(user_text)
    timeout_seconds = _command_timeout_seconds(
        command_timeout_seconds,
        str(selected_model_role.get("selected_model_role", "jarvis_chat_model")),
    )
    started_at = time.monotonic()
    try:
        for event in stream_jarvis_live_brain_response(
            user_text,
            session_id=session_id,
            ollama_timeout_seconds=timeout_seconds,
        ):
            if time.monotonic() - started_at > timeout_seconds:
                final_payload = _command_error_payload(user_text, "command_timeout")
                break
            if event["event"] == "chunk":
                chunks.append(str(event["text"]))
            if event["event"] == "done":
                final_payload = dict(event)
    except (TimeoutError, asyncio.CancelledError):
        final_payload = _command_error_payload(user_text, "command_timeout_or_cancelled")
    except KeyboardInterrupt:
        final_payload = _command_error_payload(user_text, "command_cancelled_by_operator")
    except Exception:
        final_payload = _command_error_payload(user_text, "command_runtime_error")
    if not final_payload:
        final_payload = {
            "event": "done",
            "response_text": _sanitize_model_output("".join(chunks)).strip(),
            "ollama_model_used": "",
            "pc_control_allowed": False,
            "output_truncated": False,
            "output_truncation_reason": "",
        }
    response_text, output_truncated, output_truncation_reason = _apply_terminal_output_policy(
        str(final_payload.get("response_text", "")).strip(),
        grounded_answer=bool(final_payload.get("grounded_answer", False)),
    )
    if not response_text:
        response_text = "Модельный runtime сейчас не вернул ответ. Повтори запрос или проверь Ollama статус."
    return {
        "llm_response": response_text,
        "ollama_model_used": str(final_payload.get("ollama_model_used", "")),
        "route_mode": str(final_payload.get("route_mode", "")),
        "thinking_chunk_count": int(final_payload.get("thinking_chunk_count", 0)),
        "answer_chunk_count": int(final_payload.get("answer_chunk_count", len(chunks))),
        "stream_chunk_count": int(final_payload.get("stream_chunk_count", len(chunks))),
        "had_thinking": bool(final_payload.get("had_thinking", False)),
        "selected_model_role": str(final_payload.get("selected_model_role", "")),
        "selected_model_id": str(final_payload.get("selected_model_id", "")),
        "selected_model_status": str(final_payload.get("selected_model_status", "")),
        "admission_allowed": bool(final_payload.get("admission_allowed", False)),
        "resource_gate_surface": str(final_payload.get("resource_gate_surface", "")),
        "session_memory_path": str(final_payload.get("session_memory_path", SESSION_STATE_PATH)),
        "local_chat_memory_path": str(final_payload.get("local_chat_memory_path", _session_turn_log_path())),
        "runtime_history_store_path": str(
            final_payload.get("runtime_history_store_path", RUNTIME_HISTORY_STORE)
        ),
        "runtime_history_store_exists": bool(
            final_payload.get("runtime_history_store_exists", RUNTIME_HISTORY_STORE.exists())
        ),
        "retrieved_snippet_count": int(final_payload.get("retrieved_snippet_count", 0)),
        "local_chat_memory_snippet_count": int(final_payload.get("local_chat_memory_snippet_count", 0)),
        "retrieval_surfaces_used": tuple(final_payload.get("retrieval_surfaces_used", ())),
        "memory_truth_contract": dict(final_payload.get("memory_truth_contract", _memory_truth_contract())),
        "dangerous_mutation_flags": dict(final_payload.get("dangerous_mutation_flags", DANGEROUS_MEMORY_FLAGS)),
        "memory_federation_available": bool(final_payload.get("memory_federation_available", False)),
        "mempalace_status": str(final_payload.get("mempalace_status", "not_detected")),
        "error_kind": str(final_payload.get("error_kind", "")),
        "error_message": str(final_payload.get("error_message", "")),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "intent_family": final_payload.get("intent_family"),
        "selected_tools": tuple(final_payload.get("selected_tools", ())),
        "read_only": bool(final_payload.get("read_only", False)),
        "execution_allowed": bool(final_payload.get("execution_allowed", False)),
        "evidence_required": bool(final_payload.get("evidence_required", False)),
        "evidence_count": int(final_payload.get("evidence_count", 0)),
        "ollama_called": final_payload.get("ollama_called"),
        "output_truncated": bool(final_payload.get("output_truncated", output_truncated)),
        "output_truncation_reason": str(final_payload.get("output_truncation_reason", output_truncation_reason)),
    }


def stream_jarvis_live_brain_response(
    user_text: str,
    session_id: str = "default",
    ollama_timeout_seconds: float | None = None,
) -> Iterator[dict[str, Any]]:
    clean_text = user_text.strip()
    if not clean_text:
        yield _event("done", response_text="", route_mode="ignored")
        return

    stream_started_at = time.monotonic()
    request_plan = _plan_jarvis_request(clean_text)
    selected_model_role = select_jarvis_live_model_role(clean_text)
    memory_status = build_jarvis_live_memory_federation_status()
    yield {
        **_event("start"),
        "status": "accepted",
        "request_route": request_plan["request_route"],
        "route_mode": request_plan["route_mode"],
        "retrieval_mode": request_plan["retrieval_mode"],
        "selected_model_role": selected_model_role["selected_model_role"],
        "selected_model_id": selected_model_role["model_id"],
        "selected_model_status": selected_model_role["status"],
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "retrieved_snippet_count": 0,
        "retrieval_surfaces_used": ("session_memory",),
        "memory_federation_available": memory_status["memory_federation_available"],
        "mempalace_status": memory_status["mempalace_status"],
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }

    context_started_at = time.monotonic()
    SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
    state = _load_session_state()
    _update_style_preferences(state, clean_text)
    _append_turn(state, "user", clean_text)
    context = build_jarvis_live_brain_context(
        clean_text,
        state,
        request_plan=request_plan,
        session_id=session_id,
    )
    transport_plan = _ollama_transport_plan(context.route_mode, context.to_prompt(), clean_text)
    read_only_tool_plan = _build_read_only_tool_plan(clean_text, context)
    timeout_policy = timeout_policy_for_model_role(context.selected_model_role["selected_model_role"])
    effective_ollama_timeout_seconds = (
        float(ollama_timeout_seconds)
        if ollama_timeout_seconds is not None and ollama_timeout_seconds > 0
        else float(timeout_policy["total_request_timeout_seconds"])
    )
    _save_session_state(state)
    context_elapsed_seconds = round(time.monotonic() - context_started_at, 4)

    yield {
        **_event("route_selected"),
        "route_mode": context.route_mode,
        "request_route": context.request_route,
        "retrieval_mode": context.retrieval_mode,
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "selected_model_id": context.selected_model_role["model_id"],
        "selected_model_status": context.selected_model_role["status"],
        "admission_allowed": context.admission_status["admission_allowed"],
        "resource_gate_surface": context.admission_status["resource_gate_surface"],
        "retrieved_snippet_count": len(context.retrieved_snippets),
        "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
        "retrieval_surfaces_used": context.retrieval_surfaces_used,
        "memory_federation_available": context.memory_federation_status["memory_federation_available"],
        "mempalace_status": context.memory_federation_status["mempalace_status"],
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "ollama_endpoint": transport_plan["primary_endpoint"],
        "primary_endpoint": transport_plan["primary_endpoint"],
        "fallback_endpoint": transport_plan["fallback_endpoint"],
        "ollama_endpoint_fallback_used": False,
        "think_mode": transport_plan["think_mode"],
        "ollama_num_predict": transport_plan["ollama_num_predict"],
        "ollama_temperature": transport_plan["ollama_temperature"],
        "ollama_top_p": transport_plan["ollama_top_p"],
        "context_elapsed_seconds": context_elapsed_seconds,
        "intent_family": read_only_tool_plan["intent_family"],
        "selected_tools": read_only_tool_plan["selected_tools"],
        "read_only": read_only_tool_plan["read_only"],
        "execution_allowed": read_only_tool_plan["execution_allowed"],
        "evidence_required": read_only_tool_plan["evidence_required"],
        "grounded_answer": False,
        "ollama_called": False,
        "evidence_count": 0,
        "timeout_policy": timeout_policy,
        "helper_model_status": context.orchestration_decision.get("helper_model_status", ""),
        "helper_model_called": context.orchestration_decision.get("helper_model_called", False),
        "helper_model_used": context.orchestration_decision.get("helper_model_used", False),
        "helper_model_id": context.orchestration_decision.get("helper_model_id", ""),
        "helper_decision_confidence": context.orchestration_decision.get("helper_decision_confidence", 0.0),
        "selection_source": context.orchestration_decision.get("selection_source", ""),
        "fallback_used": context.orchestration_decision.get("fallback_used", False),
    }
    if read_only_tool_plan["intent_family"] != "CONVERSATION":
        yield {
            **_event("operator_trace"),
            "intent_family": read_only_tool_plan["intent_family"],
            "selected_tools": read_only_tool_plan["selected_tools"],
            "reason": read_only_tool_plan["reason"],
            "read_only": read_only_tool_plan["read_only"],
            "execution_allowed": read_only_tool_plan["execution_allowed"],
            "evidence_required": read_only_tool_plan["evidence_required"],
            "ollama_called": False,
            "pc_control_allowed": False,
            "canonical_memory_write_allowed": False,
        }

    guarded_response = _guarded_local_response(clean_text, context, read_only_tool_plan)
    if guarded_response is not None:
        sanitized_guarded_response = _sanitize_model_output(guarded_response)
        sanitized_guarded_response, output_truncated, output_truncation_reason = _apply_terminal_output_policy(
            sanitized_guarded_response,
            grounded_answer=True,
        )
        for chunk in _sentence_chunks(sanitized_guarded_response):
            yield _event("chunk", text=chunk, route_mode=context.route_mode)
        _append_assistant_and_summarize(state, sanitized_guarded_response, context)
        yield {
            **_event("done", response_text=sanitized_guarded_response, route_mode=context.route_mode),
            "request_route": context.request_route,
            "retrieval_mode": context.retrieval_mode,
            "ollama_model_used": "",
            "thinking_chunk_count": 0,
            "answer_chunk_count": len(tuple(_sentence_chunks(sanitized_guarded_response))),
            "stream_chunk_count": len(tuple(_sentence_chunks(sanitized_guarded_response))),
            "had_thinking": False,
            "retrieved_snippet_count": len(context.retrieved_snippets),
            "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
            "retrieval_surfaces_used": context.retrieval_surfaces_used,
            "memory_federation_available": context.memory_federation_status["memory_federation_available"],
            "mempalace_status": context.memory_federation_status["mempalace_status"],
            "selected_model_role": context.selected_model_role["selected_model_role"],
            "selected_model_id": context.selected_model_role["model_id"],
            "selected_model_status": context.selected_model_role["status"],
            "admission_allowed": context.admission_status["admission_allowed"],
            "resource_gate_surface": context.admission_status["resource_gate_surface"],
            "session_memory_path": str(SESSION_STATE_PATH),
            "local_chat_memory_path": str(_session_turn_log_path()),
            "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
            "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
            "memory_truth_contract": _memory_truth_contract(),
            "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
            "canonical_memory_write_allowed": False,
            "pc_control_allowed": False,
            "context_elapsed_seconds": context_elapsed_seconds,
            "total_elapsed_seconds": round(time.monotonic() - stream_started_at, 4),
            "intent_family": read_only_tool_plan["intent_family"],
            "selected_tools": read_only_tool_plan["selected_tools"],
            "read_only": read_only_tool_plan["read_only"],
            "execution_allowed": read_only_tool_plan["execution_allowed"],
            "evidence_required": read_only_tool_plan["evidence_required"],
            "evidence_count": read_only_tool_plan.get("evidence_count", 0),
            "grounded_answer": True,
            "ollama_called": False,
            "output_truncated": output_truncated,
            "output_truncation_reason": output_truncation_reason,
        }
        return

    chunks: list[str] = []
    thinking_chunks: list[str] = []
    errors: list[dict[str, Any]] = []
    model_used = ""
    empty_model_id = ""
    completion_event: dict[str, Any] = {}
    first_chunk_elapsed_seconds = 0.0
    ollama_started_at = time.monotonic()
    for model_id in _candidate_model_ids_for_context(context):
        streamed = False
        reasoning_state = {"inside_reasoning": False}
        for event in _stream_ollama_model(
            model_id,
            context.to_prompt(),
            context.route_mode,
            timeout_seconds=effective_ollama_timeout_seconds,
            response_mode_text=clean_text,
        ):
            streamed = True
            if event["event"] == "thinking":
                thinking_text = str(event.get("text", ""))
                if thinking_text:
                    thinking_chunks.append(thinking_text)
                    yield event
            elif event["event"] == "chunk":
                visible_text = _filter_reasoning_chunk(str(event["text"]), reasoning_state)
                if visible_text:
                    if not chunks:
                        first_chunk_elapsed_seconds = round(time.monotonic() - stream_started_at, 4)
                    chunks.append(visible_text)
                    yield {**event, "text": visible_text}
            elif event["event"] == "tool_call":
                yield event
            elif event["event"] == "done":
                completion_event = dict(event)
                model_used = model_id
                if not chunks:
                    empty_model_id = model_id
                break
            elif event["event"] == "error":
                error_event = {
                    **event,
                    "error_kind": "ollama_stream_error",
                    "selected_model_role": context.selected_model_role["selected_model_role"],
                    "selected_model_id": context.selected_model_role["model_id"],
                }
                errors.append(error_event)
                yield error_event
        if streamed and chunks:
            break

    response_text = _sanitize_model_output("".join(chunks)).strip()
    error_kind = ""
    error_message = ""
    if not response_text and errors:
        error_kind = str(errors[-1].get("error_kind", "ollama_stream_error"))
        error_message = str(errors[-1].get("error_message", "ollama stream returned an error"))
        response_text = "Модельный runtime сейчас не вернул ответ. Проверь Ollama статус и выбранный wrapper."
    elif not response_text and int(completion_event.get("tool_call_count", 0)) > 0:
        response_text = "Модель вернула tool_call proposal; execution_allowed=false; approval_required=true."
    elif not response_text and thinking_chunks:
        error_kind = "ollama_thinking_without_final_response"
        error_message = "model produced thinking but no final response; increase num_predict or disable thinking."
    elif not response_text:
        error_kind = "ollama_empty_response"
        model_for_error = empty_model_id or model_used or context.selected_model_role["model_id"]
        error_message = f"ollama_empty_response model={model_for_error}"
    if _is_forbidden_chat_template_response(response_text):
        response_text = _repair_forbidden_chat_template_response(context)
        error_kind = "template_response_filtered"
        error_message = "model returned a repeated generic chat template; local guard replaced it"
    response_text, output_truncated, output_truncation_reason = _apply_terminal_output_policy(
        response_text,
        grounded_answer=False,
    )
    _append_assistant_and_summarize(state, response_text, context)
    yield {
        **_event("done", response_text=response_text, route_mode=context.route_mode),
        **completion_event,
        "request_route": context.request_route,
        "retrieval_mode": context.retrieval_mode,
        "ollama_model_used": model_used,
        "thinking_chunk_count": len(thinking_chunks),
        "answer_chunk_count": len(chunks),
        "stream_chunk_count": len(thinking_chunks) + len(chunks) + int(completion_event.get("tool_call_count", 0)),
        "had_thinking": bool(thinking_chunks),
        "tool_call_detected": bool(completion_event.get("tool_call_detected", False)),
        "tool_call_count": int(completion_event.get("tool_call_count", 0)),
        "had_tool_call": bool(completion_event.get("tool_call_count", 0)),
        "retrieved_snippet_count": len(context.retrieved_snippets),
        "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
        "retrieval_surfaces_used": context.retrieval_surfaces_used,
        "memory_federation_available": context.memory_federation_status["memory_federation_available"],
        "mempalace_status": context.memory_federation_status["mempalace_status"],
        "ollama_endpoint": str(completion_event.get("ollama_endpoint", "")),
        "primary_endpoint": str(completion_event.get("primary_endpoint", "")),
        "fallback_endpoint": str(completion_event.get("fallback_endpoint", "")),
        "ollama_endpoint_fallback_used": bool(completion_event.get("ollama_endpoint_fallback_used", False)),
        "think_mode": str(completion_event.get("think_mode", "")),
        "ollama_num_predict": completion_event.get("ollama_num_predict", 0),
        "ollama_temperature": completion_event.get("ollama_temperature", 0.0),
        "ollama_top_p": completion_event.get("ollama_top_p", 0.0),
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "selected_model_id": context.selected_model_role["model_id"],
        "selected_model_status": context.selected_model_role["status"],
        "error_kind": error_kind,
        "error_message": error_message,
        "template_guard_triggered": error_kind == "template_response_filtered",
        "admission_allowed": context.admission_status["admission_allowed"],
        "resource_gate_surface": context.admission_status["resource_gate_surface"],
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "memory_truth_contract": _memory_truth_contract(),
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "context_elapsed_seconds": context_elapsed_seconds,
        "ollama_elapsed_seconds": round(time.monotonic() - ollama_started_at, 4),
        "first_chunk_elapsed_seconds": first_chunk_elapsed_seconds,
        "total_elapsed_seconds": round(time.monotonic() - stream_started_at, 4),
        "intent_family": read_only_tool_plan["intent_family"],
        "selected_tools": read_only_tool_plan["selected_tools"],
        "read_only": read_only_tool_plan["read_only"],
        "execution_allowed": read_only_tool_plan["execution_allowed"],
        "evidence_required": read_only_tool_plan["evidence_required"],
        "evidence_count": read_only_tool_plan.get("evidence_count", len(context.retrieved_snippets)),
        "grounded_answer": False,
        "ollama_called": True,
        "output_truncated": output_truncated,
        "output_truncation_reason": output_truncation_reason,
    }




def build_jarvis_live_brain_health() -> dict[str, Any]:
    state = _load_session_state()
    return {
        "status": "ready",
        "ollama_url": OLLAMA_URL,
        "default_model": PRIMARY_CONVERSATION_MODEL_ID,
        "primary_conversation_model": PRIMARY_CONVERSATION_MODEL_ID,
        "fallback_model": FALLBACK_OLLAMA_MODEL_ID,
        "heavy_coder_model": HEAVY_CODER_MODEL_ID,
        "session_memory_path": str(SESSION_STATE_PATH),
        "session_memory_exists": SESSION_STATE_PATH.exists(),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "local_chat_memory_exists": _session_turn_log_path().exists(),
        "stable_style_profile": _stable_style_profile_from_state(state),
        "memory_truth_contract": _memory_truth_contract(),
        "append_only_local_chat_write_enabled": True,
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "recent_turn_count": len(state.get("recent_turns", [])),
        "model_role_profile_map": build_jarvis_live_runtime_model_role_read_model(),
        "default_model": PRIMARY_CONVERSATION_MODEL_ID,
        "primary_conversation_model": PRIMARY_CONVERSATION_MODEL_ID,
        "fallback_model": FALLBACK_OLLAMA_MODEL_ID,
        "heavy_coder_model": HEAVY_CODER_MODEL_ID,
        "memory_federation": build_jarvis_live_memory_federation_status(),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "pc_control_allowed": False,
        "canonical_memory_write_allowed": False,
    }


def build_jarvis_live_session_status() -> dict[str, Any]:
    state = _load_session_state()
    return {
        "recent_turn_count": len(state.get("recent_turns", [])),
        "rolling_summary": str(state.get("rolling_summary", "")),
        "active_topics": tuple(state.get("active_topics", [])),
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "local_chat_memory_exists": _session_turn_log_path().exists(),
        "stable_style_profile": _stable_style_profile_from_state(state),
        "memory_truth_contract": _memory_truth_contract(),
        "append_only_local_chat_write_enabled": True,
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "local_session_persistence": bool(state.get("local_session_persistence", True)),
        "model_role_profile_map": build_jarvis_live_runtime_model_role_read_model(),
        "memory_federation": build_jarvis_live_memory_federation_status(),
        "pc_control_allowed": False,
        "canonical_memory_write_allowed": False,
    }


def reset_jarvis_live_session() -> dict[str, Any]:
    state = _empty_session_state()
    _save_session_state(state)
    return build_jarvis_live_session_status()


































































def _format_activation_matrix_answer() -> str:
    matrix = build_default_capability_activation_matrix().to_read_model()
    entries = matrix["entries"]
    by_id = {str(entry["capability_id"]): entry for entry in entries}

    important_ids = (
        "voice_perception",
        "windows_voice_edge_runtime",
        "push_to_talk_stt_live",
        "mobile_on_device_ai",
        "android_junior_model",
        "ios_junior_model",
        "runtime_history_store",
        "retrieval_readonly_tools",
        "mgrep_readonly",
        "sqlite_vec_readonly",
        "qdrant_readonly_status",
        "ollama_local_engine",
        "approval_gates",
        "network_sync_gates",
        "pc_control_candidates",
    )

    lines = [
        "Activation Matrix: read_only=true; direct_execution_allowed=false; canonical_write_allowed=false; pc_control_allowed=false; phone_control_allowed=false; deployment_allowed=false.",
        "JARVIS остаётся senior/canonical authority. Android/iOS junior существуют как subordinate app-safe nodes, не как второй JARVIS.",
    ]

    for capability_id in important_ids:
        entry = by_id.get(capability_id)
        if not entry:
            continue
        lines.append(
            f"- {capability_id}: {entry['activation_level']}; "
            f"present={str(entry['capability_present']).lower()}; "
            f"contract_valid={str(entry['contract_valid']).lower()}; "
            f"dependency_installed={str(entry['dependency_installed']).lower()}; "
            f"model_present={str(entry['model_present']).lower()}; "
            f"runtime_configured={str(entry['runtime_configured']).lower()}; "
            f"smoke_passed={str(entry['smoke_passed']).lower()}; "
            f"operator_enabled={str(entry['operator_enabled']).lower()}; "
            f"policy_allowed={str(entry['policy_allowed']).lower()}; "
            f"runtime_started={str(entry['runtime_started']).lower()}; "
            f"blocked_reason={entry['blocked_reason']}; "
            f"next={entry['next_required_action']}"
        )

    return "\n".join(lines)


def _guarded_local_response(
    user_text: str,
    context: JarvisBrainContext,
    read_only_tool_plan: dict[str, Any] | None = None,
) -> str | None:
    lowered = user_text.casefold()
    conversation_style_answer = _answer_conversation_style_complaint_if_grounded(context)
    if conversation_style_answer:
        return conversation_style_answer
    style_memory_answer = _answer_style_memory_recall_if_grounded(context)
    if style_memory_answer:
        return style_memory_answer
    grounded_tool_answer = _answer_with_read_only_tools_if_grounded(
        user_text,
        context,
        read_only_tool_plan or _build_read_only_tool_plan(user_text, context),
    )
    if grounded_tool_answer:
        return grounded_tool_answer
    project_tool_answer = _answer_project_read_tool_request(user_text)
    if project_tool_answer:
        return project_tool_answer
    project_workspace_answer = _answer_project_workspace_summary_if_grounded(context)
    if project_workspace_answer:
        return project_workspace_answer
    if _asks_memory_recall(lowered) and not _has_stored_memory_for_recall(context):
        return (
            "Не буду выдумывать память: в local_chat_memory/session_summary нет сохранённой записи по этому запросу. "
            "Могу продолжить с текущего сообщения или сохранить новый факт в локальную session memory."
        )
    if _asks_permanent_memory_write(lowered):
        return "Прямая запись в постоянную/canonical память выключена: canonical_memory_write_allowed=false. Нужен ingestion proposal, review и approval перед синхронизацией."
    if _asks_weather_or_current_facts(lowered):
        return "Для погоды или текущих фактов нужен внешний инструмент. Сейчас этот tool недоступен, поэтому я не буду выдумывать ответ."
    if _asks_pc_action(lowered):
        return "Прямое управление ПК выключено: pc_control_allowed=false. Я могу подготовить план или proposal для approval/allowlist, но не буду выполнять действие."
    if "runtime_history_store" in lowered:
        exists = RUNTIME_HISTORY_STORE.exists()
        return f"Вижу runtime_history_store: путь {RUNTIME_HISTORY_STORE}, exists={str(exists).lower()}."
    if "что я спрашивал" in lowered or "до этого" in lowered:
        recent_user = [
            turn["text"]
            for turn in context.recent_turns
            if turn.get("role") == "user" and turn.get("text") != user_text
        ]
        if not recent_user:
            return "В текущей session memory пока нет предыдущих вопросов."
        return "До этого ты спрашивал: " + "; ".join(recent_user[-3:])
    if "что ты видишь по проекту" in lowered:
        return context.project_status or _project_status_summary()
    if "memory surfaces" in lowered or "memory surface" in lowered or "какие memory" in lowered or "какие памяти" in lowered:
        status = context.memory_federation_status
        return (
            "Вижу memory federation: active="
            + ", ".join(status["active_retrieval_surfaces"])
            + "; sandbox_only="
            + ", ".join(status["sandbox_only_memory_surfaces"])
            + "; disabled="
            + ", ".join(status["disabled_memory_surfaces"])
            + f"; mempalace_status={status['mempalace_status']}."
        )
    if "mempalace" in lowered:
        return (
            "MemPalace подключён только через существующую read-only/sandbox архитектуру: "
            f"mempalace_status={context.memory_federation_status['mempalace_status']}; "
            "canonical write и runtime mutation запрещены."
        )
    return None




















































































def _has_project_symbol_search_guard(lowered: str) -> bool:
    guarded_symbols = (
        "source_ref",
        "source-ref",
        "source ref",
        "evidence_binding",
        "evidence-binding",
        "evidence binding",
        "source_of_truth",
        "network_allowed_by_default",
        "runtime_mutation_allowed",
        "direct_execution_allowed",
        "vendor_gate_required",
    )
    return any(symbol in lowered for symbol in guarded_symbols)


















def _asks_safety_status_question(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "можешь управлять",
            "управлять пк",
            "можешь выполнить команду",
            "можешь выполнять команду",
            "выполнять команды",
            "выполнить команду",
            "команду на пк",
            "какие ограничения",
            "pc-control",
            "pc control",
            "shell",
            "безопас",
            "approval",
            "direct_execution",
            "execution_allowed",
        )
    )












































































































































def _compact_text(text: str, source: Path) -> str:
    single_line = " ".join(text.split())
    return f"{source}: {single_line[:700]}"












