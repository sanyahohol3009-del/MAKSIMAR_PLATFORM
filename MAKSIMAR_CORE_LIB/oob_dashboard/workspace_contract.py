from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_models import (
    DashboardWorkspaceContract,
    DisplayWorkspace,
    WorkspacePlacement,
)


def build_dashboard_workspace_contract() -> DashboardWorkspaceContract:
    """Build unified multi-display workspace contract."""

    displays = (
        DisplayWorkspace(display_id=0, enabled=True, zone_count=3),
        DisplayWorkspace(display_id=1, enabled=True, zone_count=2),
        DisplayWorkspace(display_id=2, enabled=True, zone_count=2),
    )

    placements = (
        WorkspacePlacement(display_id=0, zone="sidebar", panel_id="panel_navigation"),
        WorkspacePlacement(display_id=0, zone="main", panel_id="panel_consistency"),
        WorkspacePlacement(display_id=0, zone="secondary", panel_id="panel_incident"),

        WorkspacePlacement(display_id=1, zone="main", panel_id="panel_diagnostics"),
        WorkspacePlacement(display_id=1, zone="chat", panel_id="panel_chat"),

        WorkspacePlacement(display_id=2, zone="settings", panel_id="panel_settings"),
        WorkspacePlacement(display_id=2, zone="gesture", panel_id="panel_gesture_control"),
    )

    return DashboardWorkspaceContract(
        displays=displays,
        placements=placements,
    )
