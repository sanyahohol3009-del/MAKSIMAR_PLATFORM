from pathlib import Path
import importlib.util
import inspect
import json

import httpx
import pytest

# Reuse the canonical endpoint's synthetic secret and temporary session/trace fixture.
from tests.control_plane.test_jarvis_live_hot_endpoint_smoke import (
    isolate_existing_hot_endpoint_state,
)


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
    module = _module()

    assert module.API_BASE_URL == "http://127.0.0.1:8000"
    assert module.HOT_URL == "http://127.0.0.1:8000/jarvis-live/hot"
    assert "/jarvis-live/hot" in source
    assert "8765" not in source
    assert "/jarvis-live/chat/stream" not in source
    assert "/jarvis-live/command" not in source
    assert 'HEALTH_URL = f"{API_BASE_URL}/health"' in source
    assert "/jarvis-live/status" in source
    assert "import httpx" in source
    assert "Every content request" in source
    assert "tools.jarvis_live_runtime.jarvis_live_brain_loop" not in source
    assert "CONTROL_PLANE.api_server" not in source


def test_terminal_chat_sends_safe_command_payload() -> None:
    source = _source()
    module = _module()

    assert '"session_id": SESSION_ID' in source
    payload = module._build_hot_payload("привет")
    verified = module.identity_from_host_token(payload["host_auth_token"])
    assert verified is not None and verified[1].owner_authorized
    assert verified[0].session_id == payload["session_id"] == module.SESSION_ID
    assert "identity" not in payload
    assert "TERMINAL_IDENTITY" not in source
    assert "pc_control_allowed" not in module._build_hot_payload("привет")
    assert "SESSION_ID = \"terminal_chat\"" in source
    assert "canonical_memory_write_allowed" in source


def test_trusted_local_terminal_identity_preserves_owner_autonomy(monkeypatch) -> None:
    import CONTROL_PLANE.api_server as api_server

    module = _module()
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: {
        "handled": True,
        "orchestration_path": "canonical_semantic_turn_v2",
        "trace_id": "terminal-owner",
        "understanding_schema_version": "request_understanding.v2",
        "understanding": {"current_topic": "project status"},
        "selected_capabilities": ("project.read",),
        "selected_provider_operation": ("inspect_git_status",),
        "selection_source": "model_semantic_registry",
        "fallback_used": False,
        "fallback_reason": "",
        "response_text": "На связи.",
        "operation_status": "COMPLETE",
        "trace": {"trace_id": "terminal-owner"},
    })

    response = api_server.jarvis_live_hot(module._build_hot_payload("покажи статус"))

    assert response["owner_pc_action_eligible"] is True
    assert response["policy_execution_allowed"] is False
    assert response["pc_executor_available"] is None
    assert response["pc_operation_authorized_for_this_turn"] is False
    assert response["executed"] is False
    assert response["execution_receipt"] is None
    assert response["pc_control_allowed"] is False


def test_terminal_chat_keeps_only_interface_commands_local() -> None:
    source = _source()

    assert "/trace on" in source
    assert "/trace off" in source
    assert "/debug on" in source
    assert "/debug off" in source
    assert "/exit" in source
    assert "canonical /jarvis-live/hot" in source
    assert "JARVIS>" in source
    assert "JARVIS terminal ready" in source


def test_terminal_chat_does_not_start_server_or_execute_local_control() -> None:
    source = _source()

    # Terminal Truth UI v2 is a local operator shell:
    # subprocess is allowed only through the allowlisted _run_local_command path
    # for /git, /diff, /tests. Dangerous direct-control surfaces remain forbidden.
    forbidden = (
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
    )

    for marker in forbidden:
        assert marker not in source
    assert "import subprocess" in source
    assert "def _run_local_command(" in source
    assert "_run_local_command((\"git\", \"status\", \"-sb\")" in source
    assert "_run_local_command((\"git\", \"diff\", \"-U5\", \"--color=always\")" in source
    assert "_print_tests((\"pytest\", \"-q\", \"--tb=short\", \"--maxfail=20\", \"tests/\"))" in source
    assert "target.relative_to(root)" in source
    assert "python -m uvicorn" not in source


def test_terminal_chat_preserves_utf8_and_russian_output_path() -> None:
    source = _source()

    assert "response.json()" in source
    assert "httpx.Timeout(COMMAND_TIMEOUT_SECONDS" in source
    assert "reconfigure(encoding=\"utf-8\"" in source
    assert "errors=\"replace\"" in source


def test_terminal_chat_sanitizes_lone_surrogate_input_before_json_payload() -> None:
    source = _source()
    module = _module()

    assert "def _sanitize_text(value: str) -> str:" in source
    assert '"text": _sanitize_text(text)' in source
    assert "def _get_user_input() -> str:" in source
    assert "_sanitize_text(text)" in source
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


def test_terminal_chat_has_long_command_timeout_and_canonical_hot_route() -> None:
    module = _module()
    source = _source()

    assert module.COMMAND_TIMEOUT_SECONDS >= 180
    assert "httpx.Client(timeout=timeout)" in source
    assert "def _print_stream_response(text: str) -> None:" in source
    assert "def _build_hot_payload(text: str) -> dict[str, Any]:" in source
    assert "HOT_URL" in source
    assert "MODELS_URL" in source


def test_terminal_chat_extracts_canonical_text_and_never_returns_empty() -> None:
    module = _module()

    assert module._canonical_response_text({"response_text": "ответ"}) == "ответ"
    assert module._canonical_response_text({"llm_response": "модель"}) == "модель"
    assert module._canonical_response_text({"result": {"response_text": "вложенный"}}) == "вложенный"
    assert module._canonical_response_text({"error_kind": "component_unavailable"})
    assert module._canonical_response_text({})


def test_terminal_chat_posts_hot_payload_and_displays_response_text(monkeypatch, capsys) -> None:
    module = _module()
    calls = []

    def fake_post(url, payload):
        calls.append((url, payload))
        return {"response_text": "На связи."}

    monkeypatch.setattr(module, "_post_json", fake_post)
    module._print_stream_response("джарвис привет")

    output = capsys.readouterr().out
    assert calls[0][0] == "http://127.0.0.1:8000/jarvis-live/hot"
    verified = module.identity_from_host_token(calls[0][1]["host_auth_token"])
    assert verified is not None and verified[1].identity_source == "authenticated_http_session"
    assert verified[0].session_id == calls[0][1]["session_id"] == module.SESSION_ID
    assert "На связи." in output


def test_terminal_chat_displays_llm_response(monkeypatch, capsys) -> None:
    module = _module()
    monkeypatch.setattr(module, "_post_json", lambda url, payload: {"llm_response": "Работаю."})

    module._print_stream_response("как дела?")

    assert "Работаю." in capsys.readouterr().out


def test_terminal_chat_prints_read_only_ollama_models_and_debug_view(capsys) -> None:
    module = _module()

    fake_payload = {
        "models": {
            "ollama_version": "{\"version\":\"0.0.0\"}",
            "ollama_tags": "{\"models\":[]}",
            "ollama_ps": "{\"models\":[]}",
            "ollama_show_primary_model": "{\"model\":\"jarvis:chat8b\"}",
            "ollama_is_local_model_engine": "true",
            "pc_control_allowed": False,
        }
    }
    module._get_json = lambda url: fake_payload

    module._print_models()
    module._print_models(verbose=True)

    output = capsys.readouterr().out
    assert "ollama_version=" in output
    assert "ollama_tags=" in output
    assert "ollama_ps=" in output
    assert "ollama_show_primary_model=" in output
    assert "debug_mode=ollama" in output


def test_terminal_chat_prints_tool_catalog_and_operator_work_trace(capsys) -> None:
    module = _module()

    fake_payload = {
        "tools": {
            "read_tools": ("repo_search", "read_file_snippet"),
            "proposal_tools": ("pytest_run_proposal", "n8n_adapter_proposal"),
            "memory_surfaces": ("runtime_history_store", "mempalace_read_only_sandbox"),
            "active_retrieval_surfaces": ("runtime_history_store",),
            "execution_allowed": False,
            "approval_required_for_actions": True,
            "pc_control_allowed": False,
        }
    }
    module._get_json = lambda url: fake_payload

    module._print_tools()
    module._set_trace(True)
    module._print_stream_event(
        '{"event":"operator_trace","intent_family":"PROJECT_SEARCH",'
        '"selected_tools":["repo_search","read_file_snippet"],'
        '"read_only":true,"execution_allowed":false}'
    )

    output = capsys.readouterr().out
    assert "read_tools=" in output
    assert "repo_search" in output
    assert "read_file_snippet" in output
    assert "proposal_tools=" in output
    assert "pytest_run_proposal" in output
    assert "n8n_adapter_proposal" in output
    assert "[infra] operator" in output
    assert "intent=PROJECT_SEARCH" in output
    assert "tools=repo_search, read_file_snippet" in output
    assert "read_only=true" in output
    assert "execution_allowed=false" in output


def test_terminal_chat_prints_compact_operator_trace(capsys) -> None:
    module = _module()

    module._set_trace(True)
    module._print_stream_event(
        '{"event":"start","request_route":"conversation","route_mode":"FAST",'
        '"retrieval_mode":"session_only","selected_model_id":"jarvis:chat8b",'
        '"selected_model_status":"installed"}'
    )
    module._print_stream_event(
        '{"event":"route_selected","context_elapsed_seconds":0.018,'
        '"retrieved_snippet_count":0,"retrieval_surfaces_used":["session_memory"],'
        '"ollama_endpoint":"http://127.0.0.1:11434/api/chat",'
        '"think_mode":"false","ollama_endpoint_fallback_used":false,'
        '"ollama_num_predict":1024,'
        '"intent_family":"PROJECT_SEARCH","selected_tools":["repo_search","read_file_snippet"],'
        '"read_only":true,"execution_allowed":false,"evidence_required":true}'
    )
    module._print_stream_metadata(
        {
            "first_chunk_elapsed_seconds": 0.72,
            "ollama_elapsed_seconds": 2.14,
            "total_elapsed_seconds": 2.19,
            "stream_chunk_count": 34,
            "selected_model_id": "jarvis:chat8b",
            "ollama_endpoint": "http://127.0.0.1:11434/api/chat",
            "primary_endpoint": "http://127.0.0.1:11434/api/chat",
            "fallback_endpoint": "http://127.0.0.1:11434/api/generate",
            "ollama_endpoint_fallback_used": False,
            "think_mode": "false",
            "ollama_num_predict": 1024,
            "ollama_temperature": 0.8,
            "ollama_top_p": 0.95,
            "intent_family": "PROJECT_SEARCH",
            "selected_tools": ("repo_search", "read_file_snippet"),
            "read_only": True,
            "execution_allowed": False,
            "evidence_count": 2,
            "grounded_answer": True,
            "ollama_called": False,
        }
    )

    output = capsys.readouterr().out
    assert "[trace] route=conversation mode=FAST memory=session_only model=jarvis:chat8b status=installed" in output
    assert "[trace] context=0.018s snippets=0 surfaces=session_memory local_memory=0 endpoint=http://127.0.0.1:11434/api/chat think_mode=false fallback_used=false num_predict=1024" in output
    assert "local_memory=0" in output
    assert "[trace] first_token=0.720s ollama=2.140s total=2.190s chunks=34" in output
    assert "[trace] endpoint=http://127.0.0.1:11434/api/chat primary=http://127.0.0.1:11434/api/chat fallback=http://127.0.0.1:11434/api/generate fallback_used=false think_mode=false num_predict=1024 temperature=0.8 top_p=0.95" in output
    assert "[trace] intent_family=PROJECT_SEARCH selected_tools=repo_search, read_file_snippet read_only=true execution_allowed=false evidence_required=true" in output
    assert "[trace] intent_family=PROJECT_SEARCH selected_tools=repo_search, read_file_snippet read_only=true execution_allowed=false evidence_count=2 grounded_answer=true ollama_called=false" in output
    assert "stream_event=start" not in output


def test_terminal_chat_suppresses_trace_metadata_by_default(capsys) -> None:
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
    assert "[trace]" not in output
    assert "selected_model_id=" not in output
    assert "retrieved_snippet_count=" not in output


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
    assert "[ERROR] ollama_empty_response model=jarvis:chat8b elapsed=57.798s" in output
    assert "[trace]" not in output


def test_terminal_chat_prints_thinking_then_answer(capsys) -> None:
    module = _module()

    module._print_stream_event(
        '{"event":"thinking","text":"Проверяю локально.","ollama_model_used":"jarvis:chat8b"}'
    )
    module._print_stream_event(
        '{"event":"chunk","text":"Готов.","ollama_model_used":"jarvis:chat8b"}'
    )

    output = capsys.readouterr().out
    assert "[ 🧠 думает... ]" in output
    assert "готово." in output
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
    assert "[ 🧠 думает... ]" in output
    assert "готово." in output
    assert "[ERROR] ollama_thinking_without_final_response model=jarvis:chat8b elapsed=1.700s" in output
    assert "Модель показала thinking, но не дала финальный ответ. Повтори короче или отключи thinking для FAST." in output


def test_terminal_chat_command_timeout_does_not_claim_api_is_down(monkeypatch, capsys) -> None:
    module = _module()

    monkeypatch.setattr(module, "_post_json", lambda url, payload: None)
    monkeypatch.setattr(module, "_get_json", lambda url: {"ok": True})
    module._LAST_API_ERROR = "timeout url=http://127.0.0.1:8000/jarvis-live/hot"

    module._print_command_response("Джарвис привет")

    output = capsys.readouterr().out
    assert "JARVIS command timed out. API is running" in output
    assert "JARVIS API is not running" not in output
    assert "api_error=timeout url=http://127.0.0.1:8000/jarvis-live/hot" in output


def test_terminal_chat_dispatches_normal_text_to_stream_by_default(monkeypatch) -> None:
    module = _module()
    calls: list[tuple[str, str]] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(("stream", text)))
    monkeypatch.setattr(module, "_print_command_response", lambda text: calls.append(("command", text)))

    assert module._dispatch_user_text("Джарвис привет") is False
    assert calls == [("stream", "Джарвис привет")]


def test_terminal_chat_migrates_legacy_command_and_stream_text_to_hot(monkeypatch) -> None:
    module = _module()
    calls: list[tuple[str, str]] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(("stream", text)))
    monkeypatch.setattr(module, "_print_command_response", lambda text: calls.append(("command", text)))

    assert module._dispatch_user_text("/command Джарвис привет") is False
    assert module._dispatch_user_text("/stream Джарвис привет") is False
    assert calls == [
        ("stream", "/command Джарвис привет"),
        ("stream", "/stream Джарвис привет"),
    ]


def test_terminal_chat_keeps_only_ui_trace_debug_local_and_routes_logs_to_hot(monkeypatch, capsys) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(text))

    assert module._dispatch_user_text("/trace on") is False
    assert module._TRACE_ENABLED is True
    assert module._dispatch_user_text("/trace off") is False
    assert module._TRACE_ENABLED is False
    assert module._dispatch_user_text("/debug on") is False
    assert module._DEBUG_ENABLED is True
    assert module._dispatch_user_text("/debug off") is False
    assert module._DEBUG_ENABLED is False
    assert module._dispatch_user_text("/logs") is False
    assert calls == ["/logs"]
    capsys.readouterr()


def test_terminal_chat_routes_memory_subcommands_to_hot(monkeypatch) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(text))

    assert module._dispatch_user_text("/memory") is False
    assert module._dispatch_user_text("/memory recent") is False
    assert module._dispatch_user_text("/memory style") is False
    assert module._dispatch_user_text("/memory sources") is False
    assert calls == ["/memory", "/memory recent", "/memory style", "/memory sources"]


def test_terminal_chat_routes_tools_command_to_hot(monkeypatch) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(text))

    assert module._dispatch_user_text("/tools") is False
    assert calls == ["/tools"]


def test_terminal_chat_dispatches_project_commands_to_stream(monkeypatch) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_stream_response", lambda text: calls.append(text))

    assert module._dispatch_user_text("/project") is False
    assert module._dispatch_user_text("/project status") is False
    assert module._dispatch_user_text("/project file tools/jarvis_live_runtime/jarvis_live_brain_loop.py 1") is False
    assert calls == [
        "/project",
        "/project status",
        "/project file tools/jarvis_live_runtime/jarvis_live_brain_loop.py 1",
    ]


def test_terminal_chat_memory_style_command_prints_stable_profile(monkeypatch, capsys) -> None:
    module = _module()

    monkeypatch.setattr(
        module,
        "_get_json",
        lambda url: {
            "ok": True,
            "session": {
                "stable_style_profile": {
                    "user_name": "Александр",
                    "assistant_identity": "JARVIS",
                    "relation_style": "брат / напарник по гаражу",
                }
            },
        },
    )

    module._print_memory_style()
    output = capsys.readouterr().out

    assert "user_name=Александр" in output
    assert "assistant_identity=JARVIS" in output
    assert "relation_style=брат / напарник по гаражу" in output


def test_terminal_chat_memory_recent_reads_existing_session_file(monkeypatch, capsys) -> None:
    module = _module()

    class FakePath:
        def __init__(self, value):
            self.value = value

        def exists(self):
            return True

        def read_text(self, encoding="utf-8"):
            return '{"recent_turns":[{"role":"user","text":"Привет"},{"role":"assistant","text":"На связи."}]}'

    monkeypatch.setattr(
        module,
        "Path",
        FakePath,
    )
    monkeypatch.setattr(
        module,
        "_get_json",
        lambda url: {"ok": True, "session": {"session_memory_path": "/runtime/jarvis_live_session_state.json"}},
    )

    module._print_memory_recent()
    output = capsys.readouterr().out

    assert "user: Привет" in output
    assert "assistant: На связи." in output


