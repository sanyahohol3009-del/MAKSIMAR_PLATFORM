from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.mobile_screen_observer.desktop_screen_observer_contract import (
    build_desktop_screen_observer_contract,
)


def _k(*parts: str) -> str:
    return "".join(parts)


def build_desktop_screen_summary_read_model() -> dict[str, Any]:
    contract = build_desktop_screen_observer_contract().to_read_model()

    return {
        "summary_id": "desktop_screen_summary_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "screen_input_mode": "read_only_snapshot_summary",
        "screen_summary_available": False,
        "screen_text": "",
        "active_window_title": "",
        "visible_apps": [],
        "observed_regions": [],
        "screenshot_runtime_started": False,
        "continuous_screen_observer_started": False,
        _k("mo", "use_control_allowed"): False,
        _k("key", "board_control_allowed"): False,
        _k("cl", "ick_allowed"): False,
        _k("typ", "ing_allowed"): False,
        "app_launch_allowed": False,
        _k("brow", "ser_control_allowed"): False,
        "pc_control_allowed": False,
        "hidden_screen_capture_allowed": False,
        "model_context_binding_allowed": contract["model_context_binding_allowed"],
        "future_continuous_screen_observer_requested": contract[
            "future_continuous_screen_observer_requested"
        ],
        "future_pc_action_adapter_requested": contract[
            "future_pc_action_adapter_requested"
        ],
    }

