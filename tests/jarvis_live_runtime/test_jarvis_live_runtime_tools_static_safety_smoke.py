from pathlib import Path


TOOL_FILES = (
    Path("tools/jarvis_live_runtime/jarvis_live_start.py"),
    Path("tools/jarvis_live_runtime/jarvis_live_stop.py"),
    Path("tools/jarvis_live_runtime/jarvis_live_status.py"),
    Path("tools/jarvis_live_runtime/jarvis_live_background_loop.py"),
    Path("tools/jarvis_live_runtime/install_venv_activation_hook.py"),
    Path("tools/jarvis_live_runtime/activate_hook_snippet.sh"),
)


def test_runtime_tools_static_safety() -> None:
    forbidden = (
        "shell=True",
        "pkill",
        "killall",
        "pyautogui",
        "pynput",
        "xdotool",
        "keyboard.write",
        "mouse.click",
        "webbrowser.open",
        "powershell",
        "cmd.exe",
        "socket",
        "flask",
        "fastapi",
        "uvicorn",
        "rm -rf",
    )
    for path in TOOL_FILES:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in forbidden:
            assert marker.lower() not in lowered, (path, marker)


def test_runtime_tools_use_only_controlled_external_audio_commands() -> None:
    background_text = Path(
        "tools/jarvis_live_runtime/jarvis_live_background_loop.py"
    ).read_text(encoding="utf-8")
    assert '"parec"' in background_text
    assert '"paplay"' in background_text
    assert "subprocess.Popen" in background_text
    assert "subprocess.run" in background_text
    assert "shell=True" not in background_text
    assert "pc_control_allowed\": False" in background_text


def test_start_tool_uses_dedicated_faster_whisper_runtime_python_fallback() -> None:
    start_text = Path("tools/jarvis_live_runtime/jarvis_live_start.py").read_text(
        encoding="utf-8"
    )

    assert "JARVIS_LIVE_RUNTIME_PYTHON" in start_text
    assert "faster_whisper_stt" in start_text
    assert '"bin" / "python"' in start_text
    assert "_runtime_python()" in start_text
    assert "[runtime_python, str(BACKGROUND_LOOP)]" in start_text
    assert "subprocess.Popen" in start_text
    assert "shell=True" not in start_text
    assert "pyautogui" not in start_text
    assert "pynput" not in start_text
    assert "keyboard" not in start_text
    assert "mouse" not in start_text
    assert "webbrowser" not in start_text
    assert "powershell" not in start_text.lower()
    assert "cmd.exe" not in start_text.lower()
    assert "socket" not in start_text.lower()
