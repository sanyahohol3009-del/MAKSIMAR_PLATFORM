from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py"


def _source() -> str:
    return SOURCE.read_text(encoding="utf-8")


def _module():
    spec = importlib.util.spec_from_file_location("jarvis_live_terminal_chat", SOURCE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_terminal_chat_uses_existing_control_plane_routes_only() -> None:
    source = _source()

    assert "/jarvis-live/command" in source
    assert "/jarvis-live/chat/stream" in source
    assert "/jarvis-live/health" in source
    assert "/jarvis-live/status" in source
    assert "tools.jarvis_live_runtime.jarvis_live_brain_loop" not in source
    assert "CONTROL_PLANE.api_server" not in source.replace(
        "python -m uvicorn CONTROL_PLANE.api_server:app --host 127.0.0.1 --port 8765",
        "",
    )


def test_terminal_chat_sends_safe_command_payload() -> None:
    source = _source()

    assert '"session_id": SESSION_ID' in source
    assert '"pc_control_allowed": False' in source
    assert "SESSION_ID = \"terminal_chat\"" in source
    assert "canonical_memory_write_allowed" in source


def test_terminal_chat_supports_operator_commands() -> None:
    source = _source()

    assert "/ping" in source
    assert "/status" in source
    assert "/memory" in source
    assert "/models" in source
    assert "/stream" in source
    assert "/command" in source
    assert "/exit" in source
    assert "JARVIS>" in source
    assert "JARVIS terminal chat ready" in source


def test_terminal_chat_does_not_start_server_or_execute_local_control() -> None:
    source = _source()
    forbidden = (
        "subprocess",
        "os.system",
        "shell=True",
        "pyautogui",
        "pynput",
        "keyboard",
        "mouse",
        "webbrowser",
        "socket",
        "import uvicorn",
        "uvicorn.run",
        "write_text",
        "append(",
        "history",
    )

    for marker in forbidden:
        assert marker not in source
    assert "JARVIS API is not running. Start it with:" in source
    assert "python -m uvicorn CONTROL_PLANE.api_server:app --host 127.0.0.1 --port 8765" in source


def test_terminal_chat_preserves_utf8_and_russian_output_path() -> None:
    source = _source()

    assert "ensure_ascii=False" in source
    assert "decode(\"utf-8\"" in source
    assert "reconfigure(encoding=\"utf-8\"" in source
    assert "errors=\"replace\"" in source


def test_terminal_chat_sanitizes_lone_surrogate_input_before_json_payload() -> None:
    source = _source()
    module = _module()

    assert "def _sanitize_text(value: str) -> str:" in source
    assert '"text": _sanitize_text(text)' in source
    assert "_sanitize_text(input(\"JARVIS> \"))" in source
    sanitized = module._sanitize_text("Джарвис\udcd0 кто ты?")
    assert sanitized == "Джарвис? кто ты?"
    assert "\udcd0" not in sanitized


def test_terminal_chat_has_clear_api_connectivity_diagnostics() -> None:
    source = _source()

    assert "startup_ping" in source
    assert "{prefix}=failed" in source
    assert "connection_refused" in source
    assert "timeout" in source
    assert "http_error" in source
    assert "invalid_json" in source
    assert "api_error=" in source


def test_terminal_chat_has_long_command_timeout_and_stream_route() -> None:
    module = _module()
    source = _source()

    assert module.COMMAND_TIMEOUT_SECONDS >= 180
    assert "timeout=COMMAND_TIMEOUT_SECONDS" in source
    assert "def _print_stream_response(text: str) -> None:" in source
    assert "def _stream_json_lines(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:" in source
    assert "STREAM_URL" in source


def test_terminal_chat_prints_compact_operator_trace(capsys) -> None:
    module = _module()

    module._print_stream_event(
        '{"event":"start","request_route":"conversation","route_mode":"FAST",'
        '"retrieval_mode":"session_only","selected_model_id":"jarvis:chat8b",'
        '"selected_model_status":"installed"}'
    )
    module._print_stream_event(
        '{"event":"route_selected","context_elapsed_seconds":0.018,'
        '"retrieved_snippet_count":0,"retrieval_surfaces_used":["session_memory"]}'
    )
    module._print_stream_metadata(
        {
            "first_chunk_elapsed_seconds": 0.72,
            "ollama_elapsed_seconds": 2.14,
            "total_elapsed_seconds": 2.19,
            "stream_chunk_count": 34,
            "selected_model_id": "jarvis:chat8b",
        }
    )

    output = capsys.readouterr().out
    assert "[trace] route=conversation mode=FAST memory=session_only model=jarvis:chat8b status=installed" in output
    assert "[trace] context=0.018s snippets=0 surfaces=session_memory" in output
    assert "[trace] first_token=0.720s ollama=2.140s total=2.190s chunks=34" in output
    assert "stream_event=start" not in output


def test_terminal_chat_prints_empty_ollama_response_error(capsys) -> None:
    module = _module()

    module._print_stream_metadata(
        {
            "error_kind": "ollama_empty_response",
            "selected_model_id": "jarvis:chat8b",
            "ollama_elapsed_seconds": 57.798,
            "total_elapsed_seconds": 57.807,
            "stream_chunk_count": 0,
        }
    )

    output = capsys.readouterr().out
    assert "[error] ollama_empty_response model=jarvis:chat8b elapsed=57.798s" in output
    assert "[trace] first_token= ollama=57.798s total=57.807s chunks=0" in output


def test_terminal_chat_prints_thinking_then_answer(capsys) -> None:
    module = _module()

    module._print_stream_event(
        '{"event":"thinking","text":"Проверяю локально.","ollama_model_used":"jarvis:chat8b"}'
    )
    module._print_stream_event(
        '{"event":"chunk","text":"Готов.","ollama_model_used":"jarvis:chat8b"}'
    )

    output = capsys.readouterr().out
    assert "Thinking..." in output
    assert "Проверяю локально." in output
    assert "...done thinking." in output
    assert "Готов." in output


def test_terminal_chat_prints_thinking_without_final_response_error(capsys) -> None:
    module = _module()

    module._print_stream_event(
        '{"event":"thinking","text":"Думаю без ответа.","ollama_model_used":"jarvis:chat8b"}'
    )
    module._print_stream_metadata(
        {
            "error_kind": "ollama_thinking_without_final_response",
            "selected_model_id": "jarvis:chat8b",
            "ollama_elapsed_seconds": 1.7,
            "total_elapsed_seconds": 1.71,
            "thinking_chunk_count": 1,
            "answer_chunk_count": 0,
            "stream_chunk_count": 1,
            "had_thinking": True,
        }
    )

    output = capsys.readouterr().out
    assert "Thinking..." in output
    assert "Думаю без ответа." in output
    assert "...done thinking." in output
    assert "[error] ollama_thinking_without_final_response model=jarvis:chat8b elapsed=1.700s" in output


def test_terminal_chat_command_timeout_does_not_claim_api_is_down(monkeypatch, capsys) -> None:
    module = _module()

    monkeypatch.setattr(module, "_post_json", lambda url, payload: None)
    monkeypatch.setattr(module, "_get_json", lambda url: {"ok": True})
    module._LAST_API_ERROR = "timeout url=http://127.0.0.1:8765/jarvis-live/command"

    module._print_command_response("Джарвис привет")

    output = capsys.readouterr().out
    assert "JARVIS command timed out. API is running" in output
    assert "JARVIS API is not running" not in output
    assert "api_error=timeout url=http://127.0.0.1:8765/jarvis-live/command" in output


def test_terminal_chat_dispatches_normal_text_to_stream_by_default(monkeypatch) -> None:
    module = _module()
    calls: list[tuple[str, str]] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(("stream", text)))
    monkeypatch.setattr(module, "_print_command_response", lambda text: calls.append(("command", text)))

    assert module._dispatch_user_text("Джарвис привет") is False
    assert calls == [("stream", "Джарвис привет")]


def test_terminal_chat_dispatches_explicit_command_and_stream(monkeypatch) -> None:
    module = _module()
    calls: list[tuple[str, str]] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(("stream", text)))
    monkeypatch.setattr(module, "_print_command_response", lambda text: calls.append(("command", text)))

    assert module._dispatch_user_text("/command Джарвис привет") is False
    assert module._dispatch_user_text("/stream Джарвис привет") is False
    assert calls == [("command", "Джарвис привет"), ("stream", "Джарвис привет")]


def test_terminal_chat_handles_keyboard_interrupt_during_request(monkeypatch, capsys) -> None:
    module = _module()
    inputs = iter(["Джарвис привет", "/exit"])

    monkeypatch.setattr(module, "_print_ping", lambda startup=False: None)
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    def interrupt_once(user_text: str) -> bool:
        if user_text == "Джарвис привет":
            raise KeyboardInterrupt
        return True

    monkeypatch.setattr(module, "_dispatch_user_text", interrupt_once)

    assert module.main() == 0
    output = capsys.readouterr().out
    assert "request_interrupted=true" in output
    assert "Traceback" not in output
