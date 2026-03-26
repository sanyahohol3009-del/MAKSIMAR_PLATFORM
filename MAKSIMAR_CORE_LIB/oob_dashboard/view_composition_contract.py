from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_orchestration_contract import (
    build_dashboard_panel_orchestration_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_dashboard_panel_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_composition_models import (
    ComposedViewPanel,
    DashboardViewCompositionContract,
)


def build_dashboard_view_composition_contract() -> DashboardViewCompositionContract:
    """Build unified dashboard view composition contract."""
    orchestration = build_dashboard_panel_orchestration_contract()
    registry = build_dashboard_panel_registry_contract()

    visible_panel_ids = {
        panel.panel_id
        for panel in registry.panels
        if panel.visible_in_sidebar
    }

    composed_panels = tuple(
        ComposedViewPanel(
            panel_id=panel.panel_id,
            display_id=panel.display_id,
            zone=panel.zone,
            visible=panel.panel_id in visible_panel_ids,
            active=panel.active,
        )
        for panel in orchestration.panels
    )

    return DashboardViewCompositionContract(
        total_panels=len(composed_panels),
        composed_panels=composed_panels,
        active_panel_id=orchestration.active_panel_id,
    )
