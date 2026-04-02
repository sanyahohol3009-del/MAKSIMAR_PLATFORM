from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_content_contract import (
    build_topology_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


TopologyNodeRole = Literal[
    "core_anchor",
    "topology_node",
    "operator_node",
    "mobile_node",
    "home_node",
]

TopologyVisualState = Literal[
    "highlighted",
    "connected",
    "passive",
]

TopologyRingLayer = Literal[
    "inner_ring",
    "mid_ring",
    "outer_ring",
]


@dataclass(frozen=True, slots=True)
class VisualTopologyOverlayEntry:
    """Canonical visual topology overlay entry for HUD ring composition."""

    overlay_id: str
    panel_id: str
    node_role: TopologyNodeRole
    visual_state: TopologyVisualState
    ring_layer: TopologyRingLayer
    renderer_surface_id: str
    topology_visible: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualTopologyOverlayContract:
    """Canonical visual topology overlay contract for HUD ring composition."""

    contract_id: str
    total_entries: int
    highlighted_entries: int
    connected_entries: int
    passive_entries: int
    inner_ring_entries: int
    mid_ring_entries: int
    outer_ring_entries: int
    topology_visible_entries: int
    read_only_entries: int
    entries: tuple[VisualTopologyOverlayEntry, ...]


def _node_role_for_panel(panel_id: str) -> TopologyNodeRole:
    """Resolve topology node role from canonical panel id."""
    if panel_id.startswith("panel_foundation_"):
        return "core_anchor"
    if panel_id == "panel_node_topology":
        return "topology_node"
    if panel_id == "panel_chat":
        return "operator_node"
    if panel_id == "panel_navigation":
        return "operator_node"
    if panel_id == "panel_topology_001":
        return "topology_node"
    if panel_id == "panel_system_status_001":
        return "core_anchor"
    return "topology_node"


def _visual_state_for_entry(
    *,
    panel_id: str,
    preferred_zone: str,
    topology_overlay_participation: bool,
) -> TopologyVisualState:
    """Resolve topology visual state for overlay entry."""
    if panel_id.startswith("panel_foundation_"):
        return "highlighted"
    if panel_id in {"panel_system_status_001", "panel_topology_001"}:
        return "highlighted"
    if topology_overlay_participation:
        return "connected"
    if preferred_zone in {"center_core", "center_ring"}:
        return "connected"
    return "passive"


def _ring_layer_for_entry(
    *,
    panel_id: str,
    preferred_zone: str,
) -> TopologyRingLayer:
    """Resolve topology ring layer for overlay entry."""
    if panel_id.startswith("panel_foundation_") or preferred_zone == "center_core":
        return "inner_ring"
    if preferred_zone == "center_ring":
        return "mid_ring"
    return "outer_ring"


def build_visual_topology_overlay_contract() -> VisualTopologyOverlayContract:
    """Build canonical visual topology overlay contract."""
    mapping_contract = build_panel_to_visual_mapping_contract()
    render_surface_contract = build_visual_render_surface_contract()
    topology_content_contract = build_topology_panel_content_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id
    topology_visible = topology_content_contract.entries[0].visible_in_main_dashboard

    entries = tuple(
        VisualTopologyOverlayEntry(
            overlay_id=f"visual_topology_{mapping_entry.panel_id}",
            panel_id=mapping_entry.panel_id,
            node_role=_node_role_for_panel(mapping_entry.panel_id),
            visual_state=_visual_state_for_entry(
                panel_id=mapping_entry.panel_id,
                preferred_zone=mapping_entry.preferred_zone,
                topology_overlay_participation=(
                    mapping_entry.topology_overlay_participation
                ),
            ),
            ring_layer=_ring_layer_for_entry(
                panel_id=mapping_entry.panel_id,
                preferred_zone=mapping_entry.preferred_zone,
            ),
            renderer_surface_id=renderer_surface_id,
            topology_visible=topology_visible,
            read_only=True,
            description=(
                f"Canonical visual topology overlay entry for "
                f"{mapping_entry.panel_id}."
            ),
        )
        for mapping_entry in mapping_contract.entries
        if mapping_entry.topology_overlay_participation
        or mapping_entry.panel_id in {
            "panel_navigation",
            "panel_chat",
            "panel_system_status_001",
            "panel_topology_001",
        }
    )

    return VisualTopologyOverlayContract(
        contract_id="visual_topology_overlay_contract_001",
        total_entries=len(entries),
        highlighted_entries=sum(
            1 for entry in entries if entry.visual_state == "highlighted"
        ),
        connected_entries=sum(
            1 for entry in entries if entry.visual_state == "connected"
        ),
        passive_entries=sum(1 for entry in entries if entry.visual_state == "passive"),
        inner_ring_entries=sum(
            1 for entry in entries if entry.ring_layer == "inner_ring"
        ),
        mid_ring_entries=sum(
            1 for entry in entries if entry.ring_layer == "mid_ring"
        ),
        outer_ring_entries=sum(
            1 for entry in entries if entry.ring_layer == "outer_ring"
        ),
        topology_visible_entries=sum(
            1 for entry in entries if entry.topology_visible
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
