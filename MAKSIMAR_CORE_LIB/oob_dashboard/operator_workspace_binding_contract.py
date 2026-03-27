from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingEntry:
    """Canonical binding between operator dashboard and workspace."""

    dashboard_id: str
    workspace_id: str
    workspace_role: str
    display_target_id: str
    is_primary_operator_workspace: bool
    supports_interaction: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingContract:
    """Canonical operator workspace binding contract."""

    total_entries: int
    primary_operator_workspace_entries: int
    interactive_entries: int
    read_only_entries: int
    entries: tuple[OperatorWorkspaceBindingEntry, ...]


def build_operator_workspace_binding_contract() -> (
    OperatorWorkspaceBindingContract
):
    """Build canonical operator workspace binding contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    dashboard_read_model_contract = build_main_operator_dashboard_read_model_contract()
    workspace_registry_contract = build_workspace_registry_contract()

    workspace_registry_map = {
        entry.workspace_id: entry for entry in workspace_registry_contract.entries
    }
    dashboard_read_model_map = {
        entry.workspace_id: entry for entry in dashboard_read_model_contract.entries
    }

    entries = tuple(
        OperatorWorkspaceBindingEntry(
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            workspace_role=workspace_registry_map[dashboard_entry.workspace_id].workspace_role,
            display_target_id=dashboard_entry.display_target_id,
            is_primary_operator_workspace=(
                workspace_registry_map[dashboard_entry.workspace_id].workspace_role
                == "operator_surface"
            ),
            supports_interaction=not dashboard_read_model_map[
                dashboard_entry.workspace_id
            ].read_only,
            read_only=dashboard_read_model_map[dashboard_entry.workspace_id].read_only,
            description=(
                f"Canonical operator workspace binding entry for "
                f"{dashboard_entry.workspace_id}."
            ),
        )
        for dashboard_entry in dashboard_contract.entries
        if dashboard_entry.workspace_id in workspace_registry_map
        and dashboard_entry.workspace_id in dashboard_read_model_map
    )

    return OperatorWorkspaceBindingContract(
        total_entries=len(entries),
        primary_operator_workspace_entries=sum(
            1 for entry in entries if entry.is_primary_operator_workspace
        ),
        interactive_entries=sum(1 for entry in entries if entry.supports_interaction),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
