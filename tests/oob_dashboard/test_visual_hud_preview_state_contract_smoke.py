from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_state_contract import (
    build_visual_hud_preview_state_contract,
)


def test_visual_hud_preview_state_contract_builds() -> None:
    """Visual HUD preview state contract should build successfully."""
    contract = build_visual_hud_preview_state_contract()

    assert contract.contract_id == "visual_hud_preview_state_contract_001"
    assert contract.total_entries == 1
    assert contract.stable_entries == 1
    assert contract.partial_entries == 0
    assert contract.read_only_entries == 1


def test_visual_hud_preview_state_contains_expected_entry() -> None:
    """Visual HUD preview state should contain canonical preview state entry."""
    contract = build_visual_hud_preview_state_contract()
    entry = contract.entries[0]

    assert entry.preview_state_id == "visual_hud_preview_state_001"
    assert entry.artifact_id == "visual_hud_preview_artifact_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.preview_state_mode == "operator_hud_preview_state"
    assert entry.preview_state_status == "stable"
    assert entry.read_only is True


def test_visual_hud_preview_state_preserves_expected_layer_bindings() -> None:
    """Visual HUD preview state should preserve canonical layer bindings."""
    contract = build_visual_hud_preview_state_contract()
    entry = contract.entries[0]

    assert entry.top_layer_id == "hud_layer_top_status_bar_001"
    assert entry.center_layer_id == "hud_layer_center_render_surface_001"
    assert entry.bottom_layer_id == "hud_layer_bottom_ticker_001"
    assert (
        entry.right_sidebar_layer_id
        == "hud_layer_right_explainability_sidebar_001"
    )


def test_visual_hud_preview_state_totals_are_consistent() -> None:
    """Visual HUD preview state totals should remain internally consistent."""
    contract = build_visual_hud_preview_state_contract()
    entry = contract.entries[0]

    assert entry.total_layers == 6
    assert entry.visible_layers == 6
    assert contract.total_visible_layers == entry.visible_layers
