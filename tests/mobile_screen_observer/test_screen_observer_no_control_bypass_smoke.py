from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.mobile_screen_observer.screen_vision_candidate_contract import (
    build_screen_vision_candidate_contract,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_vision_status_read_model import (
    build_screen_vision_status_read_model,
)


def test_screen_observer_and_dashboard_cannot_bypass_control_gates() -> None:
    contract = build_screen_vision_candidate_contract().to_read_model()
    read_model = build_screen_vision_status_read_model()

    for payload in (contract, read_model):
        assert payload["dashboard_execution_allowed"] is False
        assert payload["mouse_control_allowed"] is False
        assert payload["keyboard_control_allowed"] is False
        assert payload["app_control_allowed"] is False
        assert payload["pc_control_allowed"] is False
        assert payload["screenshot_allowed"] is False
        assert payload["screen_recording_allowed"] is False
        assert payload["pixel_decode_allowed"] is False
        assert payload["ocr_runtime_enabled"] is False
        assert payload["runtime_start_allowed"] is False


def test_jl6_source_files_do_not_contain_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = (
        root / "MAKSIMAR_CORE_LIB/mobile_screen_observer/screen_vision_candidate_contract.py",
        root
        / "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/screen_vision_status_read_model.py",
    )
    forbidden = (
        "pyautogui",
        "keyboard.",
        "mouse.",
        "pynput",
        "mss",
        "pil.imagegrab",
        "cv2",
        "pytesseract",
        "easyocr",
        "screen_record(",
        "screenshot(",
        "capture_screen(",
        "open_display",
        "win32api",
        "xlib",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        for marker in forbidden:
            assert marker not in source

