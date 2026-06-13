from __future__ import annotations

import json
import asyncio
from typing import Any, Iterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pathlib import Path
import time

from CONTROL_PLANE.health.monitor import take_snapshot
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import (
    build_jarvis_live_brain_health,
    build_jarvis_live_session_status,
    run_jarvis_live_brain_once,
    stream_jarvis_live_brain_response,
    write_stream_event_safely,
)
from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_tool_catalog_read_model,
    build_jarvis_live_project_status_read_model,
    build_project_workspace_read_model,
    model_runtime_status,
    read_file_outline,
    read_file_snippet,
    repo_files,
    repo_git_status,
    repo_import_graph,
    repo_search,
    repo_tree,
    status_tools,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    select_jarvis_live_model_role,
)

app = FastAPI(title="MAKSIMAR Control Plane")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_LOG_FILE = PROJECT_ROOT / ".runtime" / "jarvis_live" / "api.log"


@app.get("/")
def root():
    return {"status": "MAKSIMAR control plane online"}


@app.get("/health")
def health():
    root = str(Path(__file__).resolve().parents[1])
    snap = take_snapshot(root)

    return {"ok": True, "health": snap.as_dict()}


@app.get("/health/latency")
def health_latency():
    t0 = time.perf_counter()
    dt_ms = (time.perf_counter() - t0) * 1000.0

    return {"ok": True, "latency_ms": dt_ms}


@app.get("/jarvis-live/health")
def jarvis_live_health() -> dict[str, Any]:
    health_payload = build_jarvis_live_brain_health()
    memory = dict(health_payload.get("memory_federation", {}))
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "brain_loop": "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
        "default_model": health_payload.get("default_model", "jarvis:chat8b"),
        "primary_conversation_model": health_payload.get("primary_conversation_model", "jarvis:chat8b"),
        "fallback_model": health_payload.get("fallback_model", "jarvis-live:qwen14b"),
        "heavy_coder_model": health_payload.get("heavy_coder_model", "jarvis:coder14b"),
        "memory_federation_available": memory.get("memory_federation_available", False),
        "memory_surfaces_detected_count": memory.get("memory_surfaces_detected_count", 0),
        "active_retrieval_surfaces": memory.get("active_retrieval_surfaces", ()),
        "disabled_memory_surfaces": memory.get("disabled_memory_surfaces", ()),
        "sandbox_only_memory_surfaces": memory.get("sandbox_only_memory_surfaces", ()),
        "vector_memory_available": memory.get("vector_memory_available", False),
        "regulatory_memory_available": memory.get("regulatory_memory_available", False),
        "business_memory_available": memory.get("business_memory_available", False),
        "mempalace_status": memory.get("mempalace_status", "not_detected"),
        "runtime_history_store_exists": memory.get("runtime_history_store_exists", False),
        "session_memory_exists": memory.get("session_memory_exists", False),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "health": health_payload,
    }


@app.get("/jarvis-live/status")
def jarvis_live_status() -> dict[str, Any]:
    session_payload = build_jarvis_live_session_status()
    memory = dict(session_payload.get("memory_federation", {}))
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "default_model": session_payload.get("default_model", "jarvis:chat8b"),
        "primary_conversation_model": session_payload.get("primary_conversation_model", "jarvis:chat8b"),
        "fallback_model": session_payload.get("fallback_model", "jarvis-live:qwen14b"),
        "heavy_coder_model": session_payload.get("heavy_coder_model", "jarvis:coder14b"),
        "memory_federation_available": memory.get("memory_federation_available", False),
        "memory_surfaces_detected_count": memory.get("memory_surfaces_detected_count", 0),
        "active_retrieval_surfaces": memory.get("active_retrieval_surfaces", ()),
        "disabled_memory_surfaces": memory.get("disabled_memory_surfaces", ()),
        "sandbox_only_memory_surfaces": memory.get("sandbox_only_memory_surfaces", ()),
        "vector_memory_available": memory.get("vector_memory_available", False),
        "regulatory_memory_available": memory.get("regulatory_memory_available", False),
        "business_memory_available": memory.get("business_memory_available", False),
        "mempalace_status": memory.get("mempalace_status", "not_detected"),
        "runtime_history_store_exists": memory.get("runtime_history_store_exists", False),
        "session_memory_exists": memory.get("session_memory_exists", False),
        "recent_turn_count": session_payload.get("recent_turn_count", 0),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "session": session_payload,
    }


@app.get("/jarvis-live/project")
def jarvis_live_project() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "project": build_project_workspace_read_model(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/status")
def jarvis_live_project_status() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "project_status": build_jarvis_live_project_status_read_model(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/tree")
def jarvis_live_project_tree(depth: int = 2, max_entries: int = 300) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "tree": repo_tree(depth=depth, max_entries=max_entries),
        "read_only": True,
    }


@app.get("/jarvis-live/project/files")
def jarvis_live_project_files(page: int = 1, page_size: int = 80) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "files": repo_files(page=page, page_size=page_size),
        "read_only": True,
    }


@app.get("/jarvis-live/project/dirty")
def jarvis_live_project_dirty() -> dict[str, Any]:
    status = repo_git_status()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "dirty_files": status.get("dirty_files", ()),
        "untracked_files": status.get("untracked_files", ()),
        "staged_files": status.get("staged_files", ()),
        "diff_name_only": status.get("diff_name_only", ()),
        "diff_stat": status.get("diff_stat", ""),
        "read_only": True,
    }


@app.get("/jarvis-live/project/search")
def jarvis_live_project_search(q: str = "", path: str = "", max_results: int = 40) -> dict[str, Any]:
    paths = tuple(part for part in path.split(",") if part.strip()) if path else None
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "search": repo_search(q, paths=paths, max_results=max_results),
        "read_only": True,
    }


