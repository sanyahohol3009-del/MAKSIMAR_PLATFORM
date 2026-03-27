from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


LayoutZone = Literal[
    "left_sidebar",
    "main_focus",
    "diagnostics_strip",
    "secondary_zone",
]

LayoutSlot = Literal[
    "slot_left_1",
    "slot_left_2",
    "slot_main_1",
    "slot_main_2",
    "slot_diag_1",
    "slot_diag_2",
    "slot_secondary_1",
    "slot_secondary_2",
]


@dataclass(frozen=True, slots=True)
class LayoutCompositionEntry:
    """Canonical layout composition entry for one panel inside a workspace."""

    workspace_id: str
    panel_id: str
    layout_zone: LayoutZone
    layout_slot: LayoutSlot
    display_target_id: str
    description: str


@dataclass(frozen=True, slots=True)
class LayoutCompositionContract:
    """Canonical layout composition contract."""

    total_entries: int
    foundation_monitoring_entries: int
    operator_surface_entries: int
    expansion_surface_entries: int
    entries: tuple[LayoutCompositionEntry, ...]


def build_layout_composition_contract() -> LayoutCompositionContract:
    """Build canonical layout composition contract."""
    workspace_contract = build_workspace_registry_contract()
    chain_contract = build_panel_view_display_chain_contract()

    workspace_map = {
        "display_secondary_diagnostics": "workspace_foundation_monitoring",
        "display_primary_operator": "workspace_operator_main",
        "display_tertiary_expansion": "workspace_expansion_observability",
    }

    valid_workspace_ids = {entry.workspace_id for entry in workspace_contract.entries}

    def resolve_layout_zone(panel_id: str, display_target_id: str) -> LayoutZone:
        if display_target_id == "display_primary_operator":
            if panel_id in ("panel_chat", "panel_settings"):
                return "main_focus"
            return "secondary_zone"
        if display_target_id == "display_secondary_diagnostics":
            if panel_id.startswith("panel_foundation_"):
                return "main_focus"
            if panel_id in ("panel_incident", "panel_diagnostics"):
                return "diagnostics_strip"
            return "left_sidebar"
        if panel_id == "panel_navigation":
            return "secondary_zone"
        return "secondary_zone"

    def resolve_layout_slot(panel_id: str, display_target_id: str) -> LayoutSlot:
        if display_target_id == "display_primary_operator":
            if panel_id == "panel_chat":
                return "slot_main_1"
            if panel_id == "panel_settings":
                return "slot_main_2"
            return "slot_secondary_1"
        if display_target_id == "display_secondary_diagnostics":
            if panel_id == "panel_foundation_runtime_status_001":
                return "slot_main_1"
            if panel_id in (
                "panel_foundation_guard_status_001",
                "panel_foundation_core_guard_status_001",
            ):
                return "slot_main_2"
            if panel_id in ("panel_incident", "panel_diagnostics"):
                return "slot_diag_1"
            return "slot_left_1"
        if panel_id == "panel_navigation":
            return "slot_secondary_2"
        return "slot_secondary_1"

    entries = tuple(
        LayoutCompositionEntry(
            workspace_id=workspace_id,
            panel_id=entry.panel_id,
            layout_zone=resolve_layout_zone(entry.panel_id, entry.display_target_id),
            layout_slot=resolve_layout_slot(entry.panel_id, entry.display_target_id),
            display_target_id=entry.display_target_id,
            description=(
                f"Canonical layout composition entry for {entry.panel_id} in {workspace_id}."
            ),
        )
        for entry in chain_contract.entries
        for workspace_id in (workspace_map[entry.display_target_id],)
        if workspace_id in valid_workspace_ids
    )

    return LayoutCompositionContract(
        total_entries=len(entries),
        foundation_monitoring_entries=sum(
            1
            for entry in entries
            if entry.workspace_id == "workspace_foundation_monitoring"
        ),
        operator_surface_entries=sum(
            1 for entry in entries if entry.workspace_id == "workspace_operator_main"
        ),
        expansion_surface_entries=sum(
            1
            for entry in entries
            if entry.workspace_id == "workspace_expansion_observability"
        ),
        entries=entries,
    )
