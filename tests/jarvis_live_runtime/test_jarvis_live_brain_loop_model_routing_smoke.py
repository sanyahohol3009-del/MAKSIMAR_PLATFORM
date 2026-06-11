from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_brain_context,
    _command_timeout_seconds,
    run_jarvis_live_brain_once,
    stream_jarvis_live_brain_response,
    write_stream_event_safely,
)


def test_brain_context_exposes_existing_model_router_and_resource_gate() -> None:
    context = build_jarvis_live_brain_context("Джарвис, сложный architecture traceback", {
        "recent_turns": [],
        "rolling_summary": "",
        "active_topics": [],
    })
    read_model = context.to_read_model()

    assert read_model["selected_model_role"]["selected_model_role"] == "heavy_coder_model"
    assert read_model["selected_model_role"]["model_id"] == "jarvis:coder14b"
    assert read_model["selected_model_role"]["target_model_id"] == "qwen2.5-coder:14b"
    assert read_model["selected_model_role"]["load_policy"] == "load_on_demand"
    assert read_model["admission_status"]["admission_allowed"] is True
    assert read_model["admission_status"]["queue_surface"] == "MAKSIMAR_CORE_LIB/execution_control"
    assert read_model["admission_status"]["worker_registry_surface"] == "MAKSIMAR_CORE_LIB/workers_registry"
    assert read_model["admission_status"]["agents_may_call_14b_directly"] is False
    assert read_model["pc_control_allowed"] is False


def test_broken_pipe_write_path_does_not_crash() -> None:
    writes: list[str] = []

    assert write_stream_event_safely(writes.append, {"event": "chunk", "text": "ok"}) is True
    assert writes

    def broken_writer(_: str) -> None:
        raise BrokenPipeError

    assert write_stream_event_safely(broken_writer, {"event": "chunk", "text": "lost"}) is False


def test_brain_loop_sanitizes_visible_thinking_blocks(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds: float | None = None):
        assert model_id == "jarvis:chat8b"
        assert prompt
        assert route_mode
        assert timeout_seconds is None
        yield {"event": "chunk", "text": "<think>hidden reasoning</think>Я JARVIS.", "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, кто ты?", session_id="test"))
    chunk_text = "".join(str(event.get("text", "")) for event in events if event["event"] == "chunk")
    done = events[-1]

    assert chunk_text == "Я JARVIS."
    assert "think" not in done["response_text"].casefold()
    assert done["selected_model_id"] == "jarvis:chat8b"
    assert done["selected_model_status"] == "installed"
    assert done["pc_control_allowed"] is False


def test_stream_emits_accepted_start_before_context_assembly(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def broken_context(*args, **kwargs):
        raise RuntimeError("context should not block first event")

    monkeypatch.setattr(brain_loop, "build_jarvis_live_brain_context", broken_context)

    stream = stream_jarvis_live_brain_response("Джарвис, привет", session_id="test")
    first = next(stream)

    assert first["event"] == "start"
    assert first["status"] == "accepted"
    assert first["request_route"] == "conversation"
    assert first["retrieval_mode"] == "session_only"
    assert first["selected_model_id"] == "jarvis:chat8b"
    assert first["pc_control_allowed"] is False


def test_weather_route_uses_current_facts_guard_without_model_hallucination(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def forbidden_model(*args, **kwargs):
        raise AssertionError("weather/current facts must not call offline model without tool")

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", forbidden_model)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, какая погода сейчас?", session_id="test"))
    done = events[-1]

    assert done["request_route"] == "current_facts_tool"
    assert done["retrieval_mode"] == "session_only"
    assert "tool недоступен" in done["response_text"]
    assert done["ollama_model_used"] == ""
    assert done["pc_control_allowed"] is False


def test_brain_command_response_is_non_empty_and_includes_selected_wrapper(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fake_error_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds: float | None = None):
        assert model_id
        assert timeout_seconds
        yield {"event": "error", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_error_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    payload = run_jarvis_live_brain_once("Джарвис, кто ты?", session_id="test")

    assert payload["llm_response"]
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_model_id"] == "jarvis:chat8b"
    assert payload["selected_model_status"] == "installed"
    assert payload["pc_control_allowed"] is False


def test_business_sovereign_command_returns_normal_response_when_ollama_succeeds(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    def fake_stream(model_id: str, prompt: str, route_mode: str, timeout_seconds: float | None = None):
        assert model_id == "jarvis:chat8b"
        assert "enterprise_business_memory" in prompt
        assert timeout_seconds == 120.0
        yield {"event": "chunk", "text": "По суверенному ИИ есть business memory context.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    payload = run_jarvis_live_brain_once("Что у нас есть по продаже суверенного ИИ?", session_id="test")

    assert payload["llm_response"]
    assert payload["error_kind"] == ""
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_model_id"] == "jarvis:chat8b"
    assert payload["memory_federation_available"] is True
    assert "enterprise_business_memory" in payload["retrieval_surfaces_used"]
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def test_command_timeout_default_is_not_too_aggressive() -> None:
    assert _command_timeout_seconds(None) == 120.0
