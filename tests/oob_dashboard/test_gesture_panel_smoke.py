from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_gesture_panel,
)


def test_gesture_panel_builds() -> None:
    panel = build_dashboard_gesture_panel()

    assert panel.panel_id == "panel_gesture_control"
    assert len(panel.bindings) >= 1
