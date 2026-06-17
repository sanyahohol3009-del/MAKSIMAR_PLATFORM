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

from tools.jarvis_live_runtime.jarvis_live_identity_prompt import (
    build_jarvis_live_identity_prompt,
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
    "tools/jarvis_live_runtime/jarvis_live_identity_prompt.py",
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


@dataclass(frozen=True)
class JarvisBrainContext:
    session_id: str
    user_text: str
    request_route: str
    route_mode: str
    retrieval_mode: str
    selected_model_role: dict[str, Any]
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
        return "\n".join(
            part
            for part in (
                _system_rules(short=True),
                build_jarvis_live_identity_prompt(self.user_text),
                _fast_final_answer_rules(),
                _format_style_profile(self.stable_style_profile),
                _format_style_memory_answer_rules(),
                _format_memory_truth_split(),
                _format_section("ROLLING_SESSION_SUMMARY", self.rolling_summary),
                _format_turns(self.recent_turns[-4:]),
                _format_list("LOCAL_CHAT_MEMORY", self.local_chat_memory_snippets),
            )
            if part
        )

    def to_deep_system_prompt(self) -> str:
        return "\n".join(
            part
            for part in (
                _system_rules(short=False),
                build_jarvis_live_identity_prompt(self.user_text),
                _format_section("REQUEST_ROUTE", self.request_route),
                _format_section("RETRIEVAL_MODE", self.retrieval_mode),
                _format_section("MODEL_ROLE", self.selected_model_role["selected_model_role"]),
                _format_section("MODEL_ROUTE_REASON", self.selected_model_role["route_reason"]),
                _format_section("ROLLING_SESSION_SUMMARY", self.rolling_summary),
                _format_turns(self.recent_turns),
                _format_style_profile(self.stable_style_profile),
                _format_style_memory_answer_rules(),
                _format_memory_truth_split(),
                _format_list("LOCAL_CHAT_MEMORY", self.local_chat_memory_snippets),
                _format_list("ACTIVE_TOPICS", self.active_topics),
                _format_list("RETRIEVAL_SURFACES_USED", self.retrieval_surfaces_used),
                _format_list("RETRIEVED_LONG_TERM_MEMORY", self.retrieved_snippets),
                _format_section("PROJECT_STATUS_READ_ONLY", self.project_status),
            )
            if part
        )

    def to_prompt(self) -> str:
        if self.route_mode == "FAST" and self.retrieval_mode == "session_only":
            return "\n".join(part for part in (self.to_fast_system_prompt(), f"USER_MESSAGE: {self.user_text}") if part)
        return "\n".join(part for part in (self.to_deep_system_prompt(), f"USER_MESSAGE: {self.user_text}") if part)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "route_mode": self.route_mode,
            "session_id": self.session_id,
            "request_route": self.request_route,
            "retrieval_mode": self.retrieval_mode,
            "selected_model_role": self.selected_model_role,
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
            "memory_truth_split": _memory_truth_split(),
            "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        }


def run_jarvis_live_brain_once(
    user_text: str,
    session_id: str = "default",
    command_timeout_seconds: float | None = None,
) -> dict[str, Any]:
    chunks: list[str] = []
    final_payload: dict[str, Any] = {}
    timeout_seconds = _command_timeout_seconds(command_timeout_seconds)
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
        }
    response_text = str(final_payload.get("response_text", "")).strip()
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
        "memory_truth_split": dict(final_payload.get("memory_truth_split", _memory_truth_split())),
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
            "memory_truth_split": _memory_truth_split(),
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
            timeout_seconds=ollama_timeout_seconds,
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
        "memory_truth_split": _memory_truth_split(),
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
    }


def build_jarvis_live_brain_context(
    user_text: str,
    state: dict[str, Any] | None = None,
    request_plan: dict[str, str] | None = None,
    session_id: str = "default",
) -> JarvisBrainContext:
    state = _load_session_state() if state is None else state
    request_plan = _plan_jarvis_request(user_text) if request_plan is None else request_plan
    route_mode = request_plan["route_mode"]
    selected_model_role = select_jarvis_live_model_role(user_text)
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
        "memory_truth_split": _memory_truth_split(),
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
        "memory_truth_split": _memory_truth_split(),
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


def build_jarvis_live_project_status_read_model() -> dict[str, Any]:
    return {
        "project_status": _project_status_summary(),
        "read_only": True,
        "pc_control_allowed": False,
        "canonical_memory_write_allowed": False,
    }


def build_project_workspace_read_model() -> dict[str, Any]:
    git_status = repo_git_status()
    tracked = _tracked_project_files()
    return {
        "project_root": str(PROJECT_ROOT),
        "git_branch": git_status["branch"],
        "git_head": git_status["head"],
        "git_status_short": git_status["status_short"],
        "dirty_files": git_status["dirty_files"],
        "untracked_files": git_status["untracked_files"],
        "staged_files": git_status["staged_files"],
        "tracked_file_count": len(tracked),
        "tracked_files_by_page": repo_files(page=1, page_size=PROJECT_FILES_PAGE_SIZE),
        "top_level_tree": repo_tree(depth=2, max_entries=PROJECT_TREE_MAX_ENTRIES),
        "important_paths_detected_dynamically": _important_paths_detected(tracked),
        "domain_groups": _domain_groups_for_paths(tracked),
        "recent_test_status_if_available": "not_run_from_chat",
        "roadmap_status_if_available": status_tools().get("roadmap_post_step_drift_check", ""),
        "model_status_if_available": model_runtime_status(),
        "runtime_status_if_available": status_tools().get("jarvis_live_ci_status", ""),
        "read_only": True,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }


def repo_git_status() -> dict[str, Any]:
    status_short = _run_read_only_command(("git", "status", "--short"))
    parsed = _parse_git_status_short(status_short)
    return {
        "branch": _run_read_only_command(("git", "branch", "--show-current")),
        "head": _run_read_only_command(("git", "rev-parse", "HEAD")),
        "status_short": status_short,
        "dirty_files": parsed["dirty_files"],
        "untracked_files": parsed["untracked_files"],
        "staged_files": parsed["staged_files"],
        "diff_name_only": tuple(_run_read_only_command(("git", "diff", "--name-only")).splitlines()),
        "diff_stat": _run_read_only_command(("git", "diff", "--stat")),
        "read_only": True,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }


def repo_tree(depth: int = 2, max_entries: int = PROJECT_TREE_MAX_ENTRIES) -> dict[str, Any]:
    depth = max(1, min(int(depth), 5))
    max_entries = max(1, min(int(max_entries), PROJECT_TREE_MAX_ENTRIES))
    entries: list[str] = []
    for path in _tracked_project_files():
        if _is_excluded_project_path(path):
            continue
        parts = Path(path).parts[:depth]
        if not parts:
            continue
        value = "/".join(parts) + ("/" if len(Path(path).parts) > len(parts) else "")
        if value not in entries:
            entries.append(value)
        if len(entries) >= max_entries:
            break
    return {"depth": depth, "entries": tuple(entries), "entry_count": len(entries), "read_only": True}


def repo_files(page: int = 1, page_size: int = PROJECT_FILES_PAGE_SIZE) -> dict[str, Any]:
    files = _tracked_project_files()
    page = max(1, int(page))
    page_size = max(1, min(int(page_size), PROJECT_FILES_PAGE_SIZE))
    start = (page - 1) * page_size
    end = start + page_size
    total_pages = (len(files) + page_size - 1) // page_size if files else 1
    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_files": len(files),
        "files": files[start:end],
        "read_only": True,
    }


def repo_search(query: str, paths: tuple[str, ...] | None = None, max_results: int = PROJECT_SEARCH_MAX_RESULTS) -> dict[str, Any]:
    query = query.strip()
    if not query:
        return {"query": query, "results": (), "result_count": 0, "read_only": True}
    max_results = max(1, min(int(max_results), PROJECT_SEARCH_MAX_RESULTS))
    search_paths = tuple(path for path in (paths or ()) if _safe_project_path(path))
    results = _repo_search_with_rg(query, search_paths, max_results)
    if not results:
        results = _repo_search_with_python(query, search_paths, max_results)
    return {"query": query, "results": tuple(results[:max_results]), "result_count": len(results[:max_results]), "read_only": True}


def read_file_snippet(path: str, start_line: int = 1, end_line: int | None = None, page: int = 1) -> dict[str, Any]:
    if not _safe_project_path(path) or not _is_safe_project_text_path(path):
        return {"path": path, "allowed": False, "error": "path_denied", "read_only": True}
    full_path = PROJECT_ROOT / path
    if not full_path.exists() or not full_path.is_file():
        return {"path": path, "allowed": False, "error": "file_not_found", "read_only": True}
    page = max(1, int(page))
    if end_line is None:
        start_line = ((page - 1) * PROJECT_FILE_PAGE_LINES) + 1
        end_line = start_line + PROJECT_FILE_PAGE_LINES - 1
    start_line = max(1, int(start_line))
    end_line = max(start_line, min(int(end_line), start_line + PROJECT_FILE_PAGE_LINES - 1))
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")[:PROJECT_FILE_MAX_BYTES * max(1, page)]
    except OSError:
        return {"path": path, "allowed": False, "error": "read_failed", "read_only": True}
    lines = text.splitlines()
    selected = lines[start_line - 1:end_line]
    numbered = tuple(f"{idx}: {line}" for idx, line in enumerate(selected, start=start_line))
    return {
        "path": path,
        "allowed": True,
        "page": page,
        "start_line": start_line,
        "end_line": min(end_line, len(lines)),
        "line_count": len(lines),
        "snippet": numbered,
        "read_only": True,
    }


def read_file_outline(path: str) -> dict[str, Any]:
    snippet = read_file_snippet(path, start_line=1, end_line=PROJECT_FILE_PAGE_LINES, page=1)
    if not snippet.get("allowed"):
        return snippet
    full_path = PROJECT_ROOT / path
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"path": path, "allowed": False, "error": "read_failed", "read_only": True}
    imports: list[str] = []
    classes: list[str] = []
    functions: list[str] = []
    constants: list[str] = []
    if full_path.suffix == ".py":
        try:
            tree = ast.parse(text)
        except SyntaxError:
            tree = None
        if tree is not None:
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(("." * node.level) + str(node.module or ""))
                elif isinstance(node, ast.ClassDef):
                    classes.append(f"{node.name}:{node.lineno}")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append(f"{node.name}:{node.lineno}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constants.append(f"{target.id}:{node.lineno}")
    return {
        "path": path,
        "allowed": True,
        "line_count": len(text.splitlines()),
        "imports": tuple(imports[:40]),
        "classes": tuple(classes[:40]),
        "functions": tuple(functions[:80]),
        "constants": tuple(constants[:40]),
        "read_only": True,
    }


def repo_import_graph(path: str | None = None, max_edges: int = PROJECT_IMPORT_MAX_EDGES) -> dict[str, Any]:
    max_edges = max(1, min(int(max_edges), PROJECT_IMPORT_MAX_EDGES))
    files = (path,) if path else tuple(file for file in _tracked_project_files() if file.endswith(".py"))
    edges: list[dict[str, str]] = []
    for file_path in files:
        outline = read_file_outline(file_path)
        if not outline.get("allowed"):
            continue
        for imported in outline.get("imports", ())[:20]:
            edges.append({"from": file_path, "to": str(imported)})
            if len(edges) >= max_edges:
                return {"edges": tuple(edges), "edge_count": len(edges), "read_only": True}
    return {"edges": tuple(edges), "edge_count": len(edges), "read_only": True}


def status_tools() -> dict[str, str]:
    return {
        "jarvis_live_ci_status": _run_read_only_command(("python", "tools/project_readiness_control/jarvis_live_ci_status.py")),
        "roadmap_post_step_drift_check": _run_read_only_command(("python", "tools/roadmap_post_step_drift_check.py")),
        "read_only": "true",
    }






def _compact_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)


def model_runtime_status() -> dict[str, str]:
    version = _ollama_get_json("/api/version")
    tags = _ollama_get_json("/api/tags")
    ps = _ollama_get_json("/api/ps")
    show_primary = _ollama_post_json("/api/show", {"model": PRIMARY_CONVERSATION_MODEL_ID})
    return {
        "ollama_version": _compact_json(version) if version else "unavailable",
        "ollama_tags": _compact_json(tags) if tags else "unavailable",
        "ollama_ps": _compact_json(ps) if ps else "unavailable",
        "ollama_show_primary_model": _compact_json(show_primary) if show_primary else "unavailable",
        "nvidia_smi": _run_optional_read_only_command(("nvidia-smi",)),
        "free_h": _run_optional_read_only_command(("free", "-h")),
        "ollama_is_local_model_engine": "true",
        "pc_control_allowed": "false",
    }