@app.get("/jarvis-live/project/file")
def jarvis_live_project_file(path: str, start_line: int = 1, end_line: int | None = None, page: int = 1) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "file": read_file_snippet(path, start_line=start_line, end_line=end_line, page=page),
        "read_only": True,
    }


@app.get("/jarvis-live/project/outline")
def jarvis_live_project_outline(path: str) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "outline": read_file_outline(path),
        "read_only": True,
    }


@app.get("/jarvis-live/project/imports")
def jarvis_live_project_imports(path: str | None = None, max_edges: int = 80) -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "imports": repo_import_graph(path=path, max_edges=max_edges),
        "read_only": True,
    }


@app.get("/jarvis-live/project/tests")
def jarvis_live_project_tests() -> dict[str, Any]:
    model = build_project_workspace_read_model()
    test_files = model.get("domain_groups", {}).get("tests", ())
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "test_file_count": len(test_files),
        "test_files": test_files,
        "project": model,
        "read_only": True,
    }


@app.get("/jarvis-live/project/roadmap")
def jarvis_live_project_roadmap() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "status": status_tools(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/models")
def jarvis_live_project_models() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "models": model_runtime_status(),
        "read_only": True,
    }


@app.get("/jarvis-live/project/safety")
def jarvis_live_project_safety() -> dict[str, Any]:
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
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "safety_matches": tuple(results),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "api_log_file": str(API_LOG_FILE),
        "read_only": True,
    }


@app.get("/jarvis-live/memory")
def jarvis_live_memory() -> dict[str, Any]:
    session_payload = build_jarvis_live_session_status()
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "session": session_payload,
        "brain_health": build_jarvis_live_brain_health(),
        "read_only": True,
    }


@app.get("/jarvis-live/models")
def jarvis_live_models() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "models": model_runtime_status(),
        "read_only": True,
    }


@app.get("/jarvis-live/tools")
def jarvis_live_tools() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "tools": build_jarvis_live_tool_catalog_read_model(),
        "read_only": True,
    }


@app.get("/jarvis-live/logs")
def jarvis_live_logs() -> dict[str, Any]:
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "api_log_file": str(API_LOG_FILE),
        "read_only": True,
    }


@app.post("/jarvis-live/command")
def jarvis_live_command(payload: dict[str, Any]) -> dict[str, Any]:
    text = _payload_text(payload)
    session_id = _payload_session_id(payload)
    try:
        result = run_jarvis_live_brain_once(text, session_id=session_id)
    except (TimeoutError, asyncio.CancelledError):
        result = _command_error_result(text, "command_timeout_or_cancelled")
    except KeyboardInterrupt:
        result = _command_error_result(text, "command_cancelled_by_operator")
    except Exception:
        result = _command_error_result(text, "command_runtime_error")
    return {
        "ok": True,
        "surface": "CONTROL_PLANE/api_server.py",
        "streaming": False,
        "llm_response": result.get("llm_response", ""),
        "error_kind": result.get("error_kind", ""),
        "selected_model_role": result.get("selected_model_role", ""),
        "selected_model_id": result.get("selected_model_id", ""),
        "selected_model_status": result.get("selected_model_status", ""),
        "retrieved_snippet_count": result.get("retrieved_snippet_count", 0),
        "retrieval_surfaces_used": result.get("retrieval_surfaces_used", ()),
        "memory_federation_available": result.get("memory_federation_available", False),
        "mempalace_status": result.get("mempalace_status", "not_detected"),
        "session_memory_path": result.get("session_memory_path", ""),
        "runtime_history_store_exists": bool(result.get("runtime_history_store_exists", False)),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
        "result": result,
    }


@app.post("/jarvis-live/chat/stream")
def jarvis_live_streaming_chat(payload: dict[str, Any]) -> StreamingResponse:
    text = _payload_text(payload)
    session_id = _payload_session_id(payload)
    return StreamingResponse(
        _jarvis_live_streaming_lines(text=text, session_id=session_id),
        media_type="application/x-ndjson",
    )


def write_jarvis_live_stream_to_callable(
    write_callable: Any,
    text: str,
    session_id: str = "windows_voice_edge",
) -> bool:
    wrote_all = True
    for event in stream_jarvis_live_brain_response(text, session_id=session_id):
        if not write_stream_event_safely(write_callable, event):
            wrote_all = False
            break
    return wrote_all


def _jarvis_live_streaming_lines(text: str, session_id: str) -> Iterable[str]:
    try:
        for event in stream_jarvis_live_brain_response(text, session_id=session_id):
            yield json.dumps(event, ensure_ascii=False) + "\n"
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        print("[WARNING] Client disconnected before receiving response")


def _payload_text(payload: dict[str, Any]) -> str:
    for key in ("text", "command", "message", "input"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _payload_session_id(payload: dict[str, Any]) -> str:
    value = payload.get("session_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "windows_voice_edge"


def _command_error_result(text: str, error_kind: str) -> dict[str, Any]:
    selected = select_jarvis_live_model_role(text)
    status = jarvis_live_status()
    return {
        "llm_response": "JARVIS command runtime не вернул модельный ответ вовремя. Действие не выполнялось; pc_control_allowed=false.",
        "error_kind": error_kind,
        "selected_model_role": selected["selected_model_role"],
        "selected_model_id": selected["model_id"],
        "selected_model_status": selected["status"],
        "retrieved_snippet_count": 0,
        "retrieval_surfaces_used": (),
        "memory_federation_available": status.get("memory_federation_available", False),
        "mempalace_status": status.get("mempalace_status", "not_detected"),
        "session_memory_path": "",
        "runtime_history_store_exists": status.get("runtime_history_store_exists", False),
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }
