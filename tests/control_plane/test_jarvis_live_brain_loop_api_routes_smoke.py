import json
from pathlib import Path

import CONTROL_PLANE.api_server as api_server
from CONTROL_PLANE.api_server import (
    app,
    jarvis_live_command,
    jarvis_live_health,
    jarvis_live_logs,
    jarvis_live_memory,
    jarvis_live_models,
    jarvis_live_tools,
    jarvis_live_project,
    jarvis_live_project_dirty,
    jarvis_live_project_files,
    jarvis_live_project_file,
    jarvis_live_project_imports,
    jarvis_live_project_outline,
    jarvis_live_project_roadmap,
    jarvis_live_project_models,
    jarvis_live_project_search,
    jarvis_live_project_safety,
    jarvis_live_project_status,
    jarvis_live_project_tests,
    jarvis_live_project_tree,
    jarvis_live_status,
    write_jarvis_live_stream_to_callable,
)


def test_control_plane_exposes_jarvis_live_brain_routes_without_new_server() -> None:
    routes = {getattr(route, "path", "") for route in app.routes}

    assert "/jarvis-live/health" in routes
    assert "/jarvis-live/status" in routes
    assert "/jarvis-live/project" in routes
    assert "/jarvis-live/project/status" in routes
    assert "/jarvis-live/project/tree" in routes
    assert "/jarvis-live/project/files" in routes
    assert "/jarvis-live/project/dirty" in routes
    assert "/jarvis-live/project/search" in routes
    assert "/jarvis-live/project/file" in routes
    assert "/jarvis-live/project/outline" in routes
    assert "/jarvis-live/project/imports" in routes
    assert "/jarvis-live/project/tests" in routes
    assert "/jarvis-live/project/roadmap" in routes
    assert "/jarvis-live/project/models" in routes
    assert "/jarvis-live/project/safety" in routes
    assert "/jarvis-live/memory" in routes
    assert "/jarvis-live/models" in routes
    assert "/jarvis-live/tools" in routes
    assert "/jarvis-live/logs" in routes
    assert "/jarvis-live/command" in routes
    assert "/jarvis-live/chat/stream" in routes

    source = Path("CONTROL_PLANE/api_server.py").read_text(encoding="utf-8")
    assert "FastAPI(title=\"MAKSIMAR Control Plane\")" in source
    assert "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter" in source
    assert "from tools.jarvis_live_runtime.jarvis_live_brain_loop import" not in source
    assert "write_stream_event_safely" in source
    assert "brain_bridge" not in source
    assert "second server" not in source.lower()

    adapter_source = Path(
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py"
    ).read_text(encoding="utf-8")
    assert "jarvis_live_brain_loop" in adapter_source
    assert "brain_bridge" not in adapter_source


def test_jarvis_live_health_and_status_are_pc_control_safe() -> None:
    health = jarvis_live_health()
    status = jarvis_live_status()

    assert health["ok"] is True
    assert health["pc_control_allowed"] is False
    assert health["brain_loop"] == "tools/jarvis_live_runtime/jarvis_live_brain_loop.py"
    assert health["default_model"] == "jarvis:chat8b"
    assert health["primary_conversation_model"] == "jarvis:chat8b"
    assert health["fallback_model"] == "jarvis-live:qwen14b"
    assert health["heavy_coder_model"] == "jarvis:coder14b"
    assert health["memory_federation_available"] is True
    assert health["memory_surfaces_detected_count"] >= 1
    assert "mempalace_status" in health
    assert health["canonical_memory_write_allowed"] is False
    assert status["ok"] is True
    assert status["pc_control_allowed"] is False
    assert status["default_model"] == "jarvis:chat8b"
    assert status["primary_conversation_model"] == "jarvis:chat8b"
    assert status["fallback_model"] == "jarvis-live:qwen14b"
    assert status["heavy_coder_model"] == "jarvis:coder14b"
    assert status["memory_federation_available"] is True
    assert "active_retrieval_surfaces" in status
    assert "sandbox_only_memory_surfaces" in status
    assert status["canonical_memory_write_allowed"] is False
    assert status["session"]["pc_control_allowed"] is False


