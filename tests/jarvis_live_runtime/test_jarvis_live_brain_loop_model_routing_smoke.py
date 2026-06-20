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
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id == "jarvis:chat8b"
        assert prompt
        assert route_mode
        assert timeout_seconds == 180.0
        assert response_mode_text == "Джарвис, кто ты?"
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
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

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
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

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
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_error_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id
        assert timeout_seconds
        assert response_mode_text == "Джарвис, кто ты?"
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


def test_empty_ollama_done_is_reported_as_visible_error(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_empty_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id == "jarvis:chat8b"
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_empty_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, привет", session_id="test"))
    done = events[-1]

    assert done["event"] == "done"
    assert done["stream_chunk_count"] == 0
    assert done["error_kind"] == "ollama_empty_response"
    assert done["error_message"] == "ollama_empty_response model=jarvis:chat8b"
    assert done["selected_model_id"] == "jarvis:chat8b"
    assert done["pc_control_allowed"] is False


def test_thinking_then_final_response_counts_thinking_and_answer(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_thinking_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id == "jarvis:chat8b"
        yield {"event": "thinking", "text": "Проверяю кратко.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "chunk", "text": "Привет.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_thinking_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, привет", session_id="test"))
    done = events[-1]

    assert any(event["event"] == "thinking" for event in events)
    assert done["had_thinking"] is True
    assert done["thinking_chunk_count"] == 1
    assert done["answer_chunk_count"] == 1
    assert done["stream_chunk_count"] == 2
    assert done["response_text"] == "Привет."
    assert done["error_kind"] == ""


def test_thinking_without_final_response_is_reported(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_thinking_only_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id == "jarvis:chat8b"
        yield {"event": "thinking", "text": "Думаю, но не отвечаю.", "ollama_model_used": model_id, "pc_control_allowed": False}
        yield {"event": "done", "ollama_model_used": model_id, "pc_control_allowed": False}

    monkeypatch.setattr(brain_loop, "_stream_ollama_model", fake_thinking_only_stream)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, привет", session_id="test"))
    done = events[-1]

    assert done["had_thinking"] is True
    assert done["thinking_chunk_count"] == 1
    assert done["answer_chunk_count"] == 0
    assert done["stream_chunk_count"] == 1
    assert done["error_kind"] == "ollama_thinking_without_final_response"
    assert "increase num_predict or disable thinking" in done["error_message"]


def test_fast_conversation_routes_to_api_chat_with_think_false(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    captured: dict[str, object] = {}

    def fake_chat(
        model_id: str,
        prompt: str,
        timeout_seconds: float | None = None,
        response_mode: object | None = None,
        response_mode_text: str | None = None,
    ):
        captured["model_id"] = model_id
        captured["prompt"] = prompt
        captured["timeout_seconds"] = timeout_seconds
        captured["response_mode_text"] = response_mode_text
        yield {
            "event": "chunk",
            "text": "Привет.",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": False,
            "think_mode": "false",
            "ollama_num_predict": brain_loop.OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": brain_loop.OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": brain_loop.OLLAMA_FAST_CHAT_TOP_P,
            "pc_control_allowed": False,
        }
        yield {
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": False,
            "think_mode": "false",
            "ollama_num_predict": brain_loop.OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": brain_loop.OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": brain_loop.OLLAMA_FAST_CHAT_TOP_P,
            "pc_control_allowed": False,
        }

    def forbidden_generate(*args, **kwargs):
        raise AssertionError("FAST path should use api/chat first")

    monkeypatch.setattr(ollama_streaming, "_stream_ollama_chat_model", fake_chat)
    monkeypatch.setattr(ollama_streaming, "_stream_ollama_generate_model", forbidden_generate)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис привет", session_id="test"))
    done = events[-1]

    assert captured["model_id"] == "jarvis:chat8b"
    assert captured["response_mode_text"] == "Джарвис привет"
    assert done["ollama_endpoint"] == brain_loop.OLLAMA_CHAT_URL
    assert done["ollama_endpoint_fallback_used"] is False
    assert done["think_mode"] == "false"
    assert done["ollama_num_predict"] == brain_loop.OLLAMA_FAST_CHAT_NUM_PREDICT
    assert done["ollama_temperature"] == brain_loop.OLLAMA_FAST_CHAT_TEMPERATURE
    assert done["ollama_top_p"] == brain_loop.OLLAMA_FAST_CHAT_TOP_P


def test_chat_parser_emits_thinking_content_and_tool_calls_as_proposal_only() -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    payload = {
        "message": {
            "thinking": "Сначала думаю.",
            "content": "Готов.",
            "tool_calls": [
                {
                    "function": {
                        "name": "run_shell",
                        "arguments": {"command": "rm -rf /"},
                    }
                }
            ],
        },
        "done": True,
    }

    events = brain_loop._parse_ollama_chat_stream_event(payload, "jarvis:chat8b")

    assert [event["event"] for event in events] == ["thinking", "tool_call", "chunk", "done"]
    tool_call_event = events[1]
    assert tool_call_event["tool_call_detected"] is True
    assert tool_call_event["tool_call_count"] == 1
    assert tool_call_event["execution_allowed"] is False
    assert tool_call_event["approval_required"] is True
    assert tool_call_event["proposal_only"] is True


def test_tool_calls_are_proposal_only_in_stream(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_chat(
        model_id: str,
        prompt: str,
        timeout_seconds: float | None = None,
        response_mode: object | None = None,
        response_mode_text: str | None = None,
    ):
        yield {
            "event": "tool_call",
            "tool_call_detected": True,
            "tool_call_count": 1,
            "tool_calls": ({"function": {"name": "search_repo"}},),
            "execution_allowed": False,
            "approval_required": True,
            "proposal_only": True,
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": False,
            "think_mode": "false",
            "ollama_num_predict": brain_loop.OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": brain_loop.OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": brain_loop.OLLAMA_FAST_CHAT_TOP_P,
            "pc_control_allowed": False,
        }
        yield {
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": False,
            "think_mode": "false",
            "ollama_num_predict": brain_loop.OLLAMA_FAST_CHAT_NUM_PREDICT,
            "ollama_temperature": brain_loop.OLLAMA_FAST_CHAT_TEMPERATURE,
            "ollama_top_p": brain_loop.OLLAMA_FAST_CHAT_TOP_P,
            "pc_control_allowed": False,
            "tool_call_count": 1,
            "tool_call_detected": True,
        }

    monkeypatch.setattr(ollama_streaming, "_stream_ollama_chat_model", fake_chat)
    monkeypatch.setattr(ollama_streaming, "_stream_ollama_generate_model", lambda *args, **kwargs: (_ for _ in ()))
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, расскажи про новый режим", session_id="test"))
    tool_event = next(event for event in events if event["event"] == "tool_call")
    done = events[-1]

    assert tool_event["execution_allowed"] is False
    assert tool_event["approval_required"] is True
    assert tool_event["proposal_only"] is True
    assert "tool_call proposal" in done["response_text"]
    assert done["tool_call_detected"] is True
    assert done["tool_call_count"] == 1


def test_chat_failure_falls_back_to_generate(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_chat(
        model_id: str,
        prompt: str,
        timeout_seconds: float | None = None,
        response_mode: object | None = None,
        response_mode_text: str | None = None,
    ):
        yield {
            "event": "error",
            "ollama_model_used": model_id,
            "error_message": "chat endpoint rejected",
            "ollama_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "pc_control_allowed": False,
        }

    def fake_generate(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        yield {
            "event": "chunk",
            "text": "Резервный ответ.",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": True,
            "primary_error_kind": "ollama_chat_stream_error",
            "primary_error_message": "chat endpoint rejected",
            "think_mode": "generate",
            "ollama_num_predict": 512,
            "ollama_temperature": 0.8,
            "ollama_top_p": 0.95,
            "pc_control_allowed": False,
        }
        yield {
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_URL,
            "primary_endpoint": brain_loop.OLLAMA_CHAT_URL,
            "fallback_endpoint": brain_loop.OLLAMA_URL,
            "ollama_endpoint_fallback_used": True,
            "primary_error_kind": "ollama_chat_stream_error",
            "primary_error_message": "chat endpoint rejected",
            "think_mode": "generate",
            "ollama_num_predict": 512,
            "ollama_temperature": 0.8,
            "ollama_top_p": 0.95,
            "pc_control_allowed": False,
        }

    monkeypatch.setattr(ollama_streaming, "_stream_ollama_chat_model", fake_chat)
    monkeypatch.setattr(ollama_streaming, "_stream_ollama_generate_model", fake_generate)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис привет", session_id="test"))
    done = events[-1]

    assert done["ollama_endpoint"] == brain_loop.OLLAMA_URL
    assert done["ollama_endpoint_fallback_used"] is True
    assert done["primary_endpoint"] == brain_loop.OLLAMA_CHAT_URL
    assert done["fallback_endpoint"] == brain_loop.OLLAMA_URL
    assert done["primary_error_kind"] == "ollama_chat_stream_error"
    assert done["primary_error_message"] == "chat endpoint rejected"


def test_deep_project_route_keeps_generate_path(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def forbidden_chat(*args, **kwargs):
        raise AssertionError("deep route should keep existing generate path")

    def fake_generate(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        yield {
            "event": "chunk",
            "text": "По суверенному ИИ есть business memory context.",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_URL,
            "primary_endpoint": brain_loop.OLLAMA_URL,
            "fallback_endpoint": "",
            "ollama_endpoint_fallback_used": False,
            "think_mode": "generate",
            "ollama_num_predict": 640,
            "ollama_temperature": 0.8,
            "ollama_top_p": 0.95,
            "pc_control_allowed": False,
        }
        yield {
            "event": "done",
            "ollama_model_used": model_id,
            "ollama_endpoint": brain_loop.OLLAMA_URL,
            "primary_endpoint": brain_loop.OLLAMA_URL,
            "fallback_endpoint": "",
            "ollama_endpoint_fallback_used": False,
            "think_mode": "generate",
            "ollama_num_predict": 640,
            "ollama_temperature": 0.8,
            "ollama_top_p": 0.95,
            "pc_control_allowed": False,
        }

    monkeypatch.setattr(brain_loop, "_stream_ollama_chat_model", forbidden_chat)
    monkeypatch.setattr(ollama_streaming, "_stream_ollama_generate_model", fake_generate)
    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Что у нас есть по продаже суверенного ИИ?", session_id="test"))
    done = events[-1]

    assert done["route_mode"] == "DEEP"
    assert done["ollama_endpoint"] == brain_loop.OLLAMA_URL
    assert done["think_mode"] == "generate"
    assert done["ollama_endpoint_fallback_used"] is False


def test_business_sovereign_command_returns_normal_response_when_ollama_succeeds(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop
    import tools.jarvis_live_runtime.ollama_streaming as ollama_streaming

    def fake_stream(
        model_id: str,
        prompt: str,
        route_mode: str,
        timeout_seconds: float | None = None,
        response_mode_text: str | None = None,
    ):
        assert model_id == "jarvis:chat8b"
        assert "enterprise_business_memory" in prompt
        assert timeout_seconds == 180.0
        assert response_mode_text == "Что у нас есть по продаже суверенного ИИ?"
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
    assert _command_timeout_seconds(None) == 180.0
