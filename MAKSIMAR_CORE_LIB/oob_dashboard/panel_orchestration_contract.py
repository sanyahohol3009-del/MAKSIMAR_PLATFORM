from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.input_router_contract import (
    build_dashboard_input_router_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.navigation_contract import (
    build_dashboard_navigation_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_orchestration_models import (
    DashboardPanelOrchestrationContract,
    OrchestratedPanel,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_contract import (
    build_dashboard_workspace_contract,
)


def _resolve_active_panel_id(active_panel: str) -> str:
    """Resolve normalized active panel id from navigation active panel."""
    return f"panel_{active_panel}"


def build_dashboard_panel_orchestration_contract() -> DashboardPanelOrchestrationContract:
    """Build unified dashboard panel orchestration contract."""
    navigation = build_dashboard_navigation_contract()
    workspace = build_dashboard_workspace_contract()
    input_router = build_dashboard_input_router_contract()

    resolved_active_panel_id = _resolve_active_panel_id(navigation.active_panel)

    panels = tuple(
        OrchestratedPanel(
            panel_id=placement.panel_id,
            active=placement.panel_id == resolved_active_panel_id,
            display_id=placement.display_id,
            zone=placement.zone,
        )
        for placement in workspace.placements
    )

    active_panel_id = next(
        (panel.panel_id for panel in panels if panel.active),
        panels[0].panel_id,
    )

    return DashboardPanelOrchestrationContract(
        panels=panels,
        active_panel_id=active_panel_id,
        navigation_enabled=True,
        input_routing_enabled=input_router.supports_navigation_routing,
    )
