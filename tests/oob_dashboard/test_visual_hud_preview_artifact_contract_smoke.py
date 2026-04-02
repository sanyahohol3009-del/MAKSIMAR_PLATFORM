from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_artifact_contract import (
    build_visual_hud_preview_artifact_contract,
)


def test_visual_hud_preview_artifact_contract_builds() -> None:
    """Visual HUD preview artifact contract should build successfully."""
    contract = build_visual_hud_preview_artifact_contract()

    assert contract.contract_id == "visual_hud_preview_artifact_contract_001"
    assert contract.total_entries == 1
    assert contract.artifact_ready_entries == 1
    assert contract.artifact_partial_entries == 0
    assert contract.read_only_entries == 1


def test_visual_hud_preview_artifact_contains_expected_entry() -> None:
    """Visual HUD preview artifact should contain canonical artifact entry."""
    contract = build_visual_hud_preview_artifact_contract()
    entry = contract.entries[0]

    assert entry.artifact_id == "visual_hud_preview_artifact_001"
    assert entry.render_result_id == "visual_hud_render_result_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.artifact_format == "hud_preview_bundle"
    assert entry.artifact_state == "artifact_ready"
    assert entry.read_only is True


def test_visual_hud_preview_artifact_preserves_expected_layer_bindings() -> None:
    """Visual HUD preview artifact should preserve canonical layer bindings."""
    contract = build_visual_hud_preview_artifact_contract()
    entry = contract.entries[0]

    assert entry.top_layer_id == "hud_layer_top_status_bar_001"
    assert entry.center_layer_id == "hud_layer_center_render_surface_001"
    assert entry.bottom_layer_id == "hud_layer_bottom_ticker_001"
    assert (
        entry.right_sidebar_layer_id
        == "hud_layer_right_explainability_sidebar_001"
    )


def test_visual_hud_preview_artifact_totals_are_consistent() -> None:
    """Visual HUD preview artifact totals should remain internally consistent."""
    contract = build_visual_hud_preview_artifact_contract()
    entry = contract.entries[0]

    assert entry.total_layers == 6
    assert entry.visible_layers == 6
    assert contract.total_visible_layers == entry.visible_layers
