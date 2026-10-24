from pathlib import Path


LAUNCHER = Path("tools/jarvis_live_runtime/jarvis_live_chat_launcher.py")
HOOK = Path("tools/jarvis_live_runtime/activate_hook_snippet.sh")


def _source() -> str:
    return LAUNCHER.read_text(encoding="utf-8")


def test_chat_launcher_opens_only_terminal_client() -> None:
    source = _source()

    assert "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py" in source
    assert "subprocess.run" in source
    assert "CONTROL_PLANE.api_server:app" not in source
    assert "uvicorn" not in source
    assert "8765" not in source
    assert "Popen" not in source


def test_chat_launcher_does_not_manage_or_kill_runtime_processes() -> None:
    source = _source()

    for marker in ("killall", "pkill", "os.kill", "SIGTERM", "SIGKILL", "_matching_project_api_pids"):
        assert marker not in source
    assert "shell=True" not in source
    assert "./tools/work" in source
    assert "./tools/rest" in source


def test_chat_launcher_preserves_local_model_env_defaults() -> None:
    source = _source()

    assert '"JARVIS_LIVE_FAST_FALLBACK_ENABLED", "0"' in source
    assert '"JARVIS_HELPER_INPUT_CORRECTION_ENABLED", "true"' in source
    assert '"JARVIS_HELPER_MODEL", "jarvis:helper3b"' in source
    assert "OLLAMA_KEEP_ALIVE" not in source
    assert '"OLLAMA_NUM_PARALLEL", "1"' in source
    assert '"OLLAMA_MAX_LOADED_MODELS", "1"' in source
    assert "env=env" in source


def test_activation_hook_exposes_manual_chat_function_without_autostart() -> None:
    source = HOOK.read_text(encoding="utf-8")
    default_branch = source.split('if [ "${JARVIS_LIVE_AUTO_START:-0}" != "1" ]; then')[0]

    assert "chat()" in default_branch
    assert "jarvis_live_chat_launcher.py" in default_branch
    assert "jarvis_live_start.py --background" not in default_branch


def test_chat_launcher_does_not_import_unrelated_runtime_surfaces() -> None:
    lowered = _source().lower()

    for marker in (
        "jarvis_live_background_loop",
        "jarvis_live_start",
        "jarvis_live_voice_once",
        "watchdog",
        "vad",
        "tts",
        "screen",
        "paplay",
        "faster_whisper",
    ):
        assert marker not in lowered, marker
