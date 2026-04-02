from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import (
    build_visual_hud_snapshot_contract,
)


def test_visual_hud_snapshot_contract_builds() -> None:
    """Visual HUD snapshot contract should build successfully."""
    contract = build_visual_hud_snapshot_contract()

    assert contract.contract_id == "visual_hud_snapshot_contract_001"
    assert contract.total_entries == 1
    assert contract.preview_ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_hud_snapshot_contains_expected_entry() -> None:
    """Visual HUD snapshot should contain canonical preview-ready entry."""
    contract = build_visual_hud_snapshot_contract()
    entry = contract.entries[0]

    assert entry.snapshot_id == "visual_hud_snapshot_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.total_layers == 6
    assert entry.visible_layers == 6
    assert entry.ready_layers == 6
    assert entry.read_only is True
    assert entry.preview_ready is True


def test_visual_hud_snapshot_contains_expected_anchor_layers() -> None:
    """Visual HUD snapshot should expose top, center, bottom, and sidebar layers."""
    contract = build_visual_hud_snapshot_contract()
    entry = contract.entries[0]

    assert entry.top_layer_id == "hud_layer_top_status_bar_001"
    assert entry.center_layer_id == "hud_layer_center_render_surface_001"
    assert entry.bottom_layer_id == "hud_layer_bottom_ticker_001"
    assert (
        entry.right_sidebar_layer_id
        == "hud_layer_right_explainability_sidebar_001"
    )


def test_visual_hud_snapshot_totals_are_consistent() -> None:
    """Visual HUD snapshot totals should remain internally consistent."""
    contract = build_visual_hud_snapshot_contract()
    entry = contract.entries[0]

    assert contract.total_visible_layers == entry.visible_layers
    assert contract.total_ready_layers == entry.ready_layers
    assert entry.visible_layers <= entry.total_layers
    assert entry.ready_layers <= entry.total_layers
