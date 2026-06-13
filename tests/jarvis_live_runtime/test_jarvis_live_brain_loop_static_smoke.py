from pathlib import Path


def test_brain_loop_reuses_existing_runtime_and_memory_surfaces() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(
        encoding="utf-8"
    )

    assert "MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_reader" in source
    assert "run_jarvis_history_query" in source
    assert "runtime_history_store" in source
    assert "SESSION_MEMORY_ROOT" in source
    assert "SESSION_STATE_PATH" in source
    assert "canonical_memory_write_allowed" in source
    assert "pc_control_allowed" in source
    assert "build_jarvis_live_identity_prompt" in source
    assert "import httpx" in source
    assert "httpx.Client" in source
    assert "/api/chat" in source
    assert "http://127.0.0.1:11434/api/generate" in source
    assert "think=false" in source or "OLLAMA_FAST_CHAT_THINK" in source
    assert "OLLAMA_CHAT_URL" in source
    assert "jarvis-live:qwen14b" in source


def test_brain_loop_streaming_uses_ollama_stream_true_and_chunk_events() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(
        encoding="utf-8"
    )

    assert "stream_jarvis_live_brain_response" in source
    assert "_stream_ollama_chat_model" in source
    assert "_stream_ollama_generate_model" in source
    assert "_build_ollama_chat_payload" in source
    assert "_parse_ollama_chat_stream_event" in source
    assert '"stream": True' in source
    assert "messages" in source
    assert "tool_call_detected" in source
    assert "fallback_endpoint" in source
    assert "stream_chunk_count" in source
    assert "run_jarvis_live_brain_once" in source


def test_brain_loop_routes_and_guards_weather_pc_and_project_status() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(
        encoding="utf-8"
    )

    assert "build_jarvis_live_brain_health" in source
    assert "build_jarvis_live_session_status" in source
    assert "reset_jarvis_live_session" in source
    assert "build_jarvis_live_project_status_read_model" in source
    assert "_asks_weather_or_current_facts" in source
    assert "tool недоступен" in source
    assert "_asks_pc_action" in source
    assert "Прямое управление ПК выключено" in source
    assert "pc_control_allowed=false" in source


def test_brain_loop_has_no_direct_control_or_parallel_memory_markers() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(
        encoding="utf-8"
    )
    lowered = source.lower()

    assert "new memory engine" not in lowered
    assert "second memory engine" not in lowered
    for marker in (
        "shell=True",
        "pyautogui",
        "pynput",
        "keyboard.",
        "mouse.",
        "webbrowser.open",
        "powershell",
        "cmd.exe",
        "xdotool",
    ):
        assert marker.lower() not in lowered, marker
