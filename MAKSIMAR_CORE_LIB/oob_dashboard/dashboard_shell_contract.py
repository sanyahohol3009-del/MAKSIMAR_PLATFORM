from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.consistency_panel import (
    build_dashboard_consistency_panel,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_shell_models import (
    DashboardShellContract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.feedback_contract import (
    build_dashboard_feedback_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_composition_contract import (
    build_dashboard_view_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_contract import (
    build_dashboard_workspace_contract,
)


def build_dashboard_shell_contract() -> DashboardShellContract:
    """Build final shell contract for OOB dashboard."""
    consistency_panel = build_dashboard_consistency_panel()
    workspace = build_dashboard_workspace_contract()
    composition = build_dashboard_view_composition_contract()
    feedback = build_dashboard_feedback_contract()

    return DashboardShellContract(
        shell_id="oob_dashboard_shell",
        total_panels=composition.total_panels,
        total_displays=len(workspace.displays),
        total_feedback_items=feedback.total_items,
        consistency_status=consistency_panel.status,
        active_panel_id=composition.active_panel_id,
    )
