from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_topology_overlay_contract import (
    build_visual_topology_overlay_contract,
)


def test_visual_topology_overlay_contract_builds() -> None:
    """Visual topology overlay contract should build successfully."""
    contract = build_visual_topology_overlay_contract()

    assert contract.contract_id == "visual_topology_overlay_contract_001"
    assert contract.total_entries > 0
    assert contract.read_only_entries == contract.total_entries
    assert contract.topology_visible_entries == contract.total_entries


def test_visual_topology_overlay_contains_runtime_core_anchor() -> None:
    """Visual topology overlay should contain runtime foundation anchor."""
    contract = build_visual_topology_overlay_contract()
    entry = next(
        item for item in contract.entries
        if item.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.overlay_id == "visual_topology_panel_foundation_runtime_status_001"
    assert entry.node_role == "core_anchor"
    assert entry.visual_state == "highlighted"
    assert entry.ring_layer == "inner_ring"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.read_only is True


def test_visual_topology_overlay_contains_navigation_outer_ring_entry() -> None:
    """Visual topology overlay should contain navigation outer-ring entry."""
    contract = build_visual_topology_overlay_contract()
    entry = next(
        item for item in contract.entries if item.panel_id == "panel_navigation"
    )

    assert entry.node_role == "operator_node"
    assert entry.visual_state == "passive"
    assert entry.ring_layer == "outer_ring"
    assert entry.topology_visible is True


def test_visual_topology_overlay_counts_are_consistent() -> None:
    """Visual topology overlay counts should remain internally consistent."""
    contract = build_visual_topology_overlay_contract()

    assert (
        contract.highlighted_entries
        + contract.connected_entries
        + contract.passive_entries
        == contract.total_entries
    )
    assert (
        contract.inner_ring_entries
        + contract.mid_ring_entries
        + contract.outer_ring_entries
        == contract.total_entries
    )
