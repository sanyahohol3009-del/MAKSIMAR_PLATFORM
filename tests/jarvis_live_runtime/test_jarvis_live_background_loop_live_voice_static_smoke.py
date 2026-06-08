from pathlib import Path


def test_background_loop_live_voice_static_safety() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_background_loop.py").read_text(
        encoding="utf-8"
    )
    lowered = source.lower()

    assert "jarvis_live_always_listen" in lowered
    assert "jarvis_live_listen_seconds" in lowered
    assert "download_root" in lowered
    assert "runtime_models\" / \"faster_whisper" in lowered
    assert "owner_detected" in lowered
    assert "latest_voice_reply" in lowered
    assert '"pc_control_allowed": false' in lowered
    assert "rdpsource" in lowered
    for marker in (
        "shell=True",
        "pyautogui",
        "pynput",
        "keyboard.",
        "keyboardinterrupt",
        "mouse.",
        "webbrowser",
        "socket",
        "flask",
        "fastapi",
        "uvicorn",
        "powershell",
        "cmd.exe",
        "xdotool",
    ):
        assert marker.lower() not in lowered, marker
