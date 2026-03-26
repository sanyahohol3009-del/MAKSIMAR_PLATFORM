from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_panel_models import (
    DashboardGesturePanel,
    GestureBinding,
)


def build_dashboard_gesture_panel() -> DashboardGesturePanel:
    """Build gesture control panel contract."""

    bindings = (
        GestureBinding(gesture="swipe", action="switch_panel", enabled=True),
        GestureBinding(gesture="drag", action="move_panel", enabled=True),
        GestureBinding(gesture="pinch", action="zoom_view", enabled=True),
        GestureBinding(gesture="tap", action="select", enabled=True),
    )

    return DashboardGesturePanel(
        panel_id="panel_gesture_control",
        bindings=bindings,
    )
