from pathlib import Path


LAUNCHER = Path("tools/jarvis_live_runtime/jarvis_live_chat_launcher.py")
HOOK = Path("tools/jarvis_live_runtime/activate_hook_snippet.sh")


def _source() -> str:
    return LAUNCHER.read_text(encoding="utf-8")


def test_chat_launcher_uses_canonical_control_plane_api_and_terminal_chat() -> None:
    source = _source()

    assert "CONTROL_PLANE.api_server:app" in source
    assert '"--host"' in source
    assert '"127.0.0.1"' in source
    assert '"--port"' in source
    assert '"8765"' in source
    assert "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py" in source
    assert "jarvis_live_brain_loop" not in source
    assert "jarvis_live_brain_loop_server_adapter" not in source


def test_chat_launcher_waits_for_api_before_opening_chat() -> None:
    source = _source()

    assert "HEALTH_URL" in source
    assert "def _wait_until_api_ready()" in source
    assert "if not _wait_until_api_ready():" in source
    assert "print(\"[launcher] api ready\")" in source
    assert "print(\"[launcher] opening JARVIS terminal chat\")" in source
    assert "return _run_terminal_chat(env)" in source


def test_chat_launcher_process_cleanup_is_project_api_scoped() -> None:
    source = _source()

    assert "killall" not in source
    assert "pkill" not in source
    assert "shell=True" not in source
    assert "CONTROL_PLANE.api_server:app" in source
    assert "uvicorn" in source
    assert "cwd == PROJECT_ROOT" in source
    assert "API_PORT not in cmdline" in source
    assert "def _matching_project_api_pids()" in source
    assert "def _stop_started_process" in source


def test_chat_launcher_sets_fast_local_env_defaults() -> None:
    source = _source()

    assert '"JARVIS_LIVE_FAST_FALLBACK_ENABLED", "0"' in source
    assert '"OLLAMA_KEEP_ALIVE", "30m"' in source
    assert '"OLLAMA_NUM_PARALLEL", "1"' in source
    assert '"OLLAMA_MAX_LOADED_MODELS", "1"' in source


def test_chat_launcher_does_not_import_voice_or_runtime_supervisor_surfaces() -> None:
    lowered = _source().lower()

    for marker in (
        "jarvis_live_background_loop",
        "jarvis_live_start",
        "jarvis_live_voice_once",
        "watchdog",
        "supervisor",
        "vad",
        "tts",
        "screen",
        "voice",
        "paplay",
        "faster_whisper",
    ):
        assert marker not in lowered, marker


def test_activation_hook_exposes_manual_chat_function_without_autostart() -> None:
    source = HOOK.read_text(encoding="utf-8")
    default_branch = source.split('if [ "${JARVIS_LIVE_AUTO_START:-0}" != "1" ]; then')[0]

    assert "chat()" in default_branch
    assert "jarvis_live_chat_launcher.py" in default_branch
    assert "jarvis_live_start.py --background" not in default_branch