def test_read_only_project_and_memory_endpoints_expose_existing_read_models() -> None:
    project = jarvis_live_project()
    project_status = jarvis_live_project_status()
    tree = jarvis_live_project_tree()
    files = jarvis_live_project_files()
    dirty = jarvis_live_project_dirty()
    search = jarvis_live_project_search(q="memory")
    file_payload = jarvis_live_project_file(path="tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    outline = jarvis_live_project_outline(path="tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    imports = jarvis_live_project_imports(path="tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    tests = jarvis_live_project_tests()
    roadmap = jarvis_live_project_roadmap()
    models = jarvis_live_project_models()
    tools = jarvis_live_tools()
    safety = jarvis_live_project_safety()
    memory = jarvis_live_memory()
    logs = jarvis_live_logs()

    assert project["ok"] is True
    assert project["read_only"] is True
    assert project["project"]["read_only"] is True
    assert project_status["project_status"]["read_only"] is True
    assert tree["tree"]["read_only"] is True
    assert files["files"]["read_only"] is True
    assert dirty["read_only"] is True
    assert search["search"]["read_only"] is True
    assert file_payload["file"]["read_only"] is True
    assert outline["outline"]["read_only"] is True
    assert imports["imports"]["read_only"] is True
    assert tests["project"]["read_only"] is True
    assert tests["test_file_count"] > 0
    assert roadmap["status"]["read_only"] == "true"
    assert models["models"]["ollama_is_local_model_engine"] == "true"
    assert "ollama_version" in models["models"]
    assert "ollama_tags" in models["models"]
    assert "ollama_ps" in models["models"]
    assert tools["tools"]["all_existing_read_tools_connected"] is True
    assert "repo_search" in tools["tools"]["read_tools"]
    assert "pytest_run_proposal" in tools["tools"]["proposal_tools"]
    assert tools["tools"]["execution_allowed"] is False
    assert safety["read_only"] is True
    assert "safety_matches" in safety
    assert len(safety["safety_matches"]) >= 0
    assert memory["session"]["canonical_memory_write_allowed"] is False
    assert memory["brain_health"]["canonical_memory_write_allowed"] is False
    assert logs["api_log_file"]


def test_stream_writer_emits_chunks_and_handles_pc_control_refusal() -> None:
    lines: list[str] = []
    original_stream = api_server.stream_jarvis_live_brain_response
    api_server.stream_jarvis_live_brain_response = _fake_pc_refusal_stream
    try:
        wrote_all = write_jarvis_live_stream_to_callable(
            lines.append,
            "Джарвис, открой браузер",
            session_id="test_control_plane_stream",
        )
    finally:
        api_server.stream_jarvis_live_brain_response = original_stream

    assert wrote_all is True
    payloads = [json.loads(line) for line in lines]
    assert any(payload["event"] == "chunk" for payload in payloads)
    assert payloads[-1]["event"] == "done"
    assert payloads[-1]["pc_control_allowed"] is False
    assert "Прямое управление ПК выключено" in payloads[-1]["response_text"]


def test_stream_writer_uses_broken_pipe_safe_helper() -> None:
    original_stream = api_server.stream_jarvis_live_brain_response
    api_server.stream_jarvis_live_brain_response = _fake_pc_refusal_stream
    def broken_writer(_: str) -> None:
        raise BrokenPipeError

    try:
        assert (
            write_jarvis_live_stream_to_callable(
                broken_writer,
                "Джарвис, погода сейчас",
                session_id="test_broken_pipe",
            )
            is False
        )
    finally:
        api_server.stream_jarvis_live_brain_response = original_stream


def test_command_route_returns_selected_model_fields_as_json() -> None:
    original_run = api_server.run_jarvis_live_brain_once
    api_server.run_jarvis_live_brain_once = _fake_command_run
    try:
        payload = jarvis_live_command({"text": "Джарвис, кто ты?", "session_id": "test"})
    finally:
        api_server.run_jarvis_live_brain_once = original_run

    assert payload["ok"] is True
    assert payload["llm_response"]
    assert payload["error_kind"] == ""
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_model_id"] == "jarvis:chat8b"
    assert payload["selected_model_status"] == "installed"
    assert payload["retrieved_snippet_count"] == 2
    assert payload["retrieval_surfaces_used"] == ("runtime_history_store", "memory_engine_registry")
    assert payload["memory_federation_available"] is True
    assert payload["mempalace_status"] == "sandbox_only_read_only"
    assert payload["session_memory_path"]
    assert payload["runtime_history_store_exists"] is True
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False
    assert payload["result"]["llm_response"]


def test_command_route_returns_valid_json_on_timeout_or_cancel() -> None:
    original_run = api_server.run_jarvis_live_brain_once

    def timed_out(text: str, session_id: str = "windows_voice_edge") -> dict[str, object]:
        raise TimeoutError

    api_server.run_jarvis_live_brain_once = timed_out
    try:
        payload = jarvis_live_command({"text": "Джарвис, кто ты?", "session_id": "test"})
    finally:
        api_server.run_jarvis_live_brain_once = original_run

    assert payload["ok"] is True
    assert payload["llm_response"]
    assert payload["error_kind"] == "command_timeout_or_cancelled"
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_model_id"] == "jarvis:chat8b"
    assert payload["selected_model_status"] == "installed"
    assert payload["retrieved_snippet_count"] == 0
    assert "retrieval_surfaces_used" in payload
    assert "memory_federation_available" in payload
    assert "mempalace_status" in payload
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def test_command_route_returns_valid_json_on_runtime_error() -> None:
    original_run = api_server.run_jarvis_live_brain_once

    def broken(text: str, session_id: str = "windows_voice_edge") -> dict[str, object]:
        raise RuntimeError("boom")

    api_server.run_jarvis_live_brain_once = broken
    try:
        payload = jarvis_live_command({"text": "Объясни BrokenPipeError", "session_id": "test"})
    finally:
        api_server.run_jarvis_live_brain_once = original_run

    assert payload["ok"] is True
    assert payload["llm_response"]
    assert payload["error_kind"] == "command_runtime_error"
    assert payload["selected_model_id"] == "jarvis:coder7b"
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def _fake_pc_refusal_stream(text: str, session_id: str = "windows_voice_edge"):
    assert text
    assert session_id
    yield {"event": "start", "pc_control_allowed": False}
    yield {
        "event": "chunk",
        "text": "Прямое управление ПК выключено",
        "pc_control_allowed": False,
    }
    yield {
        "event": "done",
        "response_text": "Прямое управление ПК выключено",
        "pc_control_allowed": False,
    }


def _fake_command_run(text: str, session_id: str = "windows_voice_edge") -> dict[str, object]:
    assert text
    assert session_id
    return {
        "llm_response": "Я JARVIS.",
        "error_kind": "",
        "selected_model_role": "jarvis_chat_model",
        "selected_model_id": "jarvis:chat8b",
        "selected_model_status": "installed",
        "retrieved_snippet_count": 2,
        "retrieval_surfaces_used": ("runtime_history_store", "memory_engine_registry"),
        "memory_federation_available": True,
        "mempalace_status": "sandbox_only_read_only",
        "session_memory_path": "/runtime/session.json",
        "runtime_history_store_exists": True,
        "canonical_memory_write_allowed": False,
        "pc_control_allowed": False,
    }
