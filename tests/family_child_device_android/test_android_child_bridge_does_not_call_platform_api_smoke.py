from pathlib import Path


def test_android_child_bridge_does_not_call_platform_api_smoke() -> None:
    source_dir = Path("ANDROID_SHELL/family_child_device")
    text = "\n".join(path.read_text(encoding="utf-8") for path in source_dir.glob("*.py"))

    forbidden_markers = [
        "MediaProjection",
        "AccessibilityService",
        "subprocess",
        "socket.",
        "requests.",
        "urllib.",
        "http.client",
        "adb ",
        "uiautomator",
        "input tap",
        "input text",
        "screencap",
        "screenrecord",
    ]

    for marker in forbidden_markers:
        assert marker not in text
