from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import asyncio
import ast
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

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


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
SESSION_MEMORY_ROOT = RUNTIME_ROOT / "session_memory"
SESSION_STATE_PATH = SESSION_MEMORY_ROOT / "jarvis_live_session_state.json"
SESSION_TURN_LOG_NAME = "jarvis_live_terminal_turns.jsonl"
RUNTIME_HISTORY_STORE = PROJECT_ROOT / "runtime_history_store"
RUNTIME_VECTOR_INDEX_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_vector_indexes"
RUNTIME_EMBEDDINGS_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_embeddings"
RUNTIME_RETRIEVAL_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "runtime_retrieval"
OLLAMA_URL = os.environ.get(
    "JARVIS_LIVE_OLLAMA_URL",
    "http://127.0.0.1:11434/api/generate",
)
PRIMARY_CONVERSATION_MODEL_ID = "jarvis:chat8b"
DEFAULT_OLLAMA_MODEL_ID = os.environ.get("JARVIS_LIVE_OLLAMA_MODEL", PRIMARY_CONVERSATION_MODEL_ID)
FALLBACK_OLLAMA_MODEL_ID = "jarvis-live:qwen14b"
HEAVY_CODER_MODEL_ID = "jarvis:coder14b"
BASE_HEAVY_CODER_MODEL_ID = "qwen2.5-coder:14b"
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

    def to_prompt(self) -> str:
        if self.route_mode == "FAST" and self.retrieval_mode == "session_only":
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
                    f"USER_MESSAGE: {self.user_text}",
                )
                if part
            )
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
                f"USER_MESSAGE: {self.user_text}",
            )
            if part
        )

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
        "context_elapsed_seconds": context_elapsed_seconds,
    }

    guarded_response = _guarded_local_response(clean_text, context)
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
        }
        return

    chunks: list[str] = []
    thinking_chunks: list[str] = []
    errors: list[dict[str, Any]] = []
    model_used = ""
    empty_model_id = ""
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
            elif event["event"] == "done":
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
    elif not response_text and thinking_chunks:
        error_kind = "ollama_thinking_without_final_response"
        error_message = "model produced thinking but no final response; increase num_predict or disable thinking."
    elif not response_text:
        error_kind = "ollama_empty_response"
        model_for_error = empty_model_id or model_used or context.selected_model_role["model_id"]
        error_message = f"ollama_empty_response model={model_for_error}"
    _append_assistant_and_summarize(state, response_text, context)
    yield {
        **_event("done", response_text=response_text, route_mode=context.route_mode),
        "request_route": context.request_route,
        "retrieval_mode": context.retrieval_mode,
        "ollama_model_used": model_used,
        "thinking_chunk_count": len(thinking_chunks),
        "answer_chunk_count": len(chunks),
        "stream_chunk_count": len(thinking_chunks) + len(chunks),
        "had_thinking": bool(thinking_chunks),
        "retrieved_snippet_count": len(context.retrieved_snippets),
        "local_chat_memory_snippet_count": len(context.local_chat_memory_snippets),
        "retrieval_surfaces_used": context.retrieval_surfaces_used,
        "memory_federation_available": context.memory_federation_status["memory_federation_available"],
        "mempalace_status": context.memory_federation_status["mempalace_status"],
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "selected_model_id": context.selected_model_role["model_id"],
        "selected_model_status": context.selected_model_role["status"],
        "error_kind": error_kind,
        "error_message": error_message,
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


def model_runtime_status() -> dict[str, str]:
    return {
        "ollama_ps": _run_optional_read_only_command(("ollama", "ps")),
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


def _stream_ollama_model(
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
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds or 120) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
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
                    )
                    return
                thinking = str(payload.get("thinking", ""))
                if thinking:
                    yield _event("thinking", text=thinking, ollama_model_used=model_id)
                chunk = str(payload.get("response", ""))
                if chunk:
                    yield _event("chunk", text=chunk, ollama_model_used=model_id)
                if payload.get("done") is True:
                    yield _event("done", ollama_model_used=model_id)
                    return
    except (urllib.error.URLError, TimeoutError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as exc:
        yield _event(
            "error",
            ollama_model_used=model_id,
            error_message=f"{exc.__class__.__name__}: {exc}",
        )


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


def _guarded_local_response(user_text: str, context: JarvisBrainContext) -> str | None:
    lowered = user_text.casefold()
    project_tool_answer = _answer_project_read_tool_request(user_text)
    if project_tool_answer:
        return project_tool_answer
    style_memory_answer = _answer_style_memory_recall_if_grounded(context)
    if style_memory_answer:
        return style_memory_answer
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
        return _format_file_answer(parts[2], page)
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


def _format_file_answer(path: str, page: int) -> str:
    payload = read_file_snippet(path, page=page)
    if not payload.get("allowed"):
        return f"File snippet denied: path={path}; error={payload.get('error', 'unknown')}; read_only=true."
    lines = [f"File snippet read-only: {path} page={payload['page']} lines={payload['start_line']}-{payload['end_line']}"]
    lines.extend(payload["snippet"])
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
        f"ollama_ps={status.get('ollama_ps') or 'unavailable'}\n"
        f"nvidia_smi={status.get('nvidia_smi') or 'unavailable'}\n"
        f"free_h={status.get('free_h') or 'unavailable'}\n"
        "pc_control_allowed=false direct_execution_allowed=false model_download_allowed=false_from_chat"
    )


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
    cleaned = text
    lowered = cleaned.casefold()
    for start_marker, end_marker in (
        ("<think>", "</think>"),
        ("<thinking>", "</thinking>"),
        ("thinking:", "\n\n"),
        ("reasoning:", "\n\n"),
        ("мысли:", "\n\n"),
        ("рассуждение:", "\n\n"),
    ):
        while start_marker in lowered:
            start = lowered.find(start_marker)
            end = lowered.find(end_marker, start + len(start_marker))
            if end == -1:
                cleaned = cleaned[:start]
            else:
                cleaned = cleaned[:start] + cleaned[end + len(end_marker) :]
            lowered = cleaned.casefold()
    return cleaned.strip()


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
