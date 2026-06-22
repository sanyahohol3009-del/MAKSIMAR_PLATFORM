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
    assert "import httpx" in source
    assert "/debug ollama" in source
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
    assert "/memory recent" in source
    assert "/memory style" in source
    assert "/memory sources" in source
    assert "/models" in source
    assert "/tools" in source
    assert "/project" in source
    assert "/project status" in source
    assert "/project tree" in source
    assert "/project files" in source
    assert "/project dirty" in source
    assert "/project search" in source
    assert "/project file" in source
    assert "/project outline" in source
    assert "/project imports" in source
    assert "/project tests" in source
    assert "/project roadmap" in source
    assert "/project models" in source
    assert "/project safety" in source
    assert "/logs" in source
    assert "/debug ollama" in source
    assert "/trace on" in source
    assert "/trace off" in source
    assert "/debug on" in source
    assert "/debug off" in source
    assert "/stream" in source
    assert "/command" in source
    assert "/exit" in source
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
    assert "python -m uvicorn CONTROL_PLANE.api_server:app --host 127.0.0.1 --port 8765" in source


def test_terminal_chat_preserves_utf8_and_russian_output_path() -> None:
    source = _source()

    assert "response.iter_lines()" in source
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


def test_terminal_chat_has_long_command_timeout_and_stream_route() -> None:
    module = _module()
    source = _source()

    assert module.COMMAND_TIMEOUT_SECONDS >= 180
    assert "httpx.Client(timeout=timeout)" in source
    assert "def _print_stream_response(text: str) -> None:" in source
    assert "def _stream_json_lines(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:" in source
    assert "STREAM_URL" in source
    assert "MODELS_URL" in source


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


def test_terminal_chat_dispatches_trace_debug_and_logs_commands(monkeypatch, capsys) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_logs", lambda: calls.append("logs"))

    assert module._dispatch_user_text("/trace on") is False
    assert module._TRACE_ENABLED is True
    assert module._dispatch_user_text("/trace off") is False
    assert module._TRACE_ENABLED is False
    assert module._dispatch_user_text("/debug on") is False
    assert module._DEBUG_ENABLED is True
    assert module._dispatch_user_text("/debug off") is False
    assert module._DEBUG_ENABLED is False
    assert module._dispatch_user_text("/logs") is False
    assert calls == ["logs"]
    capsys.readouterr()


def test_terminal_chat_dispatches_memory_subcommands(monkeypatch) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_memory", lambda: calls.append("memory"))
    monkeypatch.setattr(module, "_print_memory_recent", lambda: calls.append("recent"))
    monkeypatch.setattr(module, "_print_memory_style", lambda: calls.append("style"))
    monkeypatch.setattr(module, "_print_memory_sources", lambda: calls.append("sources"))

    assert module._dispatch_user_text("/memory") is False
    assert module._dispatch_user_text("/memory recent") is False
    assert module._dispatch_user_text("/memory style") is False
    assert module._dispatch_user_text("/memory sources") is False
    assert calls == ["memory", "recent", "style", "sources"]


def test_terminal_chat_dispatches_tools_command(monkeypatch) -> None:
    module = _module()
    calls: list[str] = []

    monkeypatch.setattr(module, "_print_tools", lambda: calls.append("tools"))

    assert module._dispatch_user_text("/tools") is False
    assert calls == ["tools"]


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


def test_terminal_truth_ui_v2_operator_shell_commands_are_present() -> None:
    source = _source()

    assert "/git" in source
    assert "/diff" in source
    assert "/tests" in source
    assert "/show <file>" in source or "/show " in source
    assert "def _run_local_command(" in source
    assert "target.relative_to(root)" in source
    assert "AGENTS_INFO" not in source
    assert "SKILLS_INFO" not in source


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


def test_terminal_truth_ui_semantic_policy_deepseek_claude_cases() -> None:
    module = _module()
    facts = {
        "execution_allowed": "false",
        "proposal_only": "true",
        "canonical_write_allowed": "false",
        "pc_control_allowed": "false",
    }
    rows = [{"name": "external_adapter:mcp_python_sdk", "status": "available"}]

    factual = module._operator_block_policy(
        "проверь инструменты я сегодня буду подключать тебе много агентов инструментов и скилов",
        facts,
        rows,
    )
    assert factual["show_facts"] is True
    assert factual["show_available"] is True
    assert factual["show_closed"] is True
    assert factual["show_fact_summary"] is False
    assert factual["show_next_recommendation"] is False

    opinion = module._operator_block_policy(
        "проверь инструменты и скажи что ты думаешь",
        facts,
        rows,
    )
    assert opinion["show_fact_summary"] is True
    assert opinion["show_next_recommendation"] is False

    next_only = module._operator_block_policy(
        "проверь инструменты и скажи что делать дальше",
        facts,
        rows,
    )
    assert next_only["show_fact_summary"] is False
    assert next_only["show_next_recommendation"] is True

    both = module._operator_block_policy(
        "проверь инструменты и скажи что ты думаешь что делать дальше",
        facts,
        rows,
    )
    assert both["show_fact_summary"] is True
    assert both["show_next_recommendation"] is True


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


def test_operator_block_policy_uses_helper_semantic_route_without_template_spam() -> None:
    module = _module()

    facts = {
        "execution_allowed": "false",
        "proposal_only": "true",
        "pc_control_allowed": "false",
    }
    rows = [
        {
            "name": "external_adapter:mcp_python_sdk",
            "status": "available",
            "availability_status": "available",
        }
    ]
    helper_route = {
        "helper_model_called": True,
        "helper_model_used": True,
        "selection_source": "helper_model",
        "helper_model_id": "jarvis:helper3b",
        "helper_decision_confidence": 0.91,
        "intent_family": "EXTERNAL_ADAPTER_SELECTION",
        "selected_tools": ("external_adapter:mcp_python_sdk",),
        "selected_agent_roles": ("tool_selector_agent",),
        "risk_class": "risk_gate",
        "evidence_required": True,
        "retrieved_snippet_count": 1,
    }

    plain = module._operator_block_policy(
        "проверь инструменты",
        facts,
        rows,
        helper_route,
    )
    assert plain["helper_semantic_used"] is True
    assert plain["show_fact_summary"] is False
    assert plain["show_next_recommendation"] is False

    opinion = module._operator_block_policy(
        "проверь инструменты и скажи что ты думаешь",
        facts,
        rows,
        helper_route,
    )
    assert opinion["show_fact_summary"] is True
    assert opinion["show_next_recommendation"] is False

    next_step = module._operator_block_policy(
        "проверь инструменты и скажи что делать дальше",
        facts,
        rows,
        helper_route,
    )
    assert next_step["show_fact_summary"] is False
    assert next_step["show_next_recommendation"] is True

    both = module._operator_block_policy(
        "проверь инструменты и скажи что ты думаешь что делать дальше",
        facts,
        rows,
        helper_route,
    )
    assert both["show_fact_summary"] is True
    assert both["show_next_recommendation"] is True


def test_operator_block_policy_does_not_show_summary_without_grounded_input() -> None:
    module = _module()

    empty_route = {
        "helper_model_called": True,
        "helper_model_used": True,
        "selection_source": "helper_model",
        "intent_family": "CONVERSATION",
        "selected_tools": (),
        "selected_agent_roles": (),
        "evidence_required": False,
        "retrieved_snippet_count": 0,
    }

    policy = module._operator_block_policy(
        "скажи что ты думаешь и что делать дальше",
        {},
        [],
        empty_route,
    )

    assert policy["helper_semantic_used"] is True
    assert policy["show_fact_summary"] is False
    assert policy["show_next_recommendation"] is False


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