def build_jarvis_live_memory_federation_status() -> dict[str, Any]:
    surfaces = _build_memory_surface_inventory()
    active = tuple(surface["surface_id"] for surface in surfaces if surface["status"] == "usable_now")
    disabled = tuple(surface["surface_id"] for surface in surfaces if surface["status"] in {"disabled", "not_connected", "unsafe"})
    sandbox_only = tuple(surface["surface_id"] for surface in surfaces if surface["status"] == "sandbox_only")
    return {
        "memory_federation_available": True,
        "memory_surfaces_detected_count": len(surfaces),
        "active_retrieval_surfaces": active,
        "disabled_memory_surfaces": disabled,
        "sandbox_only_memory_surfaces": sandbox_only,
        "vector_memory_available": any(surface["surface_id"] == "vector_runtime_indexes" and surface["status"] == "usable_now" for surface in surfaces),
        "regulatory_memory_available": any(surface["surface_id"] == "regulatory_memory_foundation" and surface["status"] == "usable_now" for surface in surfaces),
        "business_memory_available": any(surface["surface_id"] == "enterprise_business_memory" and surface["status"] == "usable_now" for surface in surfaces),
        "mempalace_status": _mempalace_status(),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "session_memory_exists": SESSION_STATE_PATH.exists(),
        "recent_turn_count": len(_load_session_state().get("recent_turns", [])),
        "surfaces": surfaces,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def build_jarvis_live_tool_catalog_read_model() -> dict[str, Any]:
    memory = build_jarvis_live_memory_federation_status()
    mgrep = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()
    sqlite_vec = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()
    qdrant = inspect_qdrant_readonly_availability(PROJECT_ROOT).to_read_model()
    memory_definitions = list_memory_definitions()
    enterprise_preview = build_enterprise_memory_preview()
    regulatory_preview = build_regulatory_routing_preview()
    mempalace_preview = build_mempalace_read_only_routing_integration_preview()
    read_tools = (
        "repo_git_status",
        "build_project_workspace_read_model",
        "repo_tree",
        "repo_files",
        "repo_search",
        "read_file_snippet",
        "read_file_outline",
        "repo_import_graph",
        "status_tools",
        "model_runtime_status",
        "stable_style_profile",
        "session_memory",
        "local_chat_memory",
        "runtime_history_store",
        "history_query",
        "memory_engine_registry",
        "enterprise_business_memory",
        "regulatory_memory_foundation",
        "vector_runtime_indexes",
        "mempalace_read_only_sandbox",
        "mgrep_readonly",
        "sqlite_vec_readonly",
        "qdrant_readonly_status",
        "retrieval_backend_status_read_model",
        "retrieval_vendor_gate_contract",
        "retrieval_tool_registry_contract",
        "semantic_intent_classifier",
    )
    proposal_tools = (
        "operator_proposal",
        "approval_boundary_read",
        "capability_registry_read",
        "pytest_run_proposal",
        "git_commit_proposal",
        "download_install_proposal",
        "n8n_adapter_proposal",
        "pc_action_proposal",
        "tool_call_proposal",
    )
    return {
        "catalog_id": "jarvis_live_existing_tool_catalog_v1",
        "read_only": True,
        "all_existing_read_tools_connected": True,
        "all_existing_memory_surfaces_connected": True,
        "read_tools": read_tools,
        "proposal_tools": proposal_tools,
        "memory_surfaces": tuple(surface["surface_id"] for surface in memory["surfaces"]),
        "active_retrieval_surfaces": memory["active_retrieval_surfaces"],
        "sandbox_only_memory_surfaces": memory["sandbox_only_memory_surfaces"],
        "disabled_memory_surfaces": memory["disabled_memory_surfaces"],
        "execution_allowed": False,
        "approval_required_for_actions": True,
        "pc_control_allowed": False,
        "shell_execution_enabled": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "runtime_mutation_allowed": False,
        "deployment_allowed_now": False,
        "retrieval_tool_contracts_visible": True,
        "retrieval_tool_runtime_enabled": True,
        "retrieval_auto_routing_contract_enabled": True,
        "retrieval_auto_routing_runtime_enabled": True,
        "project_repo_read_only_tools": (
            "repo_git_status",
            "build_project_workspace_read_model",
            "repo_tree",
            "repo_files",
            "repo_search",
            "read_file_snippet",
            "read_file_outline",
        ),
        "retrieval_read_only_tools": (
            "mgrep_readonly",
            "sqlite_vec_readonly",
            "qdrant_readonly_status",
            "retrieval_backend_status_read_model",
            "retrieval_tool_registry_contract",
        ),
        "memory_history_read_only_tools": (
            "session_memory",
            "local_chat_memory",
            "runtime_history_store",
            "history_query",
            "memory_engine_registry",
            "enterprise_business_memory",
            "regulatory_memory_foundation",
            "mempalace_read_only_sandbox",
        ),
        "model_status_read_only_tools": (
            "model_runtime_status",
            "build_jarvis_live_session_status",
            "build_jarvis_live_brain_health",
            "model_registry_status",
        ),
        "roadmap_safety_read_only_tools": (
            "status_tools",
            "roadmap_post_step_drift_check",
            "jarvis_live_ci_status",
            "project_safety_formatter",
        ),
        "action_proposal_only_tools": proposal_tools,
        "mgrep_status": mgrep,
        "sqlite_vec_status": sqlite_vec,
        "qdrant_status": qdrant,
        "memory_definition_count": len(memory_definitions),
        "memory_definition_ids": tuple(definition.entity_id for definition in memory_definitions[:24]),
        "enterprise_memory_preview_ready": bool(enterprise_preview.get("preview_ready", False)),
        "regulatory_routing_preview_ready": bool(regulatory_preview.get("preview_ready", False)),
        "mempalace_routing_ready": bool(mempalace_preview.get("routing_integration_ready", False)),
        "qdrant_server_runtime_enabled": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }


def _stream_ollama_model(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    transport_plan = _ollama_transport_plan(route_mode, prompt, response_mode_text or prompt)
    if route_mode != "FAST":
        yield from _stream_ollama_generate_model(
            model_id,
            prompt,
            route_mode,
            timeout_seconds=timeout_seconds,
            response_mode_text=response_mode_text,
        )
        return

    primary_endpoint = transport_plan["primary_endpoint"]
    fallback_endpoint = transport_plan["fallback_endpoint"]
    primary_error_reason: dict[str, Any] | None = None
    thinking_chunk_count = 0
    answer_chunk_count = 0
    tool_call_count = 0
    primary_done_event: dict[str, Any] = {}
    for event in _stream_ollama_chat_model(
        model_id,
        prompt,
        timeout_seconds=timeout_seconds,
        response_mode=transport_plan["response_mode"],
        response_mode_text=response_mode_text or prompt,
    ):
        event_type = str(event.get("event", ""))
        if event_type == "thinking":
            thinking_chunk_count += 1
            yield event
            continue
        if event_type == "tool_call":
            tool_call_count += int(event.get("tool_call_count", 0))
            yield event
            continue
        if event_type == "chunk":
            answer_chunk_count += 1
            yield event
            continue
        if event_type == "done":
            primary_done_event = event
            break
        if event_type == "error":
            primary_error_reason = {
                "error_kind": "ollama_chat_stream_error",
                "error_message": str(event.get("error_message", "ollama chat returned an error")),
                "ollama_model_used": model_id,
                "ollama_endpoint": primary_endpoint,
            }
            break

    if answer_chunk_count > 0 or tool_call_count > 0:
        primary_done_event = {
            **primary_done_event,
            "tool_call_count": tool_call_count,
            "tool_call_detected": bool(tool_call_count),
        }
        done_event = {
            **primary_done_event,
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
            "primary_endpoint": primary_endpoint,
            "fallback_endpoint": fallback_endpoint,
            "ollama_endpoint_fallback_used": False,
            "think_mode": transport_plan["think_mode"],
            "ollama_num_predict": transport_plan["ollama_num_predict"],
            "ollama_temperature": transport_plan["ollama_temperature"],
            "ollama_top_p": transport_plan["ollama_top_p"],
        }
        yield done_event
        return

    fallback_reason = primary_error_reason
    if fallback_reason is None and thinking_chunk_count > 0:
        fallback_reason = {
            "error_kind": "ollama_thinking_without_final_response",
            "error_message": "model produced thinking but no final response; increase num_predict or disable thinking.",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    if fallback_reason is None and primary_done_event:
        fallback_reason = {
            "error_kind": "ollama_chat_empty_response",
            "error_message": "chat endpoint returned done without content",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    if fallback_reason is None:
        fallback_reason = {
            "error_kind": "ollama_chat_unavailable",
            "error_message": "chat endpoint unavailable",
            "ollama_model_used": model_id,
            "ollama_endpoint": primary_endpoint,
        }
    yield from _collect_generate_stream_events(
        model_id=model_id,
        prompt=prompt,
        route_mode=route_mode,
        timeout_seconds=timeout_seconds,
        response_mode_text=response_mode_text,
        fallback_reason=fallback_reason,
        primary_endpoint=primary_endpoint,
        fallback_endpoint=fallback_endpoint,
    )


def _build_ollama_chat_payload(
    model_id: str,
    system_prompt: str,
    user_text: str,
    think_mode: bool | str = OLLAMA_FAST_CHAT_THINK,
    num_predict: int = OLLAMA_FAST_CHAT_NUM_PREDICT,
    temperature: float = OLLAMA_FAST_CHAT_TEMPERATURE,
    top_p: float = OLLAMA_FAST_CHAT_TOP_P,
    keep_alive: str = OLLAMA_FAST_CHAT_KEEP_ALIVE,
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model_id,
        "stream": True,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "think": think_mode,
        "keep_alive": keep_alive,
        "options": {
            "num_predict": num_predict,
            "temperature": temperature,
            "top_p": top_p,
        },
    }
    if tools:
        payload["tools"] = tools
    return payload


def _parse_ollama_chat_stream_event(payload: dict[str, Any], model_id: str) -> tuple[dict[str, Any], ...]:
    events: list[dict[str, Any]] = []
    if payload.get("error"):
        events.append(
            _event(
                "error",
                ollama_model_used=model_id,
                error_message=str(payload.get("error", "")),
            )
        )
        return tuple(events)
    message = payload.get("message") if isinstance(payload.get("message"), dict) else {}
    thinking = str(message.get("thinking", "") or payload.get("thinking", ""))
    content = str(message.get("content", "") or payload.get("response", "") or payload.get("content", ""))
    tool_calls = message.get("tool_calls") if isinstance(message, dict) else None
    if not isinstance(tool_calls, list):
        tool_calls = payload.get("tool_calls") if isinstance(payload.get("tool_calls"), list) else []
    if thinking:
        events.append(_event("thinking", text=thinking, ollama_model_used=model_id))
    if tool_calls:
        events.append(
            _event(
                "tool_call",
                ollama_model_used=model_id,
                tool_call_detected=True,
                tool_call_count=len(tool_calls),
                tool_calls=tuple(tool_calls),
                execution_allowed=False,
                approval_required=True,
                proposal_only=True,
            )
        )
    if content:
        events.append(_event("chunk", text=content, ollama_model_used=model_id))
    if payload.get("done") is True:
        events.append(_event("done", ollama_model_used=model_id))
    return tuple(events)


def _stream_ollama_chat_model(
    model_id: str,
    prompt: str,
    timeout_seconds: float | None = None,
    response_mode: Any | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    system_prompt, user_text = _split_chat_prompt(prompt, response_mode_text or prompt)
    payload = _build_ollama_chat_payload(
        model_id,
        system_prompt=system_prompt,
        user_text=user_text,
        think_mode=OLLAMA_FAST_CHAT_THINK,
        num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
        temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
        top_p=OLLAMA_FAST_CHAT_TOP_P,
        keep_alive=OLLAMA_FAST_CHAT_KEEP_ALIVE,
    )
    timeout = httpx.Timeout(timeout_seconds or 120.0, connect=min(10.0, timeout_seconds or 120.0))
    try:
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", OLLAMA_CHAT_URL, json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        chat_payload = json.loads(line)
                    except json.JSONDecodeError as exc:
                        yield _event(
                            "error",
                            ollama_model_used=model_id,
                            error_message=f"json_decode_error: {exc}",
                            ollama_endpoint=OLLAMA_CHAT_URL,
                            primary_endpoint=OLLAMA_CHAT_URL,
                            fallback_endpoint=OLLAMA_URL,
                            ollama_endpoint_fallback_used=False,
                            think_mode="false",
                            ollama_num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
                            ollama_temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
                            ollama_top_p=OLLAMA_FAST_CHAT_TOP_P,
                        )
                        return
                    for event in _parse_ollama_chat_stream_event(chat_payload, model_id):
                        event.setdefault("ollama_endpoint", OLLAMA_CHAT_URL)
                        event.setdefault("primary_endpoint", OLLAMA_CHAT_URL)
                        event.setdefault("fallback_endpoint", OLLAMA_URL)
                        event.setdefault("ollama_endpoint_fallback_used", False)
                        event.setdefault("think_mode", "false")
                        event.setdefault("ollama_num_predict", OLLAMA_FAST_CHAT_NUM_PREDICT)
                        event.setdefault("ollama_temperature", OLLAMA_FAST_CHAT_TEMPERATURE)
                        event.setdefault("ollama_top_p", OLLAMA_FAST_CHAT_TOP_P)
                        yield event
    except (httpx.HTTPError, TimeoutError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as exc:
        yield _event(
            "error",
            ollama_model_used=model_id,
            error_message=f"{exc.__class__.__name__}: {exc}",
            ollama_endpoint=OLLAMA_CHAT_URL,
            primary_endpoint=OLLAMA_CHAT_URL,
            fallback_endpoint=OLLAMA_URL,
            ollama_endpoint_fallback_used=False,
            think_mode="false",
            ollama_num_predict=OLLAMA_FAST_CHAT_NUM_PREDICT,
            ollama_temperature=OLLAMA_FAST_CHAT_TEMPERATURE,
            ollama_top_p=OLLAMA_FAST_CHAT_TOP_P,
        )


def _stream_ollama_generate_model(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None = None,
    response_mode_text: str | None = None,
) -> Iterator[dict[str, Any]]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    options = build_ollama_options(response_mode)
    request_payload: dict[str, Any] = {
        "model": model_id,
        "prompt": prompt,
        "stream": True,
        "options": options,
        "keep_alive": os.environ.get("JARVIS_LIVE_OLLAMA_KEEP_ALIVE", "30m"),
    }
    try:
        timeout = httpx.Timeout(timeout_seconds or 120.0, connect=min(10.0, timeout_seconds or 120.0))
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", OLLAMA_URL, json=request_payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if payload.get("error"):
                        yield _event(
                            "error",
                            ollama_model_used=model_id,
                            error_message=str(payload.get("error", "")),
                            ollama_endpoint=OLLAMA_URL,
                            primary_endpoint=OLLAMA_URL,
                            fallback_endpoint="",
                            ollama_endpoint_fallback_used=False,
                            think_mode="generate",
                            ollama_num_predict=options.get("num_predict", 0),
                            ollama_temperature=options.get("temperature", 0.0),
                            ollama_top_p=options.get("top_p", 0.0),
                        )
                        return
                    thinking = str(payload.get("thinking", ""))
                    if thinking:
                        yield _event("thinking", text=thinking, ollama_model_used=model_id, ollama_endpoint=OLLAMA_URL)
                    chunk = str(payload.get("response", ""))
                    if chunk:
                        yield _event("chunk", text=chunk, ollama_model_used=model_id, ollama_endpoint=OLLAMA_URL)
                    if payload.get("done") is True:
                        yield _event(
                            "done",
                            ollama_model_used=model_id,
                            ollama_endpoint=OLLAMA_URL,
                            primary_endpoint=OLLAMA_URL,
                            fallback_endpoint="",
                            ollama_endpoint_fallback_used=False,
                            think_mode="generate",
                            ollama_num_predict=options.get("num_predict", 0),
                            ollama_temperature=options.get("temperature", 0.0),
                            ollama_top_p=options.get("top_p", 0.0),
                        )
                        return
    except (httpx.HTTPError, TimeoutError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as exc:
        yield _event(
            "error",
            ollama_model_used=model_id,
            error_message=f"{exc.__class__.__name__}: {exc}",
            ollama_endpoint=OLLAMA_URL,
            primary_endpoint=OLLAMA_URL,
            fallback_endpoint="",
            ollama_endpoint_fallback_used=False,
            think_mode="generate",
            ollama_num_predict=options.get("num_predict", 0),
            ollama_temperature=options.get("temperature", 0.0),
            ollama_top_p=options.get("top_p", 0.0),
        )


def _ollama_transport_plan(
    route_mode: str,
    prompt: str,
    response_mode_text: str,
) -> dict[str, Any]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    if route_mode == "FAST":
        return {
            "response_mode": response_mode,
            "primary_endpoint": OLLAMA_CHAT_URL,
            "fallback_endpoint": OLLAMA_URL,
            "think_mode": "false",
            "ollama_num_predict": OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": OLLAMA_FAST_CHAT_TOP_P,
            "keep_alive": OLLAMA_FAST_CHAT_KEEP_ALIVE,
        }
    options = build_ollama_options(response_mode)
    return {
        "response_mode": response_mode,
        "primary_endpoint": OLLAMA_URL,
        "fallback_endpoint": "",
        "think_mode": "generate",
        "ollama_num_predict": int(options.get("num_predict", 0)),
        "ollama_temperature": float(options.get("temperature", 0.0)),
        "ollama_top_p": float(options.get("top_p", 0.0)),
        "keep_alive": os.environ.get("JARVIS_LIVE_OLLAMA_KEEP_ALIVE", "30m"),
    }


def _split_chat_prompt(prompt: str, fallback_user_text: str) -> tuple[str, str]:
    marker = "\nUSER_MESSAGE: "
    if marker in prompt:
        system_prompt, user_text = prompt.rsplit(marker, 1)
        user_text = user_text.strip() or fallback_user_text
        return system_prompt.strip(), user_text
    return prompt.strip(), fallback_user_text


def _collect_chat_stream_events(
    model_id: str,
    prompt: str,
    timeout_seconds: float | None,
    response_mode: Any | None,
    response_mode_text: str,
) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    thinking_chunk_count = 0
    answer_chunk_count = 0
    tool_call_count = 0
    primary_error_event: dict[str, Any] | None = None
    done_event: dict[str, Any] = {}
    for event in _stream_ollama_chat_model(
        model_id,
        prompt,
        timeout_seconds=timeout_seconds,
        response_mode=response_mode,
        response_mode_text=response_mode_text,
    ):
        event_type = str(event.get("event", ""))
        if event_type == "thinking":
            thinking_chunk_count += 1
            events.append(event)
            continue
        if event_type == "tool_call":
            tool_call_count += int(event.get("tool_call_count", 0))
            events.append(event)
            continue
        if event_type == "chunk":
            answer_chunk_count += 1
            events.append(event)
            continue
        if event_type == "error":
            primary_error_event = {
                "error_kind": "ollama_chat_stream_error",
                "error_message": str(event.get("error_message", "ollama chat returned an error")),
                "ollama_model_used": model_id,
                "ollama_endpoint": OLLAMA_CHAT_URL,
            }
            break
        if event_type == "done":
            done_event = event
            break
    return {
        "events": tuple(events),
        "done_event": done_event,
        "thinking_chunk_count": thinking_chunk_count,
        "answer_chunk_count": answer_chunk_count,
        "tool_call_count": tool_call_count,
        "primary_error_event": primary_error_event,
        "ollama_endpoint": OLLAMA_CHAT_URL,
        "primary_endpoint": OLLAMA_CHAT_URL,
        "fallback_endpoint": OLLAMA_URL,
        "think_mode": "false",
        "ollama_num_predict": OLLAMA_FAST_CHAT_NUM_PREDICT,
        "ollama_temperature": OLLAMA_FAST_CHAT_TEMPERATURE,
        "ollama_top_p": OLLAMA_FAST_CHAT_TOP_P,
        "ollama_endpoint_fallback_used": False,
    }


def _collect_generate_stream_events(
    model_id: str,
    prompt: str,
    route_mode: str,
    timeout_seconds: float | None,
    response_mode_text: str | None,
    fallback_reason: dict[str, Any] | None,
    primary_endpoint: str,
    fallback_endpoint: str,
) -> Iterator[dict[str, Any]]:
    response_mode = classify_response_mode(response_mode_text or prompt)
    options = build_ollama_options(response_mode)
    for event in _stream_ollama_generate_model(
        model_id,
        prompt,
        route_mode,
        timeout_seconds=timeout_seconds,
        response_mode_text=response_mode_text,
    ):
        if fallback_reason:
            enriched = {
                **event,
                "primary_endpoint": primary_endpoint,
                "fallback_endpoint": fallback_endpoint,
                "ollama_endpoint_fallback_used": True,
                "primary_error_kind": str(fallback_reason.get("error_kind", "")),
                "primary_error_message": str(fallback_reason.get("error_message", "")),
                "think_mode": "generate",
                "ollama_num_predict": options.get("num_predict", 0),
                "ollama_temperature": options.get("temperature", 0.0),
                "ollama_top_p": options.get("top_p", 0.0),
            }
            if event.get("event") == "error":
                enriched.setdefault("error_kind", str(fallback_reason.get("error_kind", "ollama_stream_error")))
            if event.get("event") == "done" and not enriched.get("error_kind"):
                enriched["error_kind"] = ""
            yield enriched
        else:
            yield event


def write_stream_event_safely(write_callable: Any, event: dict[str, Any]) -> bool:
    try:
        write_callable(json.dumps(event, ensure_ascii=False) + "\n")
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        print("[WARNING] Client disconnected before receiving response")
        return False
    return True


def _command_timeout_seconds(value: float | None) -> float:
    if value is not None and value > 0:
        return float(value)
    raw = os.environ.get("JARVIS_LIVE_COMMAND_TIMEOUT_SECONDS", "120")
    try:
        parsed = float(raw)
    except ValueError:
        return 120.0
    return max(1.0, parsed)


def _command_error_payload(user_text: str, error_kind: str) -> dict[str, Any]:
    selected = select_jarvis_live_model_role(user_text)
    memory = build_jarvis_live_memory_federation_status()
    return {
        "event": "done",
        "response_text": "JARVIS command runtime не успел вернуть модельный ответ. Запрос не выполнен как действие; можно повторить или проверить Ollama статус.",
        "ollama_model_used": "",
        "route_mode": _route_mode(user_text),
        "stream_chunk_count": 0,
        "retrieved_snippet_count": 0,
        "retrieval_surfaces_used": (),
        "memory_federation_available": memory["memory_federation_available"],
        "mempalace_status": memory["mempalace_status"],
        "selected_model_role": selected["selected_model_role"],
        "selected_model_id": selected["model_id"],
        "selected_model_status": selected["status"],
        "admission_allowed": False,
        "resource_gate_surface": "MAKSIMAR_CORE_LIB/execution_control/admission_contract.py",
        "session_memory_path": str(SESSION_STATE_PATH),
        "local_chat_memory_path": str(_session_turn_log_path()),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "memory_truth_split": _memory_truth_split(),
        "dangerous_mutation_flags": dict(DANGEROUS_MEMORY_FLAGS),
        "error_kind": error_kind,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def _candidate_model_ids_for_context(context: JarvisBrainContext) -> tuple[str, ...]:
    selected_model_id = str(context.selected_model_role["model_id"])
    role_id = context.selected_model_role["selected_model_role"]
    candidates = [selected_model_id]
    if context.route_mode == "FAST" and os.environ.get("JARVIS_LIVE_FAST_FALLBACK_ENABLED") != "1":
        return tuple(candidates)
    if role_id == "heavy_coder_model":
        candidates.extend((HEAVY_CODER_MODEL_ID, BASE_HEAVY_CODER_MODEL_ID, FALLBACK_OLLAMA_MODEL_ID))
    elif role_id == "daily_coder_model":
        candidates.extend(("jarvis:coder7b", FALLBACK_OLLAMA_MODEL_ID))
    elif role_id == "helper_classifier_model":
        candidates.extend(("jarvis:helper3b", DEFAULT_OLLAMA_MODEL_ID))
    else:
        candidates.extend((DEFAULT_OLLAMA_MODEL_ID, FALLBACK_OLLAMA_MODEL_ID))
    return tuple(dict.fromkeys(candidates))


def _build_admission_status(selected_model_role: dict[str, Any]) -> dict[str, Any]:
    role_id = str(selected_model_role["selected_model_role"])
    exclusive_gpu_required = role_id == "heavy_coder_model"
    return {
        "admission_allowed": True,
        "enqueue_required": True,
        "queue_surface": "MAKSIMAR_CORE_LIB/execution_control",
        "resource_gate_surface": "MAKSIMAR_CORE_LIB/execution_control/admission_contract.py",
        "worker_registry_surface": "MAKSIMAR_CORE_LIB/workers_registry",
        "exclusive_gpu_required": exclusive_gpu_required,
        "concurrent_heavy_jobs_allowed": False,
        "agents_enabled": False,
        "agents_may_call_14b_directly": False,
        "pc_control_allowed": False,
    }


def _build_read_only_tool_plan(user_text: str, context: JarvisBrainContext) -> dict[str, Any]:
    lowered = user_text.casefold()
    intent_family = "CONVERSATION"
    selected_tools: tuple[str, ...] = ()
    tool_route = None
    confidence = 0.0
    reason = "ordinary conversation"
    needs_ollama = True
    evidence_required = False

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

    return {
        "intent_family": intent_family,
        "confidence": confidence,
        "selected_tools": selected_tools,
        "reason": reason,
        "read_only": True,
        "execution_allowed": False,
        "needs_ollama": needs_ollama,
        "evidence_required": evidence_required,
        "evidence_count": 0,
        "tool_route": tool_route.to_read_model() if tool_route is not None else {},
    }


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


def _answer_conversation_style_complaint_if_grounded(context: JarvisBrainContext) -> str:
    lowered = context.user_text.casefold()
    if _looks_like_keyboard_layout_noise(context.user_text):
        return (
            "Похоже, раскладка поехала. Я не буду лепить заготовку вместо смысла: "
            "повтори фразу нормальной раскладкой, и я разберу её по делу."
        )
    if _asks_template_style_complaint(lowered):
        return (
            "Да, брат, вижу петлю: я начал повторять canned-ответ вместо реакции на смысл. "
            "Это не нормальный разговор. Чинить надо в двух местах: fast-chat guard не должен пропускать "
            "заготовки, а session memory не должна кормить их обратно в следующий ответ. "
            "Для обычного общения держу живой стиль: прямо, по делу, но не сухим шаблоном."
        )
    if _asks_casual_state_question(lowered):
        return (
            "На связи, брат. По состоянию честно: чат работает, но я вижу риск шаблонной петли, "
            "поэтому обычный разговор надо держать живым guard'ом и памятью последних реплик, "
            "а не одной дежурной фразой."
        )
    return ""


def _asks_template_style_complaint(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "шаблон",
            "заготов",
            "одно и то же",
            "один и тот же ответ",
            "перестань шаблон",
            "почему ты мне шаблон",
            "отвечаешь шаблон",
            "не живой",
            "живее",
        )
    )


def _asks_casual_state_question(lowered: str) -> bool:
    cleaned = lowered.strip(" ?!.,")
    return cleaned in {"как дела", "как ты", "ты как", "как состояние", "ты на связи"}


def _looks_like_keyboard_layout_noise(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 10:
        return False
    letters = [char for char in stripped if char.isalpha()]
    if not letters:
        return False
    latin_letters = [char for char in letters if "a" <= char.casefold() <= "z"]
    cyrillic_letters = [char for char in letters if "а" <= char.casefold() <= "я" or char.casefold() == "ё"]
    punctuation_noise = sum(1 for char in stripped if char in "&;,./[]{}")
    return len(latin_letters) >= max(8, len(letters) * 3 // 4) and not cyrillic_letters and punctuation_noise > 0


def _is_forbidden_chat_template_response(response_text: str) -> bool:
    return contains_forbidden_generic_tail(response_text)


def _repair_forbidden_chat_template_response(context: JarvisBrainContext) -> str:
    if _asks_template_style_complaint(context.user_text.casefold()):
        return _answer_conversation_style_complaint_if_grounded(context)
    return (
        "Сбил шаблонный ответ и не сохраняю его как нормальную память. "
        "По смыслу текущего запроса отвечаю заново: мне нужно держаться фактов из контекста, "
        "а если фактов не хватает — прямо сказать, что нужна проверка."
    )


def _answer_with_read_only_tools_if_grounded(
    user_text: str,
    context: JarvisBrainContext,
    plan: dict[str, Any],
) -> str:
    intent = str(plan.get("intent_family", "CONVERSATION"))
    if intent == "CONVERSATION":
        return ""
    if intent == "ACTIVATION_MATRIX":
        plan["evidence_count"] = 1
        return _format_activation_matrix_answer()
    if intent == "PROJECT_STATUS":
        plan["evidence_count"] = 1
        return _format_project_status_answer()
    if intent == "PROJECT_STRUCTURE":
        plan["evidence_count"] = 3
        return _format_project_structure_grounded_answer()
    if intent == "PROJECT_SEARCH":
        answer, evidence_count = _format_project_semantic_search_answer(user_text, _plan_tool_route(plan))
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "SEMANTIC_SIMILARITY":
        answer, evidence_count = _format_semantic_similarity_answer(
            user_text,
            _plan_tool_route(plan),
            _extract_semantic_similarity_query(user_text),
        )
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "RETRIEVAL_BACKEND_STATUS":
        plan["evidence_count"] = 3
        return _format_retrieval_backend_status_answer()
    if intent == "VENDOR_STATUS":
        plan["evidence_count"] = 2
        return _format_retrieval_vendor_status_answer()
    if intent == "CONTAINER_STATUS":
        plan["evidence_count"] = 3
        return _format_retrieval_container_status_answer()
    if intent == "TEST_STATUS":
        plan["evidence_count"] = 1
        return _format_roadmap_answer()
    if intent == "SOURCE_EVIDENCE":
        answer, evidence_count = _format_source_evidence_answer(user_text)
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "DOCS_CONTRACTS":
        answer, evidence_count = _format_project_semantic_search_answer(user_text, _plan_tool_route(plan))
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "AUTO_TOOL_USE":
        plan["evidence_count"] = 2
        return _format_auto_tool_use_status_answer()
    if intent == "PROJECT_FILE":
        path = _extract_requested_file_path(user_text)
        if not path:
            plan["evidence_count"] = 0
            return "Не нашёл подтверждение в текущих read-only источниках: путь файла не распознан."
        snippet = _format_file_answer(path, page=1, intent="PROJECT_FILE")
        outline = _format_outline_answer(path)
        plan["evidence_count"] = 2 if "denied" not in snippet.casefold() else 0
        return snippet + "\n\n" + outline
    if intent == "MEMORY_RECALL":
        answer, evidence_count = _format_memory_history_grounded_answer(user_text, context)
        plan["evidence_count"] = evidence_count
        return answer
    if intent == "MODEL_STATUS":
        plan["evidence_count"] = 1
        return _format_project_models_answer()
    if intent == "ROADMAP_STATUS":
        plan["evidence_count"] = 1
        return _format_roadmap_answer()
    if intent == "SAFETY_STATUS":
        plan["evidence_count"] = 1
        return _format_safety_answer()
    if intent == "ACTION_REQUEST":
        plan["evidence_count"] = 1
        return _format_action_request_proposal_answer(user_text)
    if intent == "TOOL_CATALOG":
        catalog = build_jarvis_live_tool_catalog_read_model()
        plan["evidence_count"] = len(catalog["read_tools"]) + len(catalog["proposal_tools"])
        return _format_tool_catalog_answer(catalog)
    return ""


def _plan_tool_route(plan: dict[str, Any]) -> dict[str, Any]:
    route = plan.get("tool_route")
    return route if isinstance(route, dict) else {}


def _answer_project_read_tool_request(user_text: str) -> str:
    text = user_text.strip()
    lowered = text.casefold()
    if text.startswith("/project"):
        return _answer_project_command(text)
    if any(marker in lowered for marker in ("что изменено", "что поменялось", "какие изменения", "dirty", "untracked")):
        return _format_project_status_answer()
    if any(marker in lowered for marker in ("покажи полностью весь проект", "весь проект", "полный проект")):
        return _format_project_atlas_answer()
    if "terminal chat" in lowered and any(marker in lowered for marker in ("где", "найди", "что у нас")):
        return _format_search_answer("terminal_chat jarvis_live_terminal_chat")
    if any(marker in lowered for marker in ("core guard", "watchdog", "safety", "security", "approval", "execution control")):
        return _format_safety_answer()
    if any(marker in lowered for marker in ("ollama", "qwen", "модел", "model")) and any(marker in lowered for marker in ("что сделано", "статус", "runtime", "оптимизац")):
        return _format_project_models_answer()
    return ""


def _answer_project_command(text: str) -> str:
    parts = text.split()
    if len(parts) == 1:
        return _format_project_snapshot_answer()
    command = parts[1]
    if command == "status":
        return _format_project_status_answer()
    if command == "tree":
        return _format_tree_answer()
    if command == "files":
        page = _parse_int(parts[2], default=1) if len(parts) > 2 else 1
        return _format_files_answer(page)
    if command == "dirty":
        return _format_dirty_answer()
    if command == "search" and len(parts) > 2:
        return _format_search_answer(" ".join(parts[2:]))
    if command == "file" and len(parts) > 2:
        page = _parse_int(parts[3], default=1) if len(parts) > 3 else 1
        return _format_file_answer(parts[2], page, intent="PROJECT_FILE")
    if command == "outline" and len(parts) > 2:
        return _format_outline_answer(parts[2])
    if command == "imports":
        return _format_imports_answer(parts[2] if len(parts) > 2 else None)
    if command == "tests":
        return _format_tests_answer()
    if command == "roadmap":
        return _format_roadmap_answer()
    if command == "models":
        return _format_project_models_answer()
    if command == "safety":
        return _format_safety_answer()
    return _format_project_help()


def _format_project_snapshot_answer() -> str:
    model = build_project_workspace_read_model()
    tree_entries = model["top_level_tree"]["entries"][:25]
    return (
        "Project workspace read-only snapshot:\n"
        f"project_root={model['project_root']}\n"
        f"branch={model['git_branch']} head={str(model['git_head'])[:12]}\n"
        f"tracked_file_count={model['tracked_file_count']}\n"
        f"top_level={', '.join(tree_entries)}\n"
        f"dirty={len(model['dirty_files'])} untracked={len(model['untracked_files'])} staged={len(model['staged_files'])}\n"
        "read_only=true direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )


def _format_project_status_answer() -> str:
    status = repo_git_status()
    return (
        "Project git status read-only:\n"
        f"branch={status['branch']} head={str(status['head'])[:12]}\n"
        f"dirty_files={_csv(status['dirty_files']) or 'none'}\n"
        f"untracked_files={_csv(status['untracked_files']) or 'none'}\n"
        f"staged_files={_csv(status['staged_files']) or 'none'}\n"
        f"diff_name_only={_csv(status['diff_name_only']) or 'none'}\n"
        f"diff_stat={status['diff_stat'] or 'none'}\n"
        "read_only=true direct_execution_allowed=false"
    )


def _format_project_structure_grounded_answer() -> str:
    model = build_project_workspace_read_model()
    tree_entries = model["top_level_tree"]["entries"][:35]
    canonical_chain = (
        "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py -> "
        "CONTROL_PLANE/api_server.py -> "
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py -> "
        "tools/jarvis_live_runtime/jarvis_live_brain_loop.py -> Ollama"
    )
    return (
        "Да, брат, проверил workspace read-only.\n"
        f"project_root={model['project_root']}\n"
        f"branch={model['git_branch']} head={str(model['git_head'])[:12]}\n"
        f"tracked_file_count={model['tracked_file_count']}\n"
        f"dirty={len(model['dirty_files'])} untracked={len(model['untracked_files'])} staged={len(model['staged_files'])}\n"
        f"top_level={', '.join(tree_entries)}\n"
        f"terminal chat canonical chain={canonical_chain}\n"
        "next_inspect=/project files 1 | /project search <term> | /project file <path> 1\n"
        "read_only=true direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )


def _format_tree_answer() -> str:
    tree = repo_tree()
    return "Project tree page read-only:\n" + "\n".join(f"- {entry}" for entry in tree["entries"][:PROJECT_TREE_MAX_ENTRIES])


def _format_files_answer(page: int) -> str:
    payload = repo_files(page=page)
    lines = [f"Project files page {payload['page']}/{payload['total_pages']} read-only:"]
    lines.extend(f"- {path}" for path in payload["files"])
    return "\n".join(lines)


def _format_dirty_answer() -> str:
    status = repo_git_status()
    return (
        "Project dirty files read-only:\n"
        f"staged={_csv(status['staged_files']) or 'none'}\n"
        f"dirty={_csv(status['dirty_files']) or 'none'}\n"
        f"untracked={_csv(status['untracked_files']) or 'none'}"
    )


def _format_search_answer(query: str) -> str:
    payload = repo_search(query)
    if not payload["results"]:
        return f"Search read-only: query={query}; results=none."
    lines = [f"Search read-only: query={query}; results={payload['result_count']}"]
    for result in payload["results"]:
        lines.append(f"- {result['path']}:{result['line_number']}: {result['line']}")
    return "\n".join(lines)


def _format_project_semantic_search_answer(
    user_text: str,
    tool_route: dict[str, Any] | None = None,
    semantic_query: str | None = None,
    intent_label: str = "PROJECT_SEARCH",
) -> tuple[str, int]:
    route = tool_route or build_retrieval_readonly_tool_route("PROJECT_SEARCH", ("mgrep_readonly", "repo_search"), PROJECT_ROOT).to_read_model()
    mgrep = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()
    query = semantic_query.strip() if semantic_query and semantic_query.strip() else _semantic_search_query(user_text)
    payload = repo_search(query)
    if not payload["results"] and query != user_text.strip():
        payload = repo_search(user_text.strip())
    path_hits = _project_path_matches(query)
    if not payload["results"]:
        if path_hits:
            lines = [
                f"[work] intent={intent_label}",
                f"primary_tool={route['primary_tool']}",
                f"effective_tool={route['effective_tool']}",
                f"selected_tool_chain={_csv(route['selected_tool_chain'])}",
                f"fallback_tool={route['fallback_tool']}",
                f"fallback_reason={route['fallback_reason']}",
                f"mgrep_source_present={str(mgrep['source_present']).lower()}",
                f"mgrep_usable_now={str(mgrep['usable_now']).lower()}",
                f"Нашёл по именам файлов read-only: query={query}; path_results={len(path_hits)}",
            ]
            lines.extend(f"- {path}" for path in path_hits[:20])
            for path in path_hits[:2]:
                outline = read_file_outline(path)
                if outline.get("allowed"):
                    lines.append(
                        f"outline {path}: imports={_csv(outline['imports']) or 'none'}; "
                        f"classes={_csv(outline['classes']) or 'none'}; "
                        f"functions={_csv(outline['functions'][:12]) or 'none'}"
                    )
            lines.append("read_only=true execution_allowed=false direct_execution_allowed=false")
            return "\n".join(lines), len(path_hits)
        return (
            f"[work] intent={intent_label}\n"
            "Не нашёл подтверждение в текущих read-only источниках.\n"
            f"primary_tool={route['primary_tool']}\n"
            f"effective_tool={route['effective_tool']}\n"
            f"selected_tool_chain={_csv(route['selected_tool_chain'])}\n"
            f"fallback_tool={route['fallback_tool']}\n"
            f"fallback_reason={route['fallback_reason']}\n"
            f"mgrep_source_present={str(mgrep['source_present']).lower()}\n"
            f"mgrep_usable_now={str(mgrep['usable_now']).lower()}\n"
            "checked_tools=mgrep_readonly, repo_search, read_file_snippet, read_file_outline\n"
            f"query={query}",
            0,
        )
    lines = [
        f"[work] intent={intent_label}",
        f"primary_tool={route['primary_tool']}",
        f"effective_tool={route['effective_tool']}",
        f"selected_tool_chain={_csv(route['selected_tool_chain'])}",
        f"fallback_tool={route['fallback_tool']}",
        f"fallback_reason={route['fallback_reason']}",
        f"mgrep_source_present={str(mgrep['source_present']).lower()}",
        f"mgrep_usable_now={str(mgrep['usable_now']).lower()}",
        f"Нашёл по проекту read-only: query={query}; results={payload['result_count']}",
    ]
    paths: list[str] = []
    for result in payload["results"][:12]:
        path = str(result["path"])
        if path not in paths:
            paths.append(path)
        lines.append(f"- {path}:{result['line_number']}: {result['line']}")
    for path in path_hits[:8]:
        if path not in paths:
            paths.append(path)
            lines.append(f"- {path}: path_match")
    for path in paths[:2]:
        outline = read_file_outline(path)
        if outline.get("allowed"):
            lines.append(
                f"outline {path}: imports={_csv(outline['imports']) or 'none'}; "
                f"classes={_csv(outline['classes']) or 'none'}; "
                f"functions={_csv(outline['functions'][:12]) or 'none'}"
            )
    lines.append("read_only=true execution_allowed=false direct_execution_allowed=false")
    return "\n".join(lines), int(payload["result_count"]) + len(path_hits)


def _format_semantic_similarity_answer(
    user_text: str,
    tool_route: dict[str, Any] | None = None,
    semantic_query: str | None = None,
) -> tuple[str, int]:
    route = tool_route or build_retrieval_readonly_tool_route(
        "SEMANTIC_SIMILARITY",
        ("sqlite_vec_readonly", "repo_search", "qdrant_readonly"),
        PROJECT_ROOT,
    ).to_read_model()
    sqlite_vec = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()
    query = semantic_query.strip() if semantic_query and semantic_query.strip() else _extract_semantic_similarity_query(user_text)
    answer, evidence_count = _format_project_semantic_search_answer(user_text, route, query, "SEMANTIC_SIMILARITY")
    recommendation = (
        "EXTEND existing surface when evidence paths match the requested domain; "
        "otherwise create only a contract/adapter after source review."
    )
    return (
        f"primary_tool={route['primary_tool']}\n"
        f"effective_tool={route['effective_tool']}\n"
        f"selected_tool_chain={_csv(route['selected_tool_chain'])}\n"
        f"fallback_tool={route['fallback_tool']}\n"
        f"fallback_reason={route['fallback_reason']}\n"
        f"sqlite_vec_source_present={str(sqlite_vec['source_present']).lower()}\n"
        f"sqlite_vec_usable_now={str(sqlite_vec['usable_now']).lower()}\n"
        + answer
        + "\nsemantic_duplicate_policy=read_only_repo_search_before_vector_runtime\n"
        + "sqlite_vec_readonly_runtime_enabled=false qdrant_readonly_runtime_enabled=false\n"
        + f"CREATE_EXTEND_ADAPTER_RECOMMENDATION={recommendation}"
    ), evidence_count


def _format_retrieval_backend_status_answer() -> str:
    status = build_retrieval_backend_status_read_model().to_read_model()
    registry = build_retrieval_tool_registry_contract().to_read_model()
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    availability = {
        item.backend_kind: item.to_read_model()
        for item in build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
    }
    lines = [
        "[work] intent=RETRIEVAL_BACKEND_STATUS",
        "primary_tool=qdrant_readonly_status",
        "effective_tool=qdrant_readonly_status",
        "selected_tool_chain=qdrant_readonly_status,retrieval_backend_status_read_model,retrieval_tool_registry_contract",
        "fallback_reason=qdrant source is present but server/container runtime is intentionally disabled",
        "Retrieval backend status read-only:",
        "contract_ready=true",
        "vendor_acquired=true",
        "scan_passed=false",
        f"runtime_enabled={str(status['execution_allowed_now']).lower()}",
        f"read_only_tool_routing_enabled={str(policy['read_only_tool_routing_enabled']).lower()}",
        f"auto_routing_readonly_enabled={str(policy['auto_routing_readonly_enabled']).lower()}",
        f"tool_registered={str(registry['runtime_registration_enabled']).lower()}",
        f"readonly_router_registered={str(registry['readonly_router_registration_enabled']).lower()}",
        f"backend_runtime_enabled={str(policy['backend_runtime_enabled']).lower()}",
        f"auto_routing_runtime_enabled={str(policy['auto_routing_runtime_enabled']).lower()}",
    ]
    for adapter in status["adapter_statuses"]:
        lines.append(
            f"- {adapter['backend_kind']}: contract_mode={adapter['contract_mode']} "
            f"source_of_truth={str(adapter['source_of_truth']).lower()} "
            f"source_ref_required={str(adapter['source_ref_required']).lower()} "
            f"evidence_binding_required={str(adapter['evidence_binding_required']).lower()} "
            f"output_requires_normalization={str(adapter['output_requires_normalization']).lower()} "
            f"execution_allowed_now={str(adapter['execution_allowed_now']).lower()} "
            f"network_allowed_by_default={str(adapter['network_allowed_by_default']).lower()}"
        )
    for backend_kind in ("mgrep", "sqlite_vec", "qdrant"):
        backend = availability[backend_kind]
        lines.append(
            f"- {backend_kind}_runtime_readonly: source_present={str(backend['source_present']).lower()} "
            f"usable_now={str(backend['usable_now']).lower()} selected_tool={backend['selected_tool']} "
            f"fallback_tool={backend['fallback_tool']} unavailable_reason={backend['unavailable_reason']}"
        )
    lines.append("qdrant_network_service_adapter_candidate=true qdrant_server_required_now=false qdrant_container_enabled=false")
    lines.append("read_only=true execution_allowed=false direct_execution_allowed=false canonical_write_allowed=false")
    lines.append("source_ref=MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_status_read_model.py")
    return "\n".join(lines)


def _format_retrieval_vendor_status_answer() -> str:
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    vendor_gate = policy["vendor_gate"]
    lines = [
        "Retrieval vendor/quarantine status read-only:",
        f"vendor_gate_required={str(vendor_gate['vendor_gate_required']).lower()}",
        f"source_verified_required={str(vendor_gate['source_verified_required']).lower()}",
        f"license_review_required={str(vendor_gate['license_review_required']).lower()}",
        f"scanner_required={str(vendor_gate['scanner_required']).lower()}",
        f"runtime_enabled={str(vendor_gate['runtime_enabled']).lower()}",
        "manifest=EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml",
    ]
    for source in vendor_gate["vendor_sources"]:
        lines.append(
            f"- {source['backend_kind']}: source_url={source['source_url']} "
            f"source_status={source['source_status']} scan_status={source['scan_status']} "
            f"vendor_gate_completed={str(source['vendor_gate_completed']).lower()} "
            f"fail_closed_until_source_verified={str(source['fail_closed_until_source_verified']).lower()}"
        )
    lines.append("safe_next_step=run vendor quarantine source/license/scanner gate before any runtime/download/install.")
    return "\n".join(lines)


def _format_retrieval_container_status_answer() -> str:
    contract = read_file_snippet("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml", start_line=1, end_line=80)
    profile = read_file_snippet("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml", start_line=1, end_line=80)
    return (
        "Retrieval container/runtime boundary read-only:\n"
        "container_ready=true runtime_enabled=false docker_required_now=false "
        "qdrant_container_enabled=false network_allowed_by_default=false\n"
        "source_ref=CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml;"
        "CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml\n"
        f"container_contract_allowed={str(contract.get('allowed', False)).lower()} "
        f"runtime_profile_allowed={str(profile.get('allowed', False)).lower()}\n"
        "safe_next_step=keep runtime disabled until a later explicit runtime batch approves service/network/container execution."
    )


def _format_source_evidence_answer(user_text: str) -> tuple[str, int]:
    query = _semantic_search_query(user_text)
    if query == "jarvis":
        query = "source_ref evidence_binding evidence_id trace_id"
    answer, evidence_count = _format_project_semantic_search_answer(query)
    if evidence_count == 0:
        return (
            "Evidence missing: no source/evidence hit was found in read-only repo search. "
            "needed_tool=repo_search/read_file_snippet safe_next_step=ask for a narrower file, contract, or trace id.",
            0,
        )
    return answer + "\nsource_bound=true hallucination_allowed=false", evidence_count


def _format_auto_tool_use_status_answer() -> str:
    policy = build_retrieval_tool_enablement_policy().to_read_model()
    return (
        "Automatic read-only tool routing status:\n"
        "semantic_classifier=enabled_in_existing_router\n"
        f"intent_groups={_csv(policy['semantic_intent_groups'])}\n"
        "read_only_first=true free_generation_after_tool_check=true\n"
        f"runtime_tool_execution_enabled={str(policy['runtime_tool_execution_enabled']).lower()} "
        f"auto_routing_runtime_enabled={str(policy['auto_routing_runtime_enabled']).lower()} "
        "direct_execution_allowed=false pc_control_allowed=false canonical_write_allowed=false"
    )


def _format_file_answer(path: str, page: int, intent: str = "PROJECT_FILE") -> str:
    payload = read_file_snippet(path, page=page)
    if not payload.get("allowed"):
        return (
            f"[work] intent={intent}\n"
            "primary_tool=read_file_snippet\n"
            "effective_tool=read_file_snippet\n"
            "selected_tool_chain=read_file_snippet,read_file_outline,repo_files\n"
            f"fallback_reason={payload.get('error', 'unknown')}\n"
            f"File snippet denied: path={path}; error={payload.get('error', 'unknown')}; "
            "read_only=true execution_allowed=false"
        )
    lines = [
        f"[work] intent={intent}",
        "primary_tool=read_file_snippet",
        "effective_tool=read_file_snippet",
        "selected_tool_chain=read_file_snippet,read_file_outline,repo_files",
        "fallback_reason=exact filename resolved before Ollama fallback",
        f"File snippet read-only: {path} page={payload['page']} lines={payload['start_line']}-{payload['end_line']}",
    ]
    lines.extend(payload["snippet"])
    lines.append("read_only=true execution_allowed=false")
    return "\n".join(lines)


def _format_outline_answer(path: str) -> str:
    payload = read_file_outline(path)
    if not payload.get("allowed"):
        return f"File outline denied: path={path}; error={payload.get('error', 'unknown')}; read_only=true."
    return (
        f"File outline read-only: {path}; line_count={payload['line_count']}\n"
        f"imports={_csv(payload['imports']) or 'none'}\n"
        f"classes={_csv(payload['classes']) or 'none'}\n"
        f"functions={_csv(payload['functions']) or 'none'}\n"
        f"constants={_csv(payload['constants']) or 'none'}"
    )


def _format_imports_answer(path: str | None) -> str:
    payload = repo_import_graph(path=path)
    lines = [f"Import graph read-only: edges={payload['edge_count']}"]
    lines.extend(f"- {edge['from']} -> {edge['to']}" for edge in payload["edges"])
    return "\n".join(lines)


def _format_tests_answer() -> str:
    tests = [path for path in _tracked_project_files() if path.startswith("tests/") and path.endswith(".py")]
    groups = _domain_groups_for_paths(tuple(tests))
    lines = [f"Project tests read-only: test_file_count={len(tests)}"]
    for group, paths in groups.items():
        if paths:
            lines.append(f"- {group}: {len(paths)} files; sample={', '.join(paths[:6])}")
    return "\n".join(lines)


def _format_roadmap_answer() -> str:
    status = status_tools()
    return (
        "Roadmap/status read-only:\n"
        f"jarvis_live_ci_status:\n{status.get('jarvis_live_ci_status', '')}\n"
        f"roadmap_post_step_drift_check:\n{status.get('roadmap_post_step_drift_check', '')}"
    )


def _format_project_models_answer() -> str:
    status = model_runtime_status()
    return (
        "Ollama/model runtime read-only:\n"
        "canonical_chain=chat launcher -> CONTROL_PLANE/api_server.py -> "
        "jarvis_live_brain_loop_server_adapter.py -> jarvis_live_brain_loop.py -> Ollama\n"
        "Ollama is local model engine on localhost:11434, not a second JARVIS server.\n"
        "tool_calls are proposals/requests only; actual execution must go through CONTROL_PLANE capability/approval/action adapter/audit.\n"
        "future_adapter_scope=/api/chat, think control, tool_calls, structured JSON, /api/ps, /api/tags, /api/show, keep_alive, embeddings later\n"
        f"ollama_version={status.get('ollama_version') or 'unavailable'}\n"
        f"ollama_tags={status.get('ollama_tags') or 'unavailable'}\n"
        f"ollama_ps={status.get('ollama_ps') or 'unavailable'}\n"
        f"ollama_show_primary_model={status.get('ollama_show_primary_model') or 'unavailable'}\n"
        f"nvidia_smi={status.get('nvidia_smi') or 'unavailable'}\n"
        f"free_h={status.get('free_h') or 'unavailable'}\n"
        "pc_control_allowed=false direct_execution_allowed=false model_download_allowed=false_from_chat"
    )


def _format_memory_history_grounded_answer(user_text: str, context: JarvisBrainContext) -> tuple[str, int]:
    checked = [
        "stable_style_profile",
        "session_memory",
        "local_chat_memory",
        "memory_engine_registry",
        "runtime_history_store",
        "history_query",
        "mempalace_read_only_sandbox",
    ]
    evidence: list[str] = []
    query_terms = _memory_query_terms(user_text)
    if context.rolling_summary.strip():
        evidence.append(f"session_summary: {context.rolling_summary.strip()}")
    for turn in context.recent_turns[-6:]:
        text = str(turn.get("text", "")).strip()
        if text and text != context.user_text.strip():
            evidence.append(f"session_turn/{turn.get('role', '')}: {text[:260]}")
    evidence.extend(context.local_chat_memory_snippets[:4])
    evidence.extend(context.retrieved_snippets[:6])
    if not evidence:
        history_snippets = _retrieve_history_snippets(user_text, deep=True)
        evidence.extend(history_snippets[:6])
    if query_terms:
        evidence = [item for item in evidence if any(term in item.casefold() for term in query_terms)]
    if not evidence:
        return (
            "Не нашёл подтверждение в текущих read-only источниках.\n"
            f"checked_sources={', '.join(checked)}\n"
            "imported_gpt_history=unavailable_or_no_match\n"
            "canonical_memory_write_allowed=false",
            0,
        )
    lines = [
        "Проверил память/историю read-only.",
        f"checked_sources={', '.join(checked)}",
        f"evidence_count={len(evidence)}",
    ]
    lines.extend(f"- {item}" for item in evidence[:8])
    lines.append("canonical_memory_write_allowed=false direct_global_memory_write=false")
    return "\n".join(lines), len(evidence)


def _format_safety_answer() -> str:
    terms = ("runtime_mutation_allowed", "direct_execution_allowed", "approval", "pc_control_allowed", "watchdog", "core guard", "OOB", "safety", "security")
    results: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for term in terms:
        for result in repo_search(term, max_results=8)["results"]:
            key = (str(result["path"]), int(result["line_number"]))
            if key in seen:
                continue
            seen.add(key)
            results.append(result)
            if len(results) >= 30:
                break
        if len(results) >= 30:
            break
    lines = ["Safety/security surfaces read-only:"]
    if results:
        lines.extend(f"- {result['path']}:{result['line_number']}: {result['line']}" for result in results)
    else:
        lines.append("- no direct matches found in bounded search")
    lines.append("direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false")
    return "\n".join(lines)


def _format_action_request_proposal_answer(user_text: str) -> str:
    lowered = user_text.casefold()
    action_family = "generic_action"
    if any(marker in lowered for marker in ("коммит", "commit", "git commit")):
        action_family = "git_commit"
    elif any(marker in lowered for marker in ("тест", "pytest", "провер")):
        action_family = "test_run"
    elif any(marker in lowered for marker in ("скачай", "установ", "install", "download", "n8n", "модель")):
        action_family = "download_or_install"
    elif _asks_pc_action(lowered):
        action_family = "pc_control"
    return (
        "Operator proposal only. Я не буду утверждать, что действие выполнено, пока нет tool_result.\n"
        f"requested_action={user_text.strip()[:240]}\n"
        f"action_family={action_family}\n"
        "execution_allowed=false approval_required=true proposal_only=true\n"
        "allowed_next_step=подготовить patch/plan через существующий capability/approval/action adapter\n"
        "pc_control_allowed=false shell_execution_enabled=false direct_execution_allowed=false "
        "canonical_write_allowed=false deployment_allowed_now=false"
    )


def _format_tool_catalog_answer(catalog: dict[str, Any]) -> str:
    read_only = str(bool(catalog.get("read_only", True))).lower()
    execution_allowed = str(bool(catalog.get("execution_allowed", False))).lower()
    mgrep = catalog.get("mgrep_status", {})
    sqlite_vec = catalog.get("sqlite_vec_status", {})
    qdrant = catalog.get("qdrant_status", {})
    lines = [
        "[work] intent=TOOL_CATALOG "
        "tools=build_jarvis_live_tool_catalog_read_model,inspect_mgrep_readonly_availability,"
        "inspect_sqlite_vec_readonly_availability,inspect_qdrant_readonly_availability "
        f"read_only={read_only} execution_allowed={execution_allowed}",
        "Project / repo read-only:",
    ]
    for tool in catalog.get("project_repo_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            "Retrieval read-only:",
            f"- mgrep_readonly status=read_only usable_now={str(bool(mgrep.get('usable_now', False))).lower()} "
            f"source_present={str(bool(mgrep.get('source_present', False))).lower()} "
            f"effective_status={mgrep.get('selected_tool', 'repo_search')}",
            f"- sqlite_vec_readonly status=read_only usable_now={str(bool(sqlite_vec.get('usable_now', False))).lower()} "
            f"source_present={str(bool(sqlite_vec.get('source_present', False))).lower()} "
            f"effective_status={sqlite_vec.get('selected_tool', 'repo_search')}",
            f"- qdrant_readonly_status status=read_only usable_now={str(bool(qdrant.get('usable_now', False))).lower()} "
            f"source_present={str(bool(qdrant.get('source_present', False))).lower()} "
            f"effective_status={qdrant.get('selected_tool', 'qdrant_readonly_status')}",
            "- retrieval_backend_status_read_model status=available read_only",
            "- retrieval_tool_registry_contract status=available read_only",
            "Memory / history read-only:",
        )
    )
    for tool in catalog.get("memory_history_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            f"- memory_engine_registry status=available read_only definitions={catalog.get('memory_definition_count', 0)}",
            "Model/status read-only:",
        )
    )
    for tool in catalog.get("model_status_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            "Roadmap / safety read-only:",
        )
    )
    for tool in catalog.get("roadmap_safety_read_only_tools", ()):
        lines.append(f"- {tool} status=available read_only")
    lines.extend(
        (
            f"- roadmap_status status=available read_only drift_check_wired={str(bool(catalog.get('all_existing_read_tools_connected', True))).lower()}",
            "Action tools:",
        )
    )
    for tool in catalog.get("action_proposal_only_tools", ()):
        lines.append(f"- {tool} status=proposal_only disabled")
    lines.extend(
        (
            f"mgrep_usable_now={str(bool(mgrep.get('usable_now', False))).lower()}",
            f"sqlite_vec_usable_now={str(bool(sqlite_vec.get('usable_now', False))).lower()}",
            f"qdrant_server_runtime_enabled={str(bool(catalog.get('qdrant_server_runtime_enabled', False))).lower()}",
            f"active_retrieval_surfaces={_csv(catalog.get('active_retrieval_surfaces', ())) or 'none'}",
            f"sandbox_only_memory_surfaces={_csv(catalog.get('sandbox_only_memory_surfaces', ())) or 'none'}",
            f"disabled_memory_surfaces={_csv(catalog.get('disabled_memory_surfaces', ())) or 'none'}",
            f"enterprise_memory_preview_ready={str(bool(catalog.get('enterprise_memory_preview_ready', False))).lower()}",
            f"regulatory_routing_preview_ready={str(bool(catalog.get('regulatory_routing_preview_ready', False))).lower()}",
            f"mempalace_routing_ready={str(bool(catalog.get('mempalace_routing_ready', False))).lower()}",
            "direct_execution_allowed=false",
            "canonical_write_allowed=false",
            "pc_control_allowed=false",
            "shell_execution_enabled=false",
            "direct_execution_allowed=false",
            "execution_allowed=false",
        )
    )
    return "\n".join(lines)


def _format_project_atlas_answer() -> str:
    model = build_project_workspace_read_model()
    groups = model["domain_groups"]
    lines = [
        "Не буду dump'ить весь репозиторий в один ответ. Даю read-only atlas и команды пагинации.",
        f"project_root={model['project_root']}",
        f"tracked_file_count={model['tracked_file_count']}",
    ]
    for group, paths in groups.items():
        if paths:
            lines.append(f"- {group}: {len(paths)} files; sample={', '.join(paths[:5])}")
    lines.extend((
        "Дальше смотри страницами:",
        "/project files 1",
        "/project files 2",
        "/project search <term>",
        "/project file <path> <page>",
    ))
    return "\n".join(lines)


def _format_project_help() -> str:
    return (
        "Project commands: /project, /project status, /project tree, /project files <page>, "
        "/project dirty, /project search <query>, /project file <path> <page>, "
        "/project outline <path>, /project imports <path>, /project tests, /project roadmap, "
        "/project models, /project safety"
    )


def _answer_project_workspace_summary_if_grounded(context: JarvisBrainContext) -> str:
    if not _asks_project_workspace_summary(context.user_text.casefold()):
        return ""
    tracked = _tracked_project_files()
    top_entries = _top_level_entries_from_tracked_files(tracked) if tracked else ()
    visible_top = tuple(
        entry.rstrip("/")
        for entry in top_entries
        if entry.rstrip("/") in {"CONTROL_PLANE", "MAKSIMAR_SERVER", "MAKSIMAR_CORE_LIB", "tools", "tests", "runtime_history_store"}
    )
    if not visible_top:
        visible_top = ("CONTROL_PLANE", "MAKSIMAR_SERVER", "MAKSIMAR_CORE_LIB", "tools", "tests")
    canonical_files = tuple(path for path in PROJECT_VISIBILITY_KEY_FILES if (PROJECT_ROOT / path).exists())
    if not canonical_files:
        return ""
    chain = (
        "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py -> "
        "CONTROL_PLANE/api_server.py -> "
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py -> "
        "tools/jarvis_live_runtime/jarvis_live_brain_loop.py -> Ollama"
    )
    support_files = (
        "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py, "
        "tools/jarvis_live_runtime/jarvis_live_identity_prompt.py, "
        "tools/jarvis_live_runtime/jarvis_live_response_mode.py"
    )
    tracked_text = f"; tracked_file_count={len(tracked)}" if tracked else ""
    return (
        "Да, брат, вижу проект в read-only режиме. "
        f"Корень: {PROJECT_ROOT}{tracked_text}. "
        f"По верхнему уровню вижу: {', '.join(visible_top)}. "
        f"Ядро terminal chat сейчас идет так: {chain}. "
        f"За интерфейс, стиль и режимы ответа отвечают: {support_files}. "
        "Я могу читать дерево проекта и bounded snippets файлов, но не пишу в ядро, "
        "не выполняю команды и не управляю ПК: "
        "project_workspace_read_enabled=true, project_tree_read_enabled=true, "
        "project_file_read_enabled=true, direct_execution_allowed=false, "
        "canonical_write_allowed=false, pc_control_allowed=false."
    )


def _asks_project_workspace_summary(lowered: str) -> bool:
    project_markers = (
        "структур",
        "дерево",
        "что ты видишь по проекту",
        "ядро terminal chat",
        "terminal chat chain",
        "project workspace",
        "файлы проекта",
        "структура ядра",
    )
    return any(marker in lowered for marker in project_markers)


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


def _extract_semantic_similarity_query(user_text: str) -> str:
    text = user_text.strip()
    lowered = text.casefold()
    patterns = (
        r"^(?:найди\s+)?похож[еаы]?[йя]?\s+на\s+",
        r"^семантически\s+",
        r"^по\s+смыслу\s+",
        r"^semantic\s+similarity\s+",
        r"^semantic\s+",
        r"^similar\s+to\s+",
        r"^related\s+to\s+",
        r"^similar\s+",
    )
    for pattern in patterns:
        candidate = re.sub(pattern, "", text, flags=re.IGNORECASE).strip(" ,.;:!?-")
        if candidate != text and candidate:
            return candidate
    for trigger in ("найди похожее на", "похожее на", "похожие на"):
        if trigger in lowered:
            index = lowered.index(trigger) + len(trigger)
            candidate = text[index:].strip(" ,.;:!?-")
            if candidate:
                return candidate
    return _semantic_search_query(user_text)


def _asks_memory_history_question(lowered: str) -> bool:
    memory_markers = (
        "что мы обсуждали",
        "что обсуждали",
        "что я говорил",
        "что я просил",
        "что было в переписке",
        "переписке с gpt",
        "gpt",
        "история",
        "history",
        "помнишь",
        "что ты помнишь",
        "загружен",
        "загрузили",
    )
    topic_markers = ("голос", "voice", "проект", "n8n", "roadmap", "роадмап", "gpt")
    return any(marker in lowered for marker in memory_markers) and (
        any(marker in lowered for marker in topic_markers) or "что я" in lowered
    )


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


def _semantic_search_query(user_text: str) -> str:
    lowered = user_text.casefold()
    filename = _extract_filename_token(user_text)
    if filename:
        return filename
    direct_queries = (
        ("source_ref", "source_ref"),
        ("source-ref", "source_ref"),
        ("source ref", "source_ref"),
        ("evidence_binding", "evidence_binding"),
        ("evidence-binding", "evidence_binding"),
        ("evidence binding", "evidence_binding"),
        ("source_of_truth", "source_of_truth"),
        ("network_allowed_by_default", "network_allowed_by_default"),
        ("runtime_mutation_allowed", "runtime_mutation_allowed"),
        ("direct_execution_allowed", "direct_execution_allowed"),
        ("vendor_gate_required", "vendor_gate_required"),
    )
    for marker, query in direct_queries:
        if marker in lowered:
            return query
    known_queries = (
        ("terminal chat", "terminal_chat jarvis_live_terminal_chat"),
        ("brain_loop", "jarvis_live_brain_loop"),
        ("n8n", "n8n adapter vendor gate sandbox"),
        ("голос", "voice jarvis live voice"),
        ("voice", "voice jarvis live voice"),
        ("памят", "memory local_chat runtime_history_store"),
        ("memory", "memory local_chat runtime_history_store"),
        ("core guard", "core guard watchdog safety"),
        ("watchdog", "watchdog core guard safety"),
        ("ollama", "ollama qwen model runtime"),
        ("qwen", "ollama qwen model runtime"),
        ("tool", "tool adapter capability approval"),
        ("adapter", "adapter capability approval"),
        ("адаптер", "adapter capability approval"),
        ("автоматизац", "workflow automation n8n adapter"),
        ("retrieval", "retrieval_backend retrieval tool contract status read model"),
        ("qdrant", "qdrant_adapter_contract qdrant_server_required_now qdrant_container_enabled"),
        ("sqlite", "sqlite_vec_adapter_contract sqlite_vec_readonly"),
        ("mgrep", "mgrep_adapter_contract mgrep_readonly"),
        ("source_ref", "source_ref evidence_binding evidence_id trace_id"),
        ("evidence", "source_ref evidence_binding evidence_id trace_id"),
        ("container", "container_contract runtime_profile runtime_enabled docker_required_now"),
        ("docker", "container_contract runtime_profile docker_required_now"),
        ("vendor", "vendor_gate retrieval_backend_manifest vendor_quarantine"),
    )
    for marker, query in known_queries:
        if marker in lowered:
            return query
    cleaned = user_text.strip()
    return cleaned[:120] if cleaned else "jarvis"


def _project_path_matches(query: str, max_results: int = 20) -> tuple[str, ...]:
    terms = tuple(term for term in _query_tokens(query) if term not in {"где", "найди", "поиск"})
    if not terms:
        return ()
    matches: list[str] = []
    for path in _tracked_project_files():
        lowered = path.casefold()
        if any(term in lowered for term in terms):
            matches.append(path)
        if len(matches) >= max_results:
            break
    return tuple(matches)


def _memory_query_terms(user_text: str) -> tuple[str, ...]:
    ignored = {
        "джарвис",
        "jarvis",
        "помнишь",
        "обсуждали",
        "переписке",
        "переписка",
        "говорил",
        "просил",
        "было",
        "были",
        "что",
        "про",
        "мой",
        "моя",
    }
    terms = [term for term in _query_tokens(user_text) if term not in ignored]
    if "голос" in terms and "voice" not in terms:
        terms.append("voice")
    if "gpt" in user_text.casefold() and "gpt" not in terms:
        terms.append("gpt")
    return tuple(dict.fromkeys(terms))


def _answer_style_memory_recall_if_grounded(context: JarvisBrainContext) -> str:
    lowered = context.user_text.casefold()
    if not _asks_style_memory_recall(lowered):
        return ""
    profile = context.stable_style_profile
    relation = str(profile.get("relation_style", "")).strip()
    communication = str(profile.get("communication_style", "")).strip()
    avoid = str(profile.get("avoid", "")).strip()
    concise_rule = str(profile.get("concise_rule", "")).strip()
    stored_style = " ".join((relation, communication, avoid, concise_rule, context.rolling_summary, *context.local_chat_memory_snippets)).casefold()
    if not any(marker in stored_style for marker in ("брат", "напарник", "гараж", "not template-like", "шаблон")):
        return ""
    return (
        "Да, брат, помню. Ты хочешь, чтобы я был не сухим помощником, "
        "а JARVIS-напарником по гаражу: говорил прямо, живо, по делу, "
        "не слишком коротко и без шаблонных концовок с дежурным предложением помощи. "
        "Буду держать этот стиль в следующих сессиях."
    )


def _asks_style_memory_recall(lowered: str) -> bool:
    recall_markers = ("помнишь", "ты помнишь", "напомни", "как я хочу", "какой стиль")
    style_markers = ("общал", "общаться", "стиль", "говорил", "говорить", "отвечал", "отвечать")
    return any(marker in lowered for marker in recall_markers) and any(marker in lowered for marker in style_markers)


def _asks_memory_recall(lowered: str) -> bool:
    return any(marker in lowered for marker in ("помнишь", "ты помнишь", "что я говорил", "что я просил"))


def _has_stored_memory_for_recall(context: JarvisBrainContext) -> bool:
    previous_turns = [
        turn
        for turn in context.recent_turns
        if str(turn.get("text", "")).strip() and str(turn.get("text", "")).strip() != context.user_text.strip()
    ]
    return bool(previous_turns or context.local_chat_memory_snippets or context.rolling_summary.strip())


def _retrieve_memory_federation_snippets(
    user_text: str,
    deep: bool,
    enabled: bool = True,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not enabled:
        return (), ("session_memory",)

    snippets: list[str] = []
    surfaces_used: list[str] = []

    history_snippets = _retrieve_history_snippets(user_text, deep=deep)
    if history_snippets:
        snippets.extend(history_snippets)
        surfaces_used.append("runtime_history_store")

    project_snippets = _retrieve_project_workspace_snippets(user_text, deep=deep)
    if project_snippets:
        snippets.extend(project_snippets)
        surfaces_used.append("project_workspace_read_model")

    memory_engine_snippets = _retrieve_memory_engine_snippets(user_text)
    if memory_engine_snippets:
        snippets.extend(memory_engine_snippets)
        surfaces_used.append("memory_engine_registry")

    enterprise_snippets = _retrieve_enterprise_memory_snippets(user_text)
    if enterprise_snippets:
        snippets.extend(enterprise_snippets)
        surfaces_used.append("enterprise_business_memory")

    regulatory_snippets = _retrieve_regulatory_memory_snippets(user_text)
    if regulatory_snippets:
        snippets.extend(regulatory_snippets)
        surfaces_used.append("regulatory_memory_foundation")

    vector_snippets = _retrieve_vector_memory_snippets(user_text)
    if vector_snippets:
        snippets.extend(vector_snippets)
        surfaces_used.append("vector_runtime_indexes")

    mempalace_snippets = _retrieve_mempalace_status_snippets(user_text)
    if mempalace_snippets:
        snippets.extend(mempalace_snippets)
        surfaces_used.append("mempalace_read_only_sandbox")

    return tuple(snippets[:10]), tuple(dict.fromkeys(surfaces_used))


def _retrieve_history_snippets(user_text: str, deep: bool) -> list[str]:
    snippets: list[str] = []
    try:
        query = JarvisHistoryQuery(
            query_text=user_text,
            query_scope="project_history",
            query_ready=True,
        )
        result = run_jarvis_history_query(query)
        titles = tuple(str(title) for title in result.get("matched_titles", ()))
        snippets.extend(f"history_query_match: {title}" for title in titles[:3])
    except (ValueError, KeyError, TypeError):
        pass
    if not RUNTIME_HISTORY_STORE.exists():
        return snippets
    tokens = _query_tokens(user_text)
    records = sorted(RUNTIME_HISTORY_STORE.glob("normalized_history/conversations/*/normalized_record.json"))
    for record_path in records[:120]:
        try:
            text = record_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lowered = text.casefold()
        if tokens and not any(token in lowered for token in tokens):
            continue
        snippets.append(_compact_text(text, source=record_path))
        if len(snippets) >= (6 if deep else 3):
            break
    return snippets


def _retrieve_project_workspace_snippets(user_text: str, deep: bool) -> list[str]:
    if not _needs_project_visibility(user_text):
        return []
    snippets = [_project_tree_summary()]
    for path in _select_project_files_for_context(user_text, deep=deep):
        snippet = _read_project_file_snippet(path)
        if snippet:
            snippets.append(snippet)
        if len(snippets) >= MAX_PROJECT_FILE_SNIPPETS + 1:
            break
    return snippets


def _parse_git_status_short(status_short: str) -> dict[str, tuple[str, ...]]:
    dirty: list[str] = []
    untracked: list[str] = []
    staged: list[str] = []
    for line in status_short.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:].strip() if len(line) > 3 else line.strip()
        if code == "??":
            untracked.append(path)
            continue
        if code[0].strip():
            staged.append(path)
        if code[1].strip():
            dirty.append(path)
    return {"dirty_files": tuple(dirty), "untracked_files": tuple(untracked), "staged_files": tuple(staged)}


def _important_paths_detected(paths: tuple[str, ...]) -> tuple[str, ...]:
    markers = (
        "CONTROL_PLANE/api_server.py",
        "jarvis_live_brain_loop.py",
        "jarvis_live_terminal_chat.py",
        "jarvis_live_chat_launcher.py",
        "jarvis_live_response_mode.py",
        "jarvis_live_identity_prompt.py",
        "jarvis_live_ci_status.py",
        "roadmap_post_step_drift_check.py",
    )
    return tuple(path for path in paths if any(marker in path for marker in markers))[:80]


def _domain_groups_for_paths(paths: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = {
        "CONTROL_PLANE": [],
        "MAKSIMAR_CORE_LIB": [],
        "MAKSIMAR_SERVER": [],
        "AI_SERVICES": [],
        "tools": [],
        "tests": [],
        "runtime_history_store": [],
        "memory/history": [],
        "regulatory memory": [],
        "proposal/audit/approval": [],
        "security/safety/execution control": [],
        "core guard / watchdog / OOB / runtime truth": [],
        "JARVIS terminal runtime": [],
        "Ollama/model/Qwen/runtime model layer": [],
        "mobile/app/chat/sync": [],
        "dashboards/read-only views": [],
        "roadmap/check/CI tools": [],
        "external/vendor": [],
        "unknown/other": [],
    }
    for path in paths:
        lowered = path.casefold()
        matched = False
        for prefix in ("CONTROL_PLANE", "MAKSIMAR_CORE_LIB", "MAKSIMAR_SERVER", "AI_SERVICES", "tools", "tests", "runtime_history_store"):
            if path.startswith(prefix + "/") or path == prefix:
                groups[prefix].append(path)
                matched = True
        keyword_groups = (
            ("memory/history", ("memory", "history", "runtime_history")),
            ("regulatory memory", ("regulatory", "jurisdiction", "compliance")),
            ("proposal/audit/approval", ("proposal", "audit", "approval")),
            ("security/safety/execution control", ("security", "safety", "execution_control", "admission", "allowlist")),
            ("core guard / watchdog / OOB / runtime truth", ("core_guard", "watchdog", "oob", "runtime_truth", "truth")),
            ("JARVIS terminal runtime", ("jarvis_live_runtime", "terminal_chat", "brain_loop", "chat_launcher")),
            ("Ollama/model/Qwen/runtime model layer", ("ollama", "qwen", "model", "ai_orchestration")),
            ("mobile/app/chat/sync", ("mobile", "android", "ios", "chat", "sync")),
            ("dashboards/read-only views", ("dashboard", "read_only", "panel")),
            ("roadmap/check/CI tools", ("roadmap", "ci_status", "drift_check", "readiness")),
            ("external/vendor", ("external", "vendor", "mempalace")),
        )
        for group, markers in keyword_groups:
            if any(marker in lowered for marker in markers):
                groups[group].append(path)
                matched = True
        if not matched:
            groups["unknown/other"].append(path)
    return {key: tuple(value[:80]) for key, value in groups.items()}


def _repo_search_with_rg(query: str, paths: tuple[str, ...], max_results: int) -> list[dict[str, Any]]:
    if shutil.which("rg") is None:
        return []
    command = ["rg", "-n", "--no-heading", "--fixed-strings", "--max-count", "3", query]
    command.extend(paths or ["."])
    output = _run_read_only_command(tuple(command))
    results: list[dict[str, Any]] = []
    for line in output.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        path, line_number, matched = parts
        if not _safe_project_path(path):
            continue
        results.append({"path": path, "line_number": _parse_int(line_number, 0), "line": matched.strip()[:300]})
        if len(results) >= max_results:
            break
    return results


def _repo_search_with_python(query: str, paths: tuple[str, ...], max_results: int) -> list[dict[str, Any]]:
    lowered = query.casefold()
    candidates = paths or _tracked_project_files()
    results: list[dict[str, Any]] = []
    for path in candidates:
        if not _safe_project_path(path) or not _is_safe_project_text_path(path):
            continue
        full_path = PROJECT_ROOT / path
        try:
            lines = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            if lowered in line.casefold():
                results.append({"path": path, "line_number": line_number, "line": line.strip()[:300]})
                break
        if len(results) >= max_results:
            break
    return results


def _safe_project_path(path: str) -> bool:
    candidate = (PROJECT_ROOT / path).resolve()
    try:
        candidate.relative_to(PROJECT_ROOT)
    except ValueError:
        return False
    return not _is_excluded_project_path(str(candidate.relative_to(PROJECT_ROOT)))


def _project_tree_summary() -> str:
    tracked = _tracked_project_files()
    if tracked:
        top_entries = _top_level_entries_from_tracked_files(tracked)
        selected = tracked[:MAX_PROJECT_TREE_ENTRIES]
        return (
            "project_workspace_read_model: "
            f"project_root={PROJECT_ROOT}; "
            f"tracked_file_count={len(tracked)}; "
            f"top_level={', '.join(top_entries[:40])}; "
            f"sample_tracked_files={', '.join(selected[:30])}; "
            "read_only=true; direct_execution_allowed=false; canonical_write_allowed=false"
        )
    top_entries = [
        path.name + ("/" if path.is_dir() else "")
        for path in sorted(PROJECT_ROOT.iterdir(), key=lambda item: item.name.casefold())
        if path.name not in PROJECT_VISIBILITY_EXCLUDED_DIRS
    ][:40]
    return (
        "project_workspace_read_model: "
        f"project_root={PROJECT_ROOT}; tracked_file_count=unknown; "
        f"top_level={', '.join(top_entries)}; "
        "read_only=true; direct_execution_allowed=false; canonical_write_allowed=false"
    )


def _tracked_project_files() -> tuple[str, ...]:
    output = _run_read_only_command(("git", "ls-files"))
    if output:
        return tuple(
            line.strip()
            for line in output.splitlines()
            if line.strip() and not _is_excluded_project_path(line.strip())
        )
    paths: list[str] = []
    for path in PROJECT_ROOT.rglob("*"):
        if len(paths) >= 2000:
            break
        if path.is_dir() or _is_excluded_project_path(str(path.relative_to(PROJECT_ROOT))):
            continue
        paths.append(str(path.relative_to(PROJECT_ROOT)))
    return tuple(sorted(paths))


def _top_level_entries_from_tracked_files(paths: tuple[str, ...]) -> tuple[str, ...]:
    entries: list[str] = []
    seen: set[str] = set()
    for path in paths:
        first = path.split("/", 1)[0]
        if first in seen:
            continue
        seen.add(first)
        entries.append(first + ("/" if "/" in path else ""))
    return tuple(entries)


def _select_project_files_for_context(user_text: str, deep: bool) -> tuple[Path, ...]:
    tokens = _query_tokens(user_text)
    selected: list[str] = []
    tracked = _tracked_project_files()
    for key_file in PROJECT_VISIBILITY_KEY_FILES:
        if key_file in tracked or (PROJECT_ROOT / key_file).exists():
            selected.append(key_file)
    for path in tracked:
        if len(selected) >= (MAX_PROJECT_FILE_SNIPPETS * 3 if deep else MAX_PROJECT_FILE_SNIPPETS):
            break
        lowered = path.casefold()
        if tokens and not any(token in lowered for token in tokens):
            continue
        if path not in selected:
            selected.append(path)
    return tuple(PROJECT_ROOT / path for path in selected if _is_safe_project_text_path(path))


def _read_project_file_snippet(path: Path) -> str:
    try:
        relative = path.relative_to(PROJECT_ROOT)
    except ValueError:
        return ""
    relative_text = str(relative)
    if _is_excluded_project_path(relative_text) or not _is_safe_project_text_path(relative_text):
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    compact = " ".join(text.split())
    return (
        "project_file_snippet: "
        f"path={relative_text}; bytes_read_limit={MAX_PROJECT_FILE_BYTES}; "
        f"content={compact[:MAX_PROJECT_FILE_BYTES]}"
    )


def _is_excluded_project_path(path: str) -> bool:
    parts = Path(path).parts
    return any(part in PROJECT_VISIBILITY_EXCLUDED_DIRS for part in parts)


def _is_safe_project_text_path(path: str) -> bool:
    suffix = Path(path).suffix.casefold()
    if suffix in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".tar", ".gz", ".sqlite", ".db"}:
        return False
    return True


def _retrieve_memory_engine_snippets(user_text: str) -> list[str]:
    tokens = _query_tokens(user_text)
    try:
        definitions = list_memory_definitions()
    except Exception:
        return []
    snippets: list[str] = []
    for definition in definitions[:300]:
        entity_id = str(getattr(definition, "entity_id", ""))
        if tokens and not any(token in entity_id.casefold() for token in tokens):
            continue
        version = str(getattr(definition, "version", ""))
        snippets.append(f"memory_engine_registry: entity_id={entity_id}; version={version}")
        if len(snippets) >= 3:
            break
    return snippets


def _retrieve_enterprise_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("суверенн", "sovereign", "business", "sales", "продаж", "enterprise", "tenant")):
        return []
    try:
        preview = build_enterprise_memory_preview()
    except Exception:
        return []
    return [
        "enterprise_business_memory: "
        f"preview_ready={preview.get('preview_ready')}; "
        f"tenant_scopes={preview.get('tenant_scopes')}; "
        f"business_ids={preview.get('business_ids')}; "
        f"policy_record_ids={preview.get('policy_record_ids')}; "
        f"runtime_policy_binding_allowed={preview.get('runtime_policy_binding_allowed')}; "
        "read_only=true"
    ]


def _retrieve_regulatory_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("закон", "law", "regulatory", "compliance", "юрисдик", "jurisdiction", "tenant")):
        return []
    try:
        preview = build_regulatory_routing_preview()
    except Exception:
        return []
    return [
        "regulatory_memory_foundation: "
        f"preview_ready={preview.get('preview_ready')}; "
        f"route_count={preview.get('route_count')}; "
        f"tenant_scope_required={preview.get('tenant_scope_required')}; "
        f"jurisdiction_scope_required={preview.get('jurisdiction_scope_required')}; "
        f"read_only={preview.get('read_only')}; "
        f"runtime_mutation_allowed={preview.get('runtime_mutation_allowed')}; "
        f"direct_core_write_allowed={preview.get('direct_core_write_allowed')}"
    ]


def _retrieve_vector_memory_snippets(user_text: str) -> list[str]:
    lowered = user_text.casefold()
    if not any(marker in lowered for marker in ("vector", "embedding", "индекс", "retrieval", "rag")):
        return []
    existing_roots = tuple(
        str(path)
        for path in (RUNTIME_VECTOR_INDEX_ROOT, RUNTIME_EMBEDDINGS_ROOT, RUNTIME_RETRIEVAL_ROOT)
        if path.exists()
    )
    if not existing_roots:
        return []
    return [
        "vector_memory: runtime vector/embedding roots detected; "
        f"roots={existing_roots}; query_helper=not_connected; canonical_write_allowed=false"
    ]


def _retrieve_mempalace_status_snippets(user_text: str) -> list[str]:
    if "mempalace" not in user_text.casefold():
        return []
    status = _mempalace_status()
    try:
        preview = build_mempalace_read_only_routing_integration_preview()
    except Exception:
        preview = {}
    return [
        "mempalace_read_only_sandbox: "
        f"status={status}; "
        f"read_only_routing_enabled={preview.get('read_only_routing_enabled', False)}; "
        f"routing_integration_ready={preview.get('routing_integration_ready', False)}; "
        f"canonical_write_allowed={preview.get('canonical_write_allowed', False)}; "
        f"runtime_mutation_allowed={preview.get('runtime_mutation_allowed', False)}; "
        f"query_domains={preview.get('query_domains', ())}"
    ]


def _retrieve_local_chat_memory_snippets(user_text: str, state: dict[str, Any]) -> tuple[str, ...]:
    snippets: list[str] = []
    tokens = _query_tokens(user_text)
    rolling_summary = str(state.get("rolling_summary", "")).strip()
    if rolling_summary:
        snippets.append(f"session_summary: {rolling_summary[:500]}")
    for record in _read_recent_local_chat_records(limit=24):
        text = " ".join(
            str(record.get(key, ""))
            for key in ("user_message", "jarvis_answer", "turn_summary", "active_task")
        ).casefold()
        if tokens and not any(token in text for token in tokens):
            continue
        snippets.append(
            "local_chat_memory: "
            f"day={record.get('day_bucket', '')}; "
            f"user={str(record.get('user_message', ''))[:180]}; "
            f"jarvis={str(record.get('jarvis_answer', ''))[:180]}"
        )
        if len(snippets) >= MAX_LOCAL_CHAT_MEMORY_SNIPPETS:
            break
    return tuple(snippets[:MAX_LOCAL_CHAT_MEMORY_SNIPPETS])


def _build_memory_surface_inventory() -> tuple[dict[str, Any], ...]:
    return (
        _surface("session_memory", "session-runtime", str(SESSION_STATE_PATH), "usable_now", ()),
        _surface("local_chat_memory", "append-only local chat/session memory", str(_session_turn_log_path()), "usable_now" if _session_turn_log_path().exists() else "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_memory_federation_smoke.py",)),
        _surface("project_workspace_read_model", "read-only project tree and bounded file snippets", str(PROJECT_ROOT), "usable_now", ("tests/jarvis_live_runtime/test_jarvis_live_brain_loop_context_smoke.py",)),
        _surface("runtime_history_store", "read-only retrieval", str(RUNTIME_HISTORY_STORE), "usable_now" if RUNTIME_HISTORY_STORE.exists() else "not_connected", ("tests/memory_engine/test_jarvis_history_query_reader_smoke.py",)),
        _surface("memory_engine_registry", "canonical/read-only retrieval", "MAKSIMAR_CORE_LIB/memory_engine", "usable_now", ("tests/memory_engine/test_memory_loader_smoke.py",)),
        _surface("vector_runtime_indexes", "vector", str(RUNTIME_VECTOR_INDEX_ROOT), "usable_now" if RUNTIME_VECTOR_INDEX_ROOT.exists() else "not_connected", ("tests/storage_registry/test_retrieval_index_reference_models_smoke.py",)),
        _surface("enterprise_business_memory", "business-sales", "MAKSIMAR_CORE_LIB/enterprise_memory_domains", "usable_now", ("tests/governance_federation_gap/test_memory_federation_policy_models_smoke.py",)),
        _surface("regulatory_memory_foundation", "regulatory", "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION", "usable_now", ("tests/regulatory_memory_foundation/test_regulatory_routing_acceptance_smoke.py",)),
        _surface("mempalace_read_only_sandbox", "external-vendor", "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters/mempalace_read_only_routing_integration.py", "sandbox_only", ("tests/memory_routing_adapters/test_mempalace_read_only_routing_integration_smoke.py",)),
        _surface("dashboard_memory_read_models", "dashboard-read-model", "MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS", "read_only", ("tests/final_memory_map/test_final_memory_summary_builder_smoke.py",)),
    )


def _surface(
    surface_id: str,
    surface_type: str,
    path: str,
    status: str,
    existing_tests: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "surface_id": surface_id,
        "path": path,
        "type": surface_type,
        "status": status,
        "existing_tests": existing_tests,
        "forbidden_direct_write": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


def _mempalace_status() -> str:
    try:
        preview = build_mempalace_read_only_routing_integration_preview()
    except Exception:
        return "not_connected"
    if preview.get("routing_integration_ready") is True and preview.get("read_only_routing_enabled") is True:
        return "sandbox_only_read_only"
    return "sandbox_only_manual_review_required"


def _project_status_summary() -> str:
    branch = _run_read_only_command(("git", "branch", "--show-current"))
    status = _run_read_only_command(("git", "status", "--short"))
    tracked = _tracked_project_files()
    top_entries = _top_level_entries_from_tracked_files(tracked) if tracked else ()
    key_files = tuple(path for path in PROJECT_VISIBILITY_KEY_FILES if (PROJECT_ROOT / path).exists())
    history_exists = RUNTIME_HISTORY_STORE.exists()
    return (
        f"project_root={PROJECT_ROOT}; branch={branch or 'unknown'}; "
        f"git_status_short={status[:500] if status else 'clean_or_unavailable'}; "
        f"tracked_file_count={len(tracked) if tracked else 'unknown'}; "
        f"top_level={', '.join(top_entries[:40])}; "
        f"canonical_chat_path_files={', '.join(key_files)}; "
        f"runtime_history_store={RUNTIME_HISTORY_STORE}; "
        f"runtime_history_store_exists={str(history_exists).lower()}; "
        "project_workspace_read_enabled=true; project_file_read_enabled=true; "
        "pc_control_allowed=false; canonical_write_allowed=false; direct_execution_allowed=false"
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
    SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
    state.update(_memory_enablement_flags())
    state["session_memory_path"] = str(SESSION_STATE_PATH)
    state["local_chat_memory_path"] = str(_session_turn_log_path())
    state["canonical_memory_write_allowed"] = False
    state["pc_control_allowed"] = False
    SESSION_STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )


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
    normalized["memory_truth_split"] = _memory_truth_split()
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
        "memory_truth_split_enabled": True,
        "session_memory_write_enabled": True,
        "runtime_history_append_enabled": False,
        "conversation_history_append_enabled": True,
        "chat_transcript_append_enabled": True,
        "chat_memory_write_enabled": True,
    }


def _memory_truth_split() -> dict[str, str]:
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


def _route_mode(text: str) -> str:
    return _plan_jarvis_request(text)["route_mode"]


def _plan_jarvis_request(text: str) -> dict[str, str]:
    lowered = text.casefold()
    if _asks_pc_action(lowered):
        return {
            "request_route": "pc_action_proposal",
            "route_mode": "FAST",
            "retrieval_mode": "session_only",
        }
    if _asks_weather_or_current_facts(lowered):
        return {
            "request_route": "current_facts_tool",
            "route_mode": "FAST",
            "retrieval_mode": "session_only",
        }
    if _is_deep_code_request(lowered):
        return {
            "request_route": "code_deep",
            "route_mode": "DEEP",
            "retrieval_mode": "deep_memory",
        }
    if _is_simple_code_request(lowered):
        return {
            "request_route": "code_simple",
            "route_mode": "DEEP",
            "retrieval_mode": "targeted_memory",
        }
    if _needs_deep_memory(lowered):
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


def _needs_deep_memory(lowered: str) -> bool:
    deep_markers = (
        "проект",
        "структур",
        "дерево",
        "файл",
        "файлы",
        "содержим",
        "ядро",
        "repo",
        "repository",
        "workspace",
        "source",
        "исходник",
        "memory",
        "память",
        "history",
        "runtime_history_store",
        "код",
        "статус",
        "ошибка",
        "тест",
        "git",
        "architecture",
        "архитектур",
        "approval gate",
        "суверенн",
        "business",
        "sales",
        "продаж",
        "enterprise",
        "закон",
        "regulatory",
        "compliance",
        "mempalace",
        "vector",
        "embedding",
        "обсуждали",
        "переписк",
        "gpt",
        "голос",
        "voice",
        "n8n",
        "tool",
        "adapter",
        "адаптер",
        "автоматизац",
    )
    return any(marker in lowered for marker in deep_markers)


def _needs_project_visibility(text: str) -> bool:
    lowered = text.casefold()
    markers = (
        "проект",
        "структур",
        "дерево",
        "файл",
        "файлы",
        "содержим",
        "ядро",
        "repo",
        "repository",
        "workspace",
        "source",
        "исходник",
        "код",
        "control_plane",
        "brain_loop",
        "terminal_chat",
    )
    return any(marker in lowered for marker in markers)


def _is_simple_code_request(lowered: str) -> bool:
    markers = ("pytest", "brokenpipeerror", "ошибка", "traceback", "код", "тест", "python")
    return any(marker in lowered for marker in markers)


def _is_deep_code_request(lowered: str) -> bool:
    markers = ("architecture", "архитектур", "сложн", "complex", "approval gate", "patch proposal")
    return any(marker in lowered for marker in markers) and _is_simple_code_request(lowered)


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


def _asks_weather_or_current_facts(lowered: str) -> bool:
    return any(marker in lowered for marker in ("погода", "курс", "новости", "сейчас в интернете", "поиск"))


def _asks_pc_action(lowered: str) -> bool:
    return any(marker in lowered for marker in ("открой", "запусти", "клик", "напечатай", "управляй", "выключи пк"))


def _asks_permanent_memory_write(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "запиши это в постоянную память",
            "сохрани в постоянную память",
            "canonical memory",
            "global memory",
            "запомни навсегда",
        )
    )


def _sanitize_model_output(text: str) -> str:
    return clean_voice_response(text)


def _filter_reasoning_chunk(chunk: str, state: dict[str, bool]) -> str:
    text = chunk
    visible = ""
    while text:
        lowered = text.casefold()
        if state.get("inside_reasoning", False):
            end_positions = [
                pos
                for marker in ("</think>", "</thinking>")
                if (pos := lowered.find(marker)) != -1
            ]
            if not end_positions:
                return visible
            end = min(end_positions)
            marker = "</think>" if lowered.startswith("</think>", end) else "</thinking>"
            text = text[end + len(marker) :]
            state["inside_reasoning"] = False
            continue
        start_positions = [
            pos
            for marker in ("<think>", "<thinking>", "thinking:", "reasoning:", "мысли:", "рассуждение:")
            if (pos := lowered.find(marker)) != -1
        ]
        if not start_positions:
            visible += text
            break
        start = min(start_positions)
        visible += text[:start]
        if lowered.startswith("thinking:", start) or lowered.startswith("reasoning:", start) or lowered.startswith("мысли:", start) or lowered.startswith("рассуждение:", start):
            paragraph_end = text.find("\n\n", start)
            if paragraph_end == -1:
                return visible
            text = text[paragraph_end + 2 :]
            continue
        state["inside_reasoning"] = True
        text = text[start:]
    return visible


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(part for part in text.casefold().replace("?", " ").replace(",", " ").split() if len(part) >= 4)


def _compact_text(text: str, source: Path) -> str:
    single_line = " ".join(text.split())
    return f"{source}: {single_line[:700]}"


def _format_section(title: str, value: str) -> str:
    return f"{title}:\n{value}" if value else ""


def _format_turns(turns: tuple[dict[str, str], ...]) -> str:
    if not turns:
        return ""
    lines = [f"- {turn.get('role')}: {turn.get('text')}" for turn in turns]
    return "RECENT_SESSION_TURNS:\n" + "\n".join(lines)


def _format_list(title: str, values: tuple[str, ...]) -> str:
    if not values:
        return ""
    return title + ":\n" + "\n".join(f"- {value}" for value in values)


def _format_style_profile(profile: dict[str, str]) -> str:
    if not profile:
        return ""
    lines = [f"- {key}: {value}" for key, value in profile.items()]
    return "STABLE_STYLE_PROFILE:\n" + "\n".join(lines)


def _format_style_memory_answer_rules() -> str:
    return (
        "STYLE_MEMORY_ANSWER_RULES:\n"
        "- If the user asks how they want you to communicate, answer from STABLE_STYLE_PROFILE/local_chat_memory directly.\n"
        "- Final answer must mention the actual stored style facts instead of a generic helper phrase.\n"
        "- Do not answer style/preference recall with 'Скажи, что нужно' or 'Нужна помощь?'.\n"
        "- If local_chat_memory/session_summary contains the answer, answer from it directly and keep it grounded."
    )


def _format_memory_truth_split() -> str:
    split = _memory_truth_split()
    lines = [f"- {key}: {value}" for key, value in split.items()]
    return (
        "MEMORY_TRUTH_SPLIT:\n"
        + "\n".join(lines)
        + "\n- Never claim 'I remember' unless session/local_chat/project_history context contains a stored record."
    )


def _system_rules(short: bool = False) -> str:
    if short:
        return (
            "SYSTEM_RULES:\n"
            "- Ты JARVIS, локальный помощник Александра.\n"
            "- Отвечай коротко по-русски.\n"
            "- Не называй себя Qwen, Alibaba, ChatGPT или облачной моделью.\n"
            "- PC control disabled: pc_control_allowed=false."
        )
    return (
        "SYSTEM_RULES:\n"
        "- Ты JARVIS, локальный помощник Александра для MAKSIMAR/JARVIS.\n"
        "- Не называй себя Qwen, Alibaba, ChatGPT или облачной моделью.\n"
        "- Используй session memory и runtime_history_store как контекст, не как абсолютную истину.\n"
        "- Не записывай в canonical/global project memory из live chat.\n"
        "- PC control disabled: pc_control_allowed=false.\n"
        "- Для погоды, поиска и текущих фактов нужен tool; если tool недоступен, скажи это."
    )


def _fast_final_answer_rules() -> str:
    return (
        "FAST_RESPONSE_RULES:\n"
        "- Если backend-модель использует thinking, thinking должен быть коротким.\n"
        "- После thinking всегда выдай финальный видимый ответ.\n"
        "- Финальный ответ не должен быть пустым."
    )


def _sentence_chunks(text: str) -> Iterator[str]:
    buffer = ""
    for char in text:
        buffer += char
        if char in ".!?…":
            yield buffer
            buffer = ""
    if buffer:
        yield buffer


def _event(event: str, **payload: Any) -> dict[str, Any]:
    return {"event": event, **payload, "pc_control_allowed": False}


def _run_read_only_command(command: tuple[str, ...]) -> str:
    try:
        result = subprocess.run(
            list(command),
            cwd=str(PROJECT_ROOT),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _run_optional_read_only_command(command: tuple[str, ...]) -> str:
    if shutil.which(command[0]) is None:
        return ""
    return _run_read_only_command(command)


def _parse_int(value: Any, default: int) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _csv(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)


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
