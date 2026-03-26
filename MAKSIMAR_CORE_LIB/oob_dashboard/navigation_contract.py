from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.navigation_models import (
    DashboardNavigationContract,
    NavigationItem,
    DisplayPanelPlacement,
)


def build_dashboard_navigation_contract() -> DashboardNavigationContract:
    """Build default navigation + layout contract."""

    items = (
        NavigationItem("nav_consistency", "Consistency", "consistency", True),
        NavigationItem("nav_snapshot", "Snapshot", "snapshot", True),
        NavigationItem("nav_incident", "Incident", "incident", True),
        NavigationItem("nav_diagnostics", "Diagnostics", "diagnostics", True),
        NavigationItem("nav_chat", "Chat", "chat", True),
        NavigationItem("nav_settings", "Settings", "settings", True),
        NavigationItem("nav_gesture", "Gesture Control", "gesture_control", True),
    )

    placements = (
        # Display 0 (primary)
        DisplayPanelPlacement("panel_consistency", "consistency", 0, "left"),
        DisplayPanelPlacement("panel_snapshot", "snapshot", 0, "center"),
        DisplayPanelPlacement("panel_incident", "incident", 0, "right"),

        # Display 1 (secondary)
        DisplayPanelPlacement("panel_diagnostics", "diagnostics", 1, "left"),
        DisplayPanelPlacement("panel_chat", "chat", 1, "center"),

        # Display 2 (optional / expandable)
        DisplayPanelPlacement("panel_settings", "settings", 2, "left"),
        DisplayPanelPlacement("panel_gesture", "gesture_control", 2, "center"),
    )

    return DashboardNavigationContract(
        items=items,
        placements=placements,
        active_panel="consistency",
    )
