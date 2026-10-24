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
    assert "/jarvis-live/readiness" in routes
    assert "/jarvis-live/command" in routes
    assert "/jarvis-live/chat/stream" in routes

    source = Path("CONTROL_PLANE/api_server.py").read_text(encoding="utf-8")
    assert (
        "FastAPI(title=\"MAKSIMAR Control Plane\", lifespan=_control_plane_lifespan)"
        in source
    )
    assert "module_name = (" in source
    assert "\"jarvis_live_\"" in source
    assert "\"server_adapter\"" in source
    assert "from tools.jarvis_live_runtime.jarvis_live_brain_loop import" not in source
    assert "legacy_route_disabled" in source

    adapter_source = Path(
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py"
    ).read_text(encoding="utf-8")
    assert "TEMPORARY_COMPATIBILITY_SHIM_final_brain" not in adapter_source
    assert "MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools" in adapter_source
    assert "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models" in adapter_source
    assert "grounded_final_brain_call" in adapter_source
    assert "brain_bridge" not in adapter_source


def test_jarvis_live_health_and_status_are_pc_control_safe() -> None:
    health = jarvis_live_health()
    status = jarvis_live_status()

    assert health["ok"] is True
    assert "pc_control_allowed" not in health
    assert "pc_executor_available" in health
    assert health["hotpath_runtime"] == "CONTROL_PLANE/canonical_semantic_spine.py"
    assert health["default_model"] == "jarvis:chat8b"
    assert health["primary_conversation_model"] == "jarvis:chat8b"
    assert health["fallback_model"] == "jarvis-live:qwen14b"
    assert health["heavy_coder_model"] == "jarvis:coder14b"
    assert health["memory_federation_available"] is True
    session_health = health["health"]["memory_federation"]["canonical_session_health"]
    assert session_health["status"] == "LIVE_READ_ONLY"
    assert session_health["owner"] == "CanonicalSessionContextStore"
    assert session_health["path"] == health["health"]["session_memory_path"]
    assert "mempalace_status" in health
    assert health["canonical_memory_write_allowed"] is False
    assert health["control_plane_alive"] is True
    assert "chat_model_resident" in health
    assert "helper_model_resident" in health
    assert status["ok"] is True
    assert "pc_control_allowed" not in status
    assert "pc_executor_available" in status
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
    assert safety["read_only"] is True
    assert "safety_matches" in safety
    assert len(safety["safety_matches"]) >= 0
    assert memory["session"]["canonical_memory_write_allowed"] is False
    assert memory["brain_health"]["canonical_memory_write_allowed"] is False
    assert logs["api_log_file"]


def test_stream_writer_emits_chunks_and_handles_pc_control_refusal() -> None:
    lines: list[str] = []
    wrote_all = write_jarvis_live_stream_to_callable(
        lines.append,
        "Джарвис, открой браузер",
        session_id="test_control_plane_stream",
    )

    assert wrote_all is True
    payloads = [json.loads(line) for line in lines]
    assert payloads[-1]["event"] == "done"
    assert payloads[-1]["route"] == "LEGACY_DISABLED"
    assert "Используй /jarvis-live/hot" in payloads[-1]["response_text"]


def test_stream_writer_uses_broken_pipe_safe_helper() -> None:
    def broken_writer(_: str) -> None:
        raise BrokenPipeError

    assert (
        write_jarvis_live_stream_to_callable(
            broken_writer,
            "Джарвис, погода сейчас",
            session_id="test_broken_pipe",
        )
        is False
    )


def test_command_route_returns_legacy_disabled_payload() -> None:
    payload = jarvis_live_command({"text": "Джарвис, кто ты?", "session_id": "test"})

    assert payload["ok"] is False
    assert payload["route"] == "LEGACY_DISABLED"
    assert payload["legacy_route_disabled"] is True
    assert "Используй /jarvis-live/hot" in payload["llm_response"]
    assert "pc_control_allowed" not in payload


def test_command_route_cannot_use_voice_flag_as_owner_authorization() -> None:
    payload = jarvis_live_command({"text": "Джарвис, кто ты?", "session_id": "test"})

    assert payload["ok"] is False
    assert "owner_pc_control_allowed" not in payload
    assert "pc_control_allowed" not in payload
