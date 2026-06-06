from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.mobile_screen_observer.screen_vision_candidate_contract import (
    build_screen_vision_candidate_contract,
)


def build_screen_vision_status_read_model() -> dict[str, Any]:
    candidate = build_screen_vision_candidate_contract().to_read_model()
    return {
        "summary_id": "screen_vision_status_read_model_v0_1",
        "candidate_ready": True,
        "candidate_roles": candidate["candidate_roles"],
        "candidate_role_ids": candidate["candidate_role_ids"],
        "source_surfaces": candidate["source_surfaces"],
        "read_only": True,
        "dashboard_safe": True,
        "screen_capture_runtime_enabled": False,
        "ocr_runtime_enabled": False,
        "pixel_decode_allowed": False,
        "screenshot_allowed": False,
        "screen_recording_allowed": False,
        "mouse_control_allowed": False,
        "keyboard_control_allowed": False,
        "app_control_allowed": False,
        "pc_control_allowed": False,
        "model_download_allowed": False,
        "runtime_start_allowed": False,
        "dashboard_execution_allowed": False,
    }

