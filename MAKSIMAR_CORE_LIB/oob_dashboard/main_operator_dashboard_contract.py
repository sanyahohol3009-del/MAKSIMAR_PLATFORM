from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_models import (
    MainOperatorDashboardContract,
    MainOperatorDashboardEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def build_main_operator_dashboard_contract() -> MainOperatorDashboardContract:
    """Build the canonical main-operator dashboard contract."""
    workspace_contract = build_workspace_registry_contract()
    workspace_ids = {entry.workspace_id for entry in workspace_contract.entries}

    primary_workspace_id = "workspace_operator_interaction"
    secondary_workspace_ids = ("workspace_foundation_monitoring",)

    if primary_workspace_id not in workspace_ids:
        raise ValueError(
            f"primary workspace missing from registry: {primary_workspace_id}"
        )

    for workspace_id in secondary_workspace_ids:
        if workspace_id not in workspace_ids:
            raise ValueError(
                f"secondary workspace missing from registry: {workspace_id}"
            )

    entries = (
        MainOperatorDashboardEntry(
            dashboard_id="main_operator_dashboard",
            dashboard_role="main_operator",
            primary_workspace_id=primary_workspace_id,
            secondary_workspace_ids=secondary_workspace_ids,
            read_only_foundation_reuse=True,
            creates_second_root=False,
            description=(
                "Canonical main operator dashboard contract reusing foundation "
                "workspaces without creating a second dashboard root."
            ),
        ),
    )

    return MainOperatorDashboardContract(entries=entries)
