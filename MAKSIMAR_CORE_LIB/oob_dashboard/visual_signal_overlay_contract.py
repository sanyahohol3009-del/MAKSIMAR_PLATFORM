from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


SignalLineStyle = Literal[
    "core_stream",
    "diagnostic_stream",
    "topology_stream",
    "operator_stream",
]

SignalLineState = Literal[
    "active",
    "passive",
    "highlighted",
]

SignalAnchorRole = Literal[
    "core",
    "left_navigation",
    "right_explainable",
    "right_operator",
    "center_ring",
    "bottom_status",
]


@dataclass(frozen=True, slots=True)
class VisualSignalOverlayEntry:
    """Canonical visual signal overlay entry for renderer-visible routing lines."""

    signal_id: str
    source_panel_id: str
    target_anchor_role: SignalAnchorRole
    line_style: SignalLineStyle
    line_state: SignalLineState
    renderer_surface_id: str
    visual_priority: str
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualSignalOverlayContract:
    """Canonical visual signal overlay contract for renderer-visible routing lines."""

    contract_id: str
    total_entries: int
    active_entries: int
    passive_entries: int
    highlighted_entries: int
    core_stream_entries: int
    diagnostics_stream_entries: int
    topology_stream_entries: int
    operator_stream_entries: int
    read_only_entries: int
    entries: tuple[VisualSignalOverlayEntry, ...]


def _style_for_panel_state_class(panel_state_class: str) -> SignalLineStyle:
    """Resolve signal line style from canonical panel state class."""
    if panel_state_class == "foundation":
        return "core_stream"
    if panel_state_class == "diagnostics":
        return "diagnostic_stream"
    if panel_state_class == "topology":
        return "topology_stream"
    return "operator_stream"


def _state_for_panel(
    *,
    panel_id: str,
    signal_overlay_participation: bool,
    preferred_zone: str,
) -> SignalLineState:
    """Resolve signal line state from panel mapping semantics."""
    if panel_id == "panel_navigation":
        return "passive"
    if panel_id.startswith("panel_foundation_"):
        return "highlighted"
    if signal_overlay_participation:
        return "active"
    if preferred_zone in {"right_explainable", "right_operator"}:
        return "active"
    return "passive"


def _target_anchor_role_for_zone(preferred_zone: str) -> SignalAnchorRole:
    """Resolve signal anchor role from canonical preferred visual zone."""
    if preferred_zone == "left_navigation":
        return "left_navigation"
    if preferred_zone == "right_explainable":
        return "right_explainable"
    if preferred_zone == "right_operator":
        return "right_operator"
    if preferred_zone == "center_ring":
        return "center_ring"
    if preferred_zone == "bottom_status":
        return "bottom_status"
    return "core"


def build_visual_signal_overlay_contract() -> VisualSignalOverlayContract:
    """Build canonical visual signal overlay contract."""
    mapping_contract = build_panel_to_visual_mapping_contract()
    metadata_contract = build_panel_metadata_contract()
    panel_chain_contract = build_panel_view_display_chain_contract()
    render_surface_contract = build_visual_render_surface_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id

    panel_state_class_by_panel_id = {
        entry.panel_id: entry.panel_state_class for entry in metadata_contract.entries
    }
    chain_panel_ids = {entry.panel_id for entry in panel_chain_contract.entries}

    entries = tuple(
        VisualSignalOverlayEntry(
            signal_id=f"visual_signal_{mapping_entry.panel_id}",
            source_panel_id=mapping_entry.panel_id,
            target_anchor_role=_target_anchor_role_for_zone(
                mapping_entry.preferred_zone
            ),
            line_style=_style_for_panel_state_class(
                panel_state_class_by_panel_id[mapping_entry.panel_id]
            ),
            line_state=_state_for_panel(
                panel_id=mapping_entry.panel_id,
                signal_overlay_participation=(
                    mapping_entry.signal_overlay_participation
                    or mapping_entry.panel_id in chain_panel_ids
                ),
                preferred_zone=mapping_entry.preferred_zone,
            ),
            renderer_surface_id=renderer_surface_id,
            visual_priority=mapping_entry.visual_priority,
            read_only=True,
            description=(
                f"Canonical visual signal overlay entry for "
                f"{mapping_entry.panel_id}."
            ),
        )
        for mapping_entry in mapping_contract.entries
    )

    return VisualSignalOverlayContract(
        contract_id="visual_signal_overlay_contract_001",
        total_entries=len(entries),
        active_entries=sum(1 for entry in entries if entry.line_state == "active"),
        passive_entries=sum(1 for entry in entries if entry.line_state == "passive"),
        highlighted_entries=sum(
            1 for entry in entries if entry.line_state == "highlighted"
        ),
        core_stream_entries=sum(
            1 for entry in entries if entry.line_style == "core_stream"
        ),
        diagnostics_stream_entries=sum(
            1 for entry in entries if entry.line_style == "diagnostic_stream"
        ),
        topology_stream_entries=sum(
            1 for entry in entries if entry.line_style == "topology_stream"
        ),
        operator_stream_entries=sum(
            1 for entry in entries if entry.line_style == "operator_stream"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
