from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import (
    build_visual_hud_composition_contract,
)


def test_visual_hud_composition_contract_builds() -> None:
    """Visual HUD composition contract should build successfully."""
    contract = build_visual_hud_composition_contract()

    assert contract.contract_id == "visual_hud_composition_contract_001"
    assert contract.total_entries == 6
    assert contract.ready_entries == 6
    assert contract.visible_entries == 6
    assert contract.read_only_entries == 6


def test_visual_hud_composition_contains_top_status_bar_layer() -> None:
    """Visual HUD composition should contain top status bar layer."""
    contract = build_visual_hud_composition_contract()
    entry = next(
        item for item in contract.entries if item.layer_role == "top_status_bar"
    )

    assert entry.hud_layer_id == "hud_layer_top_status_bar_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.layer_state == "ready"
    assert entry.visible is True
    assert entry.read_only is True
    assert entry.z_index == 100


def test_visual_hud_composition_contains_center_render_surface_layer() -> None:
    """Visual HUD composition should contain center render surface layer."""
    contract = build_visual_hud_composition_contract()
    entry = next(
        item for item in contract.entries if item.layer_role == "center_render_surface"
    )

    assert entry.hud_layer_id == "hud_layer_center_render_surface_001"
    assert entry.layer_state == "ready"
    assert entry.visible is True
    assert entry.read_only is True
    assert entry.z_index == 50


def test_visual_hud_composition_layer_order_is_consistent() -> None:
    """Visual HUD composition should preserve canonical z-index ordering."""
    contract = build_visual_hud_composition_contract()

    z_index_map = {entry.layer_role: entry.z_index for entry in contract.entries}

    assert z_index_map["top_status_bar"] > z_index_map["right_explainability_sidebar"]
    assert z_index_map["right_explainability_sidebar"] > z_index_map["signal_overlay"]
    assert z_index_map["signal_overlay"] > z_index_map["topology_overlay"]
    assert z_index_map["topology_overlay"] > z_index_map["center_render_surface"]
    assert z_index_map["bottom_ticker"] > z_index_map["center_render_surface"]