def test_terminal_chat_handles_keyboard_interrupt_during_request(monkeypatch, capsys) -> None:
    module = _module()
    monkeypatch.setattr(module, "_setup_readline", lambda: None)
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
    assert "request_interrupted=true" not in output
    assert "Traceback" not in output


def test_terminal_chat_survives_runtime_exception_and_keeps_loop_alive(monkeypatch, capsys) -> None:
    module = _module()
    monkeypatch.setattr(module, "_setup_readline", lambda: None)
    inputs = iter(["/project status", "/exit"])
    calls = {"count": 0}

    monkeypatch.setattr(module, "_print_ping", lambda startup=False: None)
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    def fail_once(text: str) -> bool:
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("boom")
        return text == "/exit"

    monkeypatch.setattr(module, "_dispatch_user_text", fail_once)

    assert module.main() == 0
    output = capsys.readouterr().out
    assert "[TERMINAL ERROR]" in output
    assert "api_log=" in output
    assert "Traceback" not in output


def test_terminal_truth_ui_v2_content_commands_use_hot_semantic_ingress() -> None:
    dispatch = inspect.getsource(_module()._dispatch_user_text)
    assert "_run_jarvis_turn(user_text)" in dispatch
    for legacy_local_action in ("_print_git_status", "_print_diff", "_print_tests", "_show_file"):
        assert legacy_local_action not in dispatch


