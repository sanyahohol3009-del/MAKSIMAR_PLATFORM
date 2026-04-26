from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_models import (
    MainOperatorDashboardReadModelContract,
    MainOperatorDashboardReadRow,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def build_main_operator_dashboard_read_model_contract() -> (
    MainOperatorDashboardReadModelContract
):
    """Build the canonical read-model contract for the main operator dashboard."""
    dashboard_contract = build_main_operator_dashboard_contract()
    workspace_contract = build_workspace_registry_contract()

    workspace_map = {entry.workspace_id: entry for entry in workspace_contract.entries}

    rows: list[MainOperatorDashboardReadRow] = []

    for entry in dashboard_contract.entries:
        workspace_ids = (entry.primary_workspace_id,) + entry.secondary_workspace_ids
        total_panel_count = 0

        for workspace_id in workspace_ids:
            if workspace_id not in workspace_map:
                raise ValueError(f"workspace missing from registry: {workspace_id}")
            total_panel_count += len(workspace_map[workspace_id].included_panel_ids)

        rows.append(
            MainOperatorDashboardReadRow(
                dashboard_id=entry.dashboard_id,
                dashboard_role=entry.dashboard_role,
                primary_workspace_id=entry.primary_workspace_id,
                secondary_workspace_ids=entry.secondary_workspace_ids,
                total_workspace_count=len(workspace_ids),
                total_panel_count=total_panel_count,
                read_only_foundation_reuse=entry.read_only_foundation_reuse,
                supports_multimonitor_layout=True,
                supports_voice_gesture_addressing=True,
                description=(
                    "Canonical read-model row for the main operator dashboard with "
                    "workspace reuse, multimonitor awareness, and future voice/gesture "
                    "addressability."
                ),
            )
        )

    return MainOperatorDashboardReadModelContract(rows=tuple(rows))
