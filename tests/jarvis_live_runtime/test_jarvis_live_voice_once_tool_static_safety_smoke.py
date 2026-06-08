from pathlib import Path


def test_voice_once_tool_static_safety_and_runtime_cache_binding() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_voice_once.py").read_text(
        encoding="utf-8"
    )
    lowered = source.lower()

    assert "download_root" in lowered
    assert "faster_whisper_model_root" in lowered
    assert "rdpsource" in lowered
    assert "pc_control_allowed=false" in lowered
    for marker in (
        "shell=True",
        "pyautogui",
        "pynput",
        "keyboard",
        "mouse",
        "webbrowser",
        "socket",
        "flask",
        "fastapi",
        "uvicorn",
        "powershell",
        "cmd.exe",
    ):
        assert marker.lower() not in lowered, marker
