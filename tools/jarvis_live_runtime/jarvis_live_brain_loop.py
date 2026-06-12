from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import asyncio
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


@dataclass(frozen=True)
class JarvisBrainContext:
    user_text: str
    request_route: str
    route_mode: str
    retrieval_mode: str
    selected_model_role: dict[str, Any]
    admission_status: dict[str, Any]
    recent_turns: tuple[dict[str, str], ...]
    rolling_summary: str
    active_topics: tuple[str, ...]
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
                    _format_turns(self.recent_turns[-4:]),
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
            "request_route": self.request_route,
            "retrieval_mode": self.retrieval_mode,
            "selected_model_role": self.selected_model_role,
            "admission_status": self.admission_status,
            "recent_turn_count": len(self.recent_turns),
            "rolling_summary": self.rolling_summary,
            "active_topics": self.active_topics,
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
        "runtime_history_store_path": str(
            final_payload.get("runtime_history_store_path", RUNTIME_HISTORY_STORE)
        ),
        "runtime_history_store_exists": bool(
            final_payload.get("runtime_history_store_exists", RUNTIME_HISTORY_STORE.exists())
        ),
        "retrieved_snippet_count": int(final_payload.get("retrieved_snippet_count", 0)),
        "retrieval_surfaces_used": tuple(final_payload.get("retrieval_surfaces_used", ())),
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
    _append_turn(state, "user", clean_text)
    context = build_jarvis_live_brain_context(clean_text, state, request_plan=request_plan)
    _save_session_state(state)
    context_elapsed_seconds = round(time.monotonic() - context_started_at, 4)

    yield {
        **_event("route_selected"),
        "route_mode": context.route_mode,
        "request_route": context.request_route,
        "retrieval_mode": context.retrieval_mode,
        "session_memory_path": str(SESSION_STATE_PATH),
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
        "selected_model_role": context.selected_model_role["selected_model_role"],
        "selected_model_id": context.selected_model_role["model_id"],
        "selected_model_status": context.selected_model_role["status"],
        "admission_allowed": context.admission_status["admission_allowed"],
        "resource_gate_surface": context.admission_status["resource_gate_surface"],
        "retrieved_snippet_count": len(context.retrieved_snippets),
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
            "retrieval_surfaces_used": context.retrieval_surfaces_used,
            "memory_federation_available": context.memory_federation_status["memory_federation_available"],
            "mempalace_status": context.memory_federation_status["mempalace_status"],
            "selected_model_role": context.selected_model_role["selected_model_role"],
            "selected_model_id": context.selected_model_role["model_id"],
            "selected_model_status": context.selected_model_role["status"],
            "admission_allowed": context.admission_status["admission_allowed"],
            "resource_gate_surface": context.admission_status["resource_gate_surface"],
            "session_memory_path": str(SESSION_STATE_PATH),
            "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
            "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
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
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
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
    memory_federation_status = build_jarvis_live_memory_federation_status()
    project_status = _project_status_summary() if _needs_project_status(user_text) else ""
    return JarvisBrainContext(
        user_text=user_text,
        request_route=request_plan["request_route"],
        route_mode=route_mode,
        retrieval_mode=request_plan["retrieval_mode"],
        selected_model_role=selected_model_role,
        admission_status=admission_status,
        recent_turns=tuple(state.get("recent_turns", [])[-MAX_RECENT_TURNS:]),
        rolling_summary=str(state.get("rolling_summary", "")),
        active_topics=tuple(state.get("active_topics", [])),
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
    if route_mode == "FAST":
        options = {**options, "num_predict": min(int(options.get("num_predict", 120)), 120)}
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
        "runtime_history_store_path": str(RUNTIME_HISTORY_STORE),
        "runtime_history_store_exists": RUNTIME_HISTORY_STORE.exists(),
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


def _build_memory_surface_inventory() -> tuple[dict[str, Any], ...]:
    return (
        _surface("session_memory", "session-runtime", str(SESSION_STATE_PATH), "usable_now", ()),
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
    history_exists = RUNTIME_HISTORY_STORE.exists()
    return (
        f"project_root={PROJECT_ROOT}; branch={branch or 'unknown'}; "
        f"git_status_short={status[:500] if status else 'clean_or_unavailable'}; "
        f"runtime_history_store={RUNTIME_HISTORY_STORE}; "
        f"runtime_history_store_exists={str(history_exists).lower()}; "
        "pc_control_allowed=false"
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


def _append_turn(state: dict[str, Any], role: str, text: str) -> None:
    if not text.strip():
        return
    turns = list(state.get("recent_turns", []))
    turns.append({"role": role, "text": text.strip(), "updated_at": str(time.time())})
    state["recent_turns"] = turns[-MAX_RECENT_TURNS:]
    state["local_session_persistence"] = True
    state["canonical_memory_write_allowed"] = False
    state["pc_control_allowed"] = False


def _load_session_state() -> dict[str, Any]:
    if not SESSION_STATE_PATH.exists():
        return _empty_session_state()
    try:
        payload = json.loads(SESSION_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_session_state()
    if not isinstance(payload, dict):
        return _empty_session_state()
    return payload


def _save_session_state(state: dict[str, Any]) -> None:
    SESSION_MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
    state["session_memory_path"] = str(SESSION_STATE_PATH)
    state["canonical_memory_write_allowed"] = False
    state["pc_control_allowed"] = False
    SESSION_STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )


def _empty_session_state() -> dict[str, Any]:
    return {
        "recent_turns": [],
        "rolling_summary": "",
        "active_topics": [],
        "local_session_persistence": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }


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


def _is_simple_code_request(lowered: str) -> bool:
    markers = ("pytest", "brokenpipeerror", "ошибка", "traceback", "код", "тест", "python")
    return any(marker in lowered for marker in markers)


def _is_deep_code_request(lowered: str) -> bool:
    markers = ("architecture", "архитектур", "сложн", "complex", "approval gate", "patch proposal")
    return any(marker in lowered for marker in markers) and _is_simple_code_request(lowered)


def _needs_project_status(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in ("проект", "статус", "git", "ветка", "runtime_history_store"))


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
