from pathlib import Path


def test_ios_child_bridge_does_not_call_platform_api_smoke() -> None:
    source_dir = Path("IOS_SHELL/family_child_device")
    text = "\n".join(path.read_text(encoding="utf-8") for path in source_dir.glob("*.py"))

    forbidden_markers = [
        "ReplayKit",
        "RPScreenRecorder",
        "AXUIElement",
        "UIAccessibility",
        "UIScreen.main",
        "UIGraphicsImageRenderer",
        "CGWindowListCreateImage",
        "take_screenshot",
        "capture_screenshot",
        "start_capture",
        "start_recording",
        "screenrecord",
        "subprocess",
        "socket.",
        "requests.",
        "urllib.",
        "http.client",
        "xcrun",
        "simctl",
    ]

    for marker in forbidden_markers:
        assert marker not in text
