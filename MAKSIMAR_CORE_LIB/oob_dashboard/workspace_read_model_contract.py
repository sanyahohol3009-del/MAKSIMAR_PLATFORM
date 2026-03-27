from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


@dataclass(frozen=True, slots=True)
class WorkspaceReadModelEntry:
    """Canonical read-only workspace entry."""

    workspace_id: str
    workspace_role: str
    display_target_id: str
    total_panels: int
    main_focus_panels: int
    diagnostics_panels: int
    sidebar_panels: int
    secondary_panels: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class WorkspaceReadModelContract:
    """Canonical workspace read model contract."""

    total_entries: int
    read_only_entries: int
    operator_surface_entries: int
    entries: tuple[WorkspaceReadModelEntry, ...]


def build_workspace_read_model_contract() -> WorkspaceReadModelContract:
    """Build canonical workspace read model contract."""
    workspace_contract = build_workspace_registry_contract()
    layout_contract = build_layout_composition_contract()
    chain_contract = build_panel_view_display_chain_contract()

    chain_panel_ids = {entry.panel_id for entry in chain_contract.entries}

    entries = tuple(
        WorkspaceReadModelEntry(
            workspace_id=workspace_entry.workspace_id,
            workspace_role=workspace_entry.workspace_role,
            display_target_id=workspace_entry.display_target_id,
            total_panels=sum(
                1
                for layout_entry in layout_contract.entries
                if layout_entry.workspace_id == workspace_entry.workspace_id
                and layout_entry.panel_id in chain_panel_ids
            ),
            main_focus_panels=sum(
                1
                for layout_entry in layout_contract.entries
                if layout_entry.workspace_id == workspace_entry.workspace_id
                and layout_entry.layout_zone == "main_focus"
            ),
            diagnostics_panels=sum(
                1
                for layout_entry in layout_contract.entries
                if layout_entry.workspace_id == workspace_entry.workspace_id
                and layout_entry.layout_zone == "diagnostics_strip"
            ),
            sidebar_panels=sum(
                1
                for layout_entry in layout_contract.entries
                if layout_entry.workspace_id == workspace_entry.workspace_id
                and layout_entry.layout_zone == "left_sidebar"
            ),
            secondary_panels=sum(
                1
                for layout_entry in layout_contract.entries
                if layout_entry.workspace_id == workspace_entry.workspace_id
                and layout_entry.layout_zone == "secondary_zone"
            ),
            read_only=workspace_entry.read_only,
            description=(
                f"Canonical workspace read model entry for {workspace_entry.workspace_id}."
            ),
        )
        for workspace_entry in workspace_contract.entries
    )

    return WorkspaceReadModelContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        operator_surface_entries=sum(
            1 for entry in entries if entry.workspace_role == "operator_surface"
        ),
        entries=entries,
    )
