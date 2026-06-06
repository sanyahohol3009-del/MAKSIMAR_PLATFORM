from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_vision_status_read_model import (
    build_screen_vision_status_read_model,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_screen_vision_status_read_model_is_disabled_candidate() -> None:
    read_model = build_screen_vision_status_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["candidate_ready"] is True
    assert read_model["screen_capture_runtime_enabled"] is False
    assert read_model["ocr_runtime_enabled"] is False
    assert read_model["pixel_decode_allowed"] is False
    assert read_model["screenshot_allowed"] is False
    assert read_model["screen_recording_allowed"] is False
    assert read_model["mouse_control_allowed"] is False
    assert read_model["keyboard_control_allowed"] is False
    assert read_model["app_control_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False


def test_screen_vision_status_source_has_no_forbidden_runtime_imports() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root
        / "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/screen_vision_status_read_model.py"
    ).read_text(encoding="utf-8").lower()

    forbidden = (
        "import pil",
        "from pil",
        "import cv2",
        "from cv2",
        "pytesseract",
        "import mss",
        "from mss",
        "pyautogui",
        "keyboard.",
        "mouse.",
        "pynput",
        "win32api",
        "xlib",
        "screenshot(",
        "capture_screen(",
        "screen_record(",
        "open_display",
    )

    for marker in forbidden:
        assert marker not in source


def test_jarvis_roadmap_marks_jl6_ready_but_all_live_gates_remain_blocked() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert "JL-6" in status["ready_batches"]

    next_batch = status["next_batch"]
    if next_batch is not None:
        assert next_batch["batch_id"] != "JL-6"

    assert status["model_download_allowed_now"] == ("JL-10" in status["ready_batches"])
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False
