from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_models import (
    OperatorWorkspaceBindingContract,
    OperatorWorkspaceBindingEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def build_operator_workspace_binding_contract() -> OperatorWorkspaceBindingContract:
    """Build the canonical operator-workspace binding contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    workspace_contract = build_workspace_registry_contract()

    workspace_ids = {entry.workspace_id for entry in workspace_contract.entries}
    entries: list[OperatorWorkspaceBindingEntry] = []

    for dashboard_entry in dashboard_contract.entries:
        ordered_workspace_ids = (
            (dashboard_entry.primary_workspace_id,) + dashboard_entry.secondary_workspace_ids
        )

        for order, workspace_id in enumerate(ordered_workspace_ids):
            if workspace_id not in workspace_ids:
                raise ValueError(f"workspace missing from registry: {workspace_id}")

            entries.append(
                OperatorWorkspaceBindingEntry(
                    dashboard_id=dashboard_entry.dashboard_id,
                    workspace_id=workspace_id,
                    binding_role=(
                        "primary_operator_workspace"
                        if workspace_id == dashboard_entry.primary_workspace_id
                        else "secondary_foundation_workspace"
                    ),
                    workspace_order=order,
                    is_primary_workspace=workspace_id == dashboard_entry.primary_workspace_id,
                    read_only_binding=True,
                    description=(
                        f"Canonical operator workspace binding for "
                        f"{dashboard_entry.dashboard_id} -> {workspace_id}."
                    ),
                )
            )

    return OperatorWorkspaceBindingContract(entries=tuple(entries))
