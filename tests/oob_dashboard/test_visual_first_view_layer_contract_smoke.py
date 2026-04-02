from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_view_layer_contract import (
    build_visual_first_view_layer_contract,
)


def test_visual_first_view_layer_contract_builds() -> None:
    """First view-layer contract should build successfully."""
    contract = build_visual_first_view_layer_contract()

    assert contract.contract_id == "visual_first_view_layer_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_view_layer_contains_expected_entry() -> None:
    """First view-layer contract should contain canonical entry."""
    contract = build_visual_first_view_layer_contract()
    entry = contract.entries[0]

    assert entry.view_layer_id == "visual_first_view_layer_001"
    assert entry.operator_demo_preview_id == "visual_operator_demo_preview_001"
    assert entry.view_layer_mode == "first_view_layer"
    assert entry.view_layer_status == "view_layer_ready"


def test_visual_first_view_layer_preserves_truth_bound_read_only_boundary() -> None:
    """First view-layer should preserve truth-bound read-only boundary."""
    contract = build_visual_first_view_layer_contract()
    entry = contract.entries[0]

    assert entry.demo_ready is True
    assert entry.view_facing_ready is True
    assert entry.truth_bound_view_layer is True
    assert entry.read_only is True


def test_visual_first_view_layer_binds_expected_visual_targets() -> None:
    """First view-layer should bind expected visual targets."""
    contract = build_visual_first_view_layer_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
