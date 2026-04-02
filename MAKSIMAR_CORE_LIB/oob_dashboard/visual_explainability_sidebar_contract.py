from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


SidebarBlockType = Literal[
    "security_block",
    "diagnostics_block",
    "explainability_block",
]

SidebarPriority = Literal[
    "primary",
    "secondary",
    "supporting",
]


@dataclass(frozen=True, slots=True)
class VisualExplainabilitySidebarEntry:
    """Canonical explainability sidebar entry for HUD right-column composition."""

    sidebar_entry_id: str
    panel_id: str
    block_type: SidebarBlockType
    sidebar_priority: SidebarPriority
    renderer_surface_id: str
    visible_in_sidebar: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualExplainabilitySidebarContract:
    """Canonical explainability sidebar contract for HUD right-column composition."""

    contract_id: str
    total_entries: int
    security_block_entries: int
    diagnostics_block_entries: int
    explainability_block_entries: int
    primary_entries: int
    secondary_entries: int
    supporting_entries: int
    visible_entries: int
    read_only_entries: int
    entries: tuple[VisualExplainabilitySidebarEntry, ...]


def _block_type_for_panel(panel_id: str) -> SidebarBlockType:
    """Resolve sidebar block type for panel."""
    if panel_id in {
        "panel_system_status_001",
        "panel_guard_chain_001",
    }:
        return "security_block"
    if panel_id in {
        "panel_incidents_001",
        "panel_logs_001",
    }:
        return "diagnostics_block"
    return "explainability_block"


def _priority_for_panel(
    panel_id: str,
    visual_priority: str,
) -> SidebarPriority:
    """Resolve sidebar priority for panel."""
    if panel_id == "panel_system_status_001":
        return "primary"
    if panel_id in {
        "panel_guard_chain_001",
        "panel_incidents_001",
        "panel_logs_001",
    }:
        return "secondary"
    if visual_priority == "primary":
        return "primary"
    if visual_priority == "secondary":
        return "secondary"
    return "supporting"


def build_visual_explainability_sidebar_contract() -> (
    VisualExplainabilitySidebarContract
):
    """Build canonical explainability sidebar contract."""
    mapping_contract = build_panel_to_visual_mapping_contract()
    render_surface_contract = build_visual_render_surface_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id

    visible_mapping_entries = tuple(
        entry
        for entry in mapping_contract.entries
        if entry.explainability_binding and entry.preferred_zone == "right_explainable"
    )

    visible_mapping_panel_ids = {entry.panel_id for entry in visible_mapping_entries}

    fixed_sidebar_panels: tuple[tuple[str, str], ...] = (
        ("panel_system_status_001", "primary"),
        ("panel_guard_chain_001", "secondary"),
        ("panel_incidents_001", "secondary"),
        ("panel_logs_001", "secondary"),
    )

    fixed_entries = tuple(
        VisualExplainabilitySidebarEntry(
            sidebar_entry_id=f"visual_sidebar_{panel_id}",
            panel_id=panel_id,
            block_type=_block_type_for_panel(panel_id),
            sidebar_priority=_priority_for_panel(panel_id, visual_priority),
            renderer_surface_id=renderer_surface_id,
            visible_in_sidebar=True,
            read_only=True,
            description=(
                f"Canonical explainability sidebar entry for {panel_id}."
            ),
        )
        for panel_id, visual_priority in fixed_sidebar_panels
    )

    mapped_entries = tuple(
        VisualExplainabilitySidebarEntry(
            sidebar_entry_id=f"visual_sidebar_{mapping_entry.panel_id}",
            panel_id=mapping_entry.panel_id,
            block_type=_block_type_for_panel(mapping_entry.panel_id),
            sidebar_priority=_priority_for_panel(
                mapping_entry.panel_id,
                mapping_entry.visual_priority,
            ),
            renderer_surface_id=renderer_surface_id,
            visible_in_sidebar=True,
            read_only=True,
            description=(
                f"Canonical explainability sidebar entry for "
                f"{mapping_entry.panel_id}."
            ),
        )
        for mapping_entry in visible_mapping_entries
        if mapping_entry.panel_id not in visible_mapping_panel_ids.intersection(
            {
                "panel_system_status_001",
                "panel_guard_chain_001",
                "panel_incidents_001",
                "panel_logs_001",
            }
        )
    )

    entries = fixed_entries + mapped_entries

    return VisualExplainabilitySidebarContract(
        contract_id="visual_explainability_sidebar_contract_001",
        total_entries=len(entries),
        security_block_entries=sum(
            1 for entry in entries if entry.block_type == "security_block"
        ),
        diagnostics_block_entries=sum(
            1 for entry in entries if entry.block_type == "diagnostics_block"
        ),
        explainability_block_entries=sum(
            1 for entry in entries if entry.block_type == "explainability_block"
        ),
        primary_entries=sum(
            1 for entry in entries if entry.sidebar_priority == "primary"
        ),
        secondary_entries=sum(
            1 for entry in entries if entry.sidebar_priority == "secondary"
        ),
        supporting_entries=sum(
            1 for entry in entries if entry.sidebar_priority == "supporting"
        ),
        visible_entries=sum(1 for entry in entries if entry.visible_in_sidebar),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