def test_terminal_truth_ui_formats_operator_work_text(capsys) -> None:
    module = _module()
    module._render_chunk(
        "[work] intent=TOOL_CATALOG tools=repo_search,read_file_snippet "
        "read_only=true execution_allowed=false "
        "Project / repo read-only: - repo_search status=available read_only "
        "- read_file_snippet status=available read_only "
        "Action tools: - pytest_run_proposal status=proposal_only disabled "
        "direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )

    module._flush_operator_work_buffer()

    output = capsys.readouterr().out
    assert "ФАКТЫ" in output
    assert "НАЙДЕНО / ДОСТУПНО" in output
    assert "PROPOSAL ONLY" in output
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ, НЕ ROADMAP" not in output
    assert "repo_search" in output
    assert "read_file_snippet" in output
    assert "pytest_run_proposal" in output
    assert "execution_allowed=false" in output
    assert "прямое выполнение закрыто" not in output


def test_terminal_truth_ui_buffers_full_operator_work_until_done(capsys) -> None:
    module = _module()

    module._render_chunk(
        "[work] intent=EXTERNAL_ADAPTER_SELECTION tools=build_adapter "
        "read_only=true execution_allowed=false Selected external adapters: "
        "- external_adapter:mcp_python_sdk status=available selection_enabled=true "
    )
    partial = capsys.readouterr().out
    assert "ФАКТЫ" not in partial
    assert "external_adapter:mcp_python_sdk" not in partial

    module._render_chunk(
        "Semantic registry candidates: - external_adapter:autogen status=legacy_unavailable "
        "selection_enabled=false blocked_reason=legacy_alias_requires_importable_autogen_runtime "
        "direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )
    module._LAST_USER_TEXT = "проверь инструменты и дай мнение что дальше"
    module._print_stream_metadata({"selected_model_id": "jarvis:chat8b"})

    output = capsys.readouterr().out
    assert "ФАКТЫ" in output
    assert "НАЙДЕНО / ДОСТУПНО" in output
    assert "ЗАКРЫТО / НЕДОСТУПНО" in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ, НЕ ROADMAP" not in output
    assert "external_adapter:mcp_python_sdk" in output
    assert "external_adapter:autogen" in output
    assert "approval-backed operator runner" not in output


def test_terminal_truth_ui_formats_opinion_only_when_requested(capsys) -> None:
    module = _module()

    work = (
        "[work] intent=TOOL_CATALOG tools=repo_search,read_file_snippet "
        "read_only=true execution_allowed=false "
        "Project / repo read-only: - repo_search status=available read_only "
        "Action tools: - pytest_run_proposal status=proposal_only disabled "
        "direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )

    module._LAST_USER_TEXT = "проверь инструменты"
    module._render_operator_work_text(work)
    output = capsys.readouterr().out
    assert "НАЙДЕНО / ДОСТУПНО" in output
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ" not in output

    module._LAST_USER_TEXT = "проверь инструменты и дай мнение что дальше"
    module._render_operator_work_text(work)
    output = capsys.readouterr().out
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ, НЕ ROADMAP" not in output


def test_terminal_truth_ui_semantic_block_policy(capsys) -> None:
    module = _module()

    work = (
        "[work] intent=EXTERNAL_ADAPTER_SELECTION tools=build_adapter "
        "read_only=true execution_allowed=false proposal_only=true "
        "Selected external adapters: - external_adapter:mcp_python_sdk "
        "status=available selection_enabled=true import_probe_passed=true risk_class=risk_gate "
        "Semantic registry candidates: - external_adapter:autogen "
        "availability_status=legacy_unavailable selection_enabled=false "
        "direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )

    module._LAST_USER_TEXT = "проверь инструменты я сегодня буду подключать много агентов инструментов и скилов"
    module._render_operator_work_text(work)
    output = capsys.readouterr().out
    assert "ФАКТЫ" in output
    assert "НАЙДЕНО / ДОСТУПНО" in output
    assert "ЗАКРЫТО / НЕДОСТУПНО" in output
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ" not in output

    module._LAST_USER_TEXT = "проверь инструменты и дай вывод что найдено и что закрыто"
    module._render_operator_work_text(work)
    output = capsys.readouterr().out
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ" not in output

    module._LAST_USER_TEXT = "проверь инструменты и скажи что делать дальше"
    module._render_operator_work_text(work)
    output = capsys.readouterr().out
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ, НЕ ROADMAP" not in output


def test_terminal_truth_ui_detects_work_marker_split_across_chunks(capsys) -> None:
    module = _module()
    module._LAST_USER_TEXT = "проверь инструменты и скажи что ты думаешь что делать дальше"

    module._render_chunk("[wo")
    first = capsys.readouterr().out
    assert first == ""

    module._render_chunk(
        "rk] intent=EXTERNAL_ADAPTER_SELECTION tools=build_adapter "
        "read_only=true execution_allowed=false proposal_only=true "
        "Selected external adapters: - external_adapter:mcp_python_sdk "
        "status=available selection_enabled=true import_probe_passed=true risk_class=risk_gate "
        "Semantic registry candidates: - external_adapter:autogen "
        "availability_status=legacy_unavailable selection_enabled=false "
        "direct_execution_allowed=false canonical_write_allowed=false pc_control_allowed=false"
    )
    second = capsys.readouterr().out
    assert second == ""

    module._print_stream_metadata({"selected_model_id": "jarvis:chat8b"})
    output = capsys.readouterr().out

    assert "ФАКТЫ" in output
    assert "НАЙДЕНО / ДОСТУПНО" in output
    assert "ЗАКРЫТО / НЕДОСТУПНО" in output
    assert "ВЫВОД ПО ФАКТАМ" not in output
    assert "РЕКОМЕНДАЦИЯ ПО ФАКТАМ, НЕ ROADMAP" not in output
    assert "external_adapter:mcp_python_sdk" in output
    assert "external_adapter:autogen" in output


def test_terminal_operator_renderer_does_not_emit_canned_summary_or_next_steps() -> None:
    source = _source()

    forbidden = (
        "Вывод: чтение и выбор инструментов уже работают",
        "Вывод: выполнение включено",
        "Canonical write закрыт — это нормально для текущей стадии.",
        "PC-control закрыт — управление ПК ещё не включено.",
        "approval-backed operator runner",
        "Для proposal-only tools нужен proposal",
        "Закрытые adapters сначала проверять",
    )
    for marker in forbidden:
        assert marker not in source


def test_terminal_import_never_issues_a_credential(monkeypatch):
    from MAKSIMAR_CORE_LIB.security_layer import host_principal
    monkeypatch.setattr(host_principal, "bootstrap_local_owner_token",
                        lambda **_: pytest.fail("import must not bootstrap"))
    _module()


@pytest.mark.parametrize("entrypoint", ["_print_command_response", "_print_stream_response"],
                         ids=["command", "stream"])
def test_terminal_posts_fresh_signed_context_without_owner_claim(monkeypatch, capsys, tmp_path, entrypoint):
    import CONTROL_PLANE.api_server as api
    from tests.control_plane.test_jarvis_live_hot_endpoint_smoke import canonical_result
    module = _module()
    issuer = module.bootstrap_local_owner_token
    issued_sessions = []
    credentials = []
    constructor_flags = []
    requests = []
    def issue(**kwargs):
        issued_sessions.append(kwargs["session_id"])
        return issuer(**kwargs)
    monkeypatch.setattr(module, "bootstrap_local_owner_token", issue)
    monkeypatch.setattr(api, "run_canonical_semantic_turn", lambda **_: canonical_result())
    def handle(request):
        payload = json.loads(request.content)
        credentials.append(payload["host_auth_token"])
        requests.append(str(request.url))
        assert payload["session_id"] == module.SESSION_ID
        assert "identity" not in payload and "pc_control_allowed" not in payload
        result = api.jarvis_live_hot(payload)
        assert result["owner_pc_action_eligible"] is True
        assert result["pc_operation_authorized_for_this_turn"] is False
        assert result["executed"] is False and result["execution_receipt"] is None
        return httpx.Response(200, json=result)
    real_client = httpx.Client
    def client(**kwargs):
        constructor_flags.append((kwargs["trust_env"], kwargs["follow_redirects"]))
        return real_client(transport=httpx.MockTransport(handle), **kwargs)
    monkeypatch.setattr(module.httpx, "Client", client)
    for _ in range(2):
        getattr(module, entrypoint)("authenticated terminal request")
    assert issued_sessions == [module.SESSION_ID, module.SESSION_ID]
    assert requests == [module.HOT_URL, module.HOT_URL]
    assert constructor_flags == [(False, False), (False, False)]
    rendered = capsys.readouterr()
    assert all(value not in rendered.out + rendered.err for value in credentials)
    for path in tmp_path.rglob("*.json*"):
        assert all(value not in path.read_text() for value in credentials)


@pytest.mark.parametrize("case", ["missing", "forged", "expired", "wrong_payload_session",
                                  "wrong_signed_session", "non_owner", "json_owner", "malformed"])
def test_terminal_auth_rejection_precedes_http(monkeypatch, case):
    from MAKSIMAR_CORE_LIB.security_layer import host_principal as host
    module = _module()
    payload = {"text": "test", "session_id": module.SESSION_ID}
    if case not in {"missing", "json_owner"}:
        token = host.issue_host_token(host.HostPrincipal(
            "synthetic-owner", "other" if case == "wrong_signed_session" else module.SESSION_ID,
            "child" if case == "non_owner" else "owner"),
            ttl_seconds=-1 if case == "expired" else 300)
        payload["host_auth_token"] = token + ".invalid" if case == "forged" else token
    if case == "wrong_payload_session":
        payload["session_id"] = "other"
    if case == "json_owner":
        payload["identity"] = {"identity_id": "aleksandr", "profile_type": "owner", "verified": True}
    if case == "malformed":
        payload["host_auth_token"] = "body.подпись"
    monkeypatch.setattr(module.httpx, "Client", lambda **_: pytest.fail("HTTP before authenticated binding"))
    assert module._post_json(module.HOT_URL, payload) is None
    assert module._LAST_API_ERROR == "canonical_host_auth_context_required"


@pytest.mark.parametrize("case", ["failure", "empty", "none", "untyped"])
def test_terminal_failed_issuer_has_no_http_or_secret_diagnostic(monkeypatch, capsys, case):
    module = _module()
    def issue(**_):
        if case == "failure":
            raise RuntimeError("private-bootstrap-sentinel")
        return {"empty": "", "none": None, "untyped": {}}[case]
    monkeypatch.setattr(module, "bootstrap_local_owner_token", issue)
    monkeypatch.setattr(module.httpx, "Client", lambda **_: pytest.fail("failed issuer must not send HTTP"))
    with pytest.raises(RuntimeError, match="canonical_host_bootstrap") as error:
        module._build_hot_payload("test")
    assert "private-bootstrap-sentinel" not in str(error.value)
    assert error.value.__suppress_context__ or error.value.__context__ is None
    module._print_stream_response("test")
    rendered = capsys.readouterr()
    assert "private-bootstrap-sentinel" not in rendered.out + rendered.err


@pytest.mark.parametrize("url", [
    "http://0.0.0.0:8000/jarvis-live/hot", "http://192.0.2.1:8000/jarvis-live/hot",
    "http://localhost:8000/jarvis-live/hot", "http://foreign.invalid:8000/jarvis-live/hot",
    "https://127.0.0.1:8000/jarvis-live/hot", "http://127.0.0.1:8001/jarvis-live/hot",
    "http://127.0.0.1:8000/other", "http://user:pass@127.0.0.1:8000/jarvis-live/hot",
    "http://127.0.0.1:8000/jarvis-live/hot?token=untrusted",
    "http://127.0.0.1:8000/jarvis-live/hot#fragment",
    "http://127.0.0.1:8000/jarvis-live/%68ot", "http://127.0.0.1:8000/jarvis-live/hot?",
], ids=["wildcard", "remote", "hostname", "foreign", "scheme", "port", "path", "userinfo",
        "query", "fragment", "encoded_path", "empty_query"])
def test_terminal_destination_checked_before_issuance_and_send(monkeypatch, url):
    module = _module()
    monkeypatch.setattr(module, "HOT_URL", url)
    monkeypatch.setattr(module, "bootstrap_local_owner_token", lambda **_: pytest.fail("unsafe issuance"))
    monkeypatch.setattr(module, "identity_from_host_token", lambda *_: pytest.fail("unsafe destination validation"))
    monkeypatch.setattr(module.httpx, "Client", lambda **_: pytest.fail("unsafe destination send"))
    with pytest.raises(RuntimeError, match="canonical_local_host_endpoint_required"):
        module._build_hot_payload("test")
    assert module._post_json(url, {"session_id": module.SESSION_ID, "host_auth_token": "unused"}) is None


def test_terminal_wildcard_config_does_not_become_trusted(monkeypatch):
    module = _module()
    monkeypatch.setattr(module, "CONTROL_PLANE_HOST", "0.0.0.0")
    monkeypatch.setattr(module, "HOT_URL", "http://0.0.0.0:8000/jarvis-live/hot")
    monkeypatch.setattr(module, "bootstrap_local_owner_token", lambda **_: pytest.fail("wildcard issuance"))
    with pytest.raises(RuntimeError, match="canonical_local_host_endpoint_required"):
        module._build_hot_payload("test")


@pytest.mark.parametrize("status", [302, 307, 401, 403])
def test_terminal_proxy_redirect_and_auth_errors_never_forward_or_replay(monkeypatch, status):
    module = _module()
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.setenv(name, "http://proxy.invalid:3128")
    monkeypatch.delenv("NO_PROXY", raising=False)
    monkeypatch.delenv("no_proxy", raising=False)
    requests = []
    real_client = httpx.Client
    def handle(request):
        requests.append(str(request.url))
        return httpx.Response(status, headers={"Location": "http://foreign.invalid/collect"})
    def client(**kwargs):
        assert kwargs["trust_env"] is False and kwargs["follow_redirects"] is False
        return real_client(transport=httpx.MockTransport(handle), **kwargs)
    monkeypatch.setattr(module.httpx, "Client", client)
    assert module._post_json(module.HOT_URL, module._build_hot_payload("test")) is None
    assert requests == [module.HOT_URL]
    assert module._LAST_API_ERROR.startswith("http_error status=")


def test_terminal_httpx_does_not_consult_environment_proxy_configuration(monkeypatch):
    module = _module()
    monkeypatch.setenv("HTTP_PROXY", "http://proxy.invalid:3128")
    # Exercise HTTPX's real constructor with no supplied transport, so its
    # environment-proxy branch would run if trust_env were accidentally enabled.
    monkeypatch.setattr(httpx._client, "get_environment_proxies",
                        lambda: pytest.fail("environment proxy configuration consulted"))
    monkeypatch.setattr(httpx._client, "HTTPTransport", lambda **_: httpx.MockTransport(
        lambda request: httpx.Response(200, json={"response_text": "offline"})))
    result = module._post_json(module.HOT_URL, module._build_hot_payload("test"))
    assert result == {"response_text": "offline"}


@pytest.mark.parametrize("kind", ["request", "unexpected"])
def test_terminal_transport_error_does_not_expose_authenticated_payload(monkeypatch, capsys, kind):
    module = _module()
    credentials = []
    real_client = httpx.Client
    def handle(request):
        credentials.append(json.loads(request.content)["host_auth_token"])
        if kind == "request":
            raise httpx.RequestError(request.content.decode(), request=request)
        raise RuntimeError(request.content.decode())
    monkeypatch.setattr(module.httpx, "Client", lambda **kw: real_client(transport=httpx.MockTransport(handle), **kw))
    monkeypatch.setattr(module, "_get_json", lambda _: {"ok": True})
    module._set_debug(True)
    module._print_stream_response("test")
    rendered = capsys.readouterr()
    assert len(credentials) == 1
    assert credentials[0] not in rendered.out + rendered.err + module._LAST_API_ERROR
    assert "host_auth_token" not in rendered.out + rendered.err + module._LAST_API_ERROR
