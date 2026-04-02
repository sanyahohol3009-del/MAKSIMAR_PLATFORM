from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_showable_view_contract import (
    build_visual_first_showable_view_contract,
)


def test_visual_first_showable_view_contract_builds() -> None:
    """First showable view contract should build successfully."""
    contract = build_visual_first_showable_view_contract()

    assert contract.contract_id == "visual_first_showable_view_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_showable_view_contains_expected_entry() -> None:
    """First showable view contract should contain canonical entry."""
    contract = build_visual_first_showable_view_contract()
    entry = contract.entries[0]

    assert entry.showable_view_id == "visual_first_showable_view_001"
    assert entry.view_layer_id == "visual_first_view_layer_001"
    assert entry.showable_view_mode == "first_showable_view"
    assert entry.showable_view_status == "showable_view_ready"


def test_visual_first_showable_view_preserves_truth_bound_read_only_boundary() -> None:
    """First showable view should preserve truth-bound read-only boundary."""
    contract = build_visual_first_showable_view_contract()
    entry = contract.entries[0]

    assert entry.view_facing_ready is True
    assert entry.showable_ready is True
    assert entry.truth_bound_showable_view is True
    assert entry.read_only is True


def test_visual_first_showable_view_binds_expected_visual_targets() -> None:
    """First showable view should bind expected visual targets."""
    contract = build_visual_first_showable_view_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
