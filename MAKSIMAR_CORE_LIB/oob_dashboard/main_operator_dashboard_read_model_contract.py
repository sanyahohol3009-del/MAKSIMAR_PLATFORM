from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_contract import (
    build_workspace_read_model_contract,
)


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardReadModelEntry:
    """Canonical read-only main operator dashboard entry."""

    dashboard_id: str
    workspace_id: str
    display_target_id: str
    total_panels: int
    main_focus_panels: int
    secondary_panels: int
    diagnostics_panels: int
    sidebar_panels: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class MainOperatorDashboardReadModelContract:
    """Canonical main operator dashboard read model contract."""

    total_entries: int
    read_only_entries: int
    interactive_entries: int
    entries: tuple[MainOperatorDashboardReadModelEntry, ...]


def build_main_operator_dashboard_read_model_contract() -> (
    MainOperatorDashboardReadModelContract
):
    """Build canonical main operator dashboard read model contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    workspace_read_model_contract = build_workspace_read_model_contract()
    layout_contract = build_layout_composition_contract()

    workspace_read_model_map = {
        entry.workspace_id: entry for entry in workspace_read_model_contract.entries
    }

    entries = tuple(
        MainOperatorDashboardReadModelEntry(
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            display_target_id=dashboard_entry.display_target_id,
            total_panels=dashboard_entry.total_panels,
            main_focus_panels=workspace_read_model_map[
                dashboard_entry.workspace_id
            ].main_focus_panels,
            secondary_panels=workspace_read_model_map[
                dashboard_entry.workspace_id
            ].secondary_panels,
            diagnostics_panels=workspace_read_model_map[
                dashboard_entry.workspace_id
            ].diagnostics_panels,
            sidebar_panels=workspace_read_model_map[
                dashboard_entry.workspace_id
            ].sidebar_panels,
            read_only=dashboard_entry.read_only,
            description=(
                f"Canonical main operator dashboard read model entry for "
                f"{dashboard_entry.workspace_id}."
            ),
        )
        for dashboard_entry in dashboard_contract.entries
        if any(
            layout_entry.workspace_id == dashboard_entry.workspace_id
            for layout_entry in layout_contract.entries
        )
    )

    return MainOperatorDashboardReadModelContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        interactive_entries=sum(1 for entry in entries if not entry.read_only),
        entries=entries,
    )
