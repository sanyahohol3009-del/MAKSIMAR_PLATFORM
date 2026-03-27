from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_contract import (
    build_workspace_read_model_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardEntry:
    """Canonical main operator dashboard entry."""

    dashboard_id: str
    workspace_id: str
    display_target_id: str
    total_panels: int
    main_focus_panels: int
    secondary_panels: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardContract:
    """Canonical main operator dashboard contract."""

    total_entries: int
    operator_workspace_entries: int
    read_only_entries: int
    interactive_entries: int
    entries: tuple[MainOperatorDashboardEntry, ...]


def build_main_operator_dashboard_contract() -> MainOperatorDashboardContract:
    """Build canonical main operator dashboard contract."""
    workspace_registry_contract = build_workspace_registry_contract()
    workspace_read_model_contract = build_workspace_read_model_contract()
    layout_contract = build_layout_composition_contract()

    workspace_registry_map = {
        entry.workspace_id: entry for entry in workspace_registry_contract.entries
    }
    workspace_read_model_map = {
        entry.workspace_id: entry for entry in workspace_read_model_contract.entries
    }

    operator_workspace_ids = tuple(
        entry.workspace_id
        for entry in workspace_registry_contract.entries
        if entry.workspace_role == "operator_surface"
    )

    entries = tuple(
        MainOperatorDashboardEntry(
            dashboard_id="dashboard_main_operator_001",
            workspace_id=workspace_id,
            display_target_id=workspace_registry_map[workspace_id].display_target_id,
            total_panels=workspace_read_model_map[workspace_id].total_panels,
            main_focus_panels=workspace_read_model_map[workspace_id].main_focus_panels,
            secondary_panels=workspace_read_model_map[workspace_id].secondary_panels,
            read_only=workspace_registry_map[workspace_id].read_only,
            description=(
                f"Canonical main operator dashboard entry for {workspace_id}."
            ),
        )
        for workspace_id in operator_workspace_ids
        if any(
            layout_entry.workspace_id == workspace_id
            for layout_entry in layout_contract.entries
        )
    )

    return MainOperatorDashboardContract(
        total_entries=len(entries),
        operator_workspace_entries=len(operator_workspace_ids),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        interactive_entries=sum(1 for entry in entries if not entry.read_only),
        entries=entries,
    )
