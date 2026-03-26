from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_models import (
    DashboardPanelRegistryContract,
    RegisteredPanel,
)


def build_dashboard_panel_registry_contract() -> DashboardPanelRegistryContract:
    """Build unified dashboard panel registry contract."""

    panels = (
        RegisteredPanel(
            panel_id="panel_consistency",
            label="Consistency",
            category="core",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_snapshot",
            label="Snapshot",
            category="core",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_incident",
            label="Incident",
            category="diagnostics",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_diagnostics",
            label="Diagnostics",
            category="diagnostics",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_chat",
            label="Chat",
            category="interaction",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_settings",
            label="Settings",
            category="settings",
            visible_in_sidebar=True,
        ),
        RegisteredPanel(
            panel_id="panel_gesture_control",
            label="Gesture Control",
            category="control",
            visible_in_sidebar=True,
        ),
    )

    return DashboardPanelRegistryContract(
        total_panels=len(panels),
        panels=panels,
    )
