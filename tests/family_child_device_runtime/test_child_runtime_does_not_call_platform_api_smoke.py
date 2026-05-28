from pathlib import Path


def test_child_runtime_does_not_call_platform_api_smoke() -> None:
    runtime_dir = Path("MAKSIMAR_SERVER/FAMILY_CHILD_DEVICE_RUNTIME")
    text = "\n".join(path.read_text(encoding="utf-8") for path in runtime_dir.glob("*.py"))

    forbidden = [
        "adb",
        "MediaProjection",
        "ReplayKit",
        "AccessibilityService",
        "subprocess",
        "socket",
        "requests.",
        "urllib.",
        "http.client",
    ]

    for marker in forbidden:
        assert marker not in text
