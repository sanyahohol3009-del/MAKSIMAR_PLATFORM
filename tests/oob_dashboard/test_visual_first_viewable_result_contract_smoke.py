from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_viewable_result_contract import (
    build_visual_first_viewable_result_contract,
)


def test_visual_first_viewable_result_contract_builds() -> None:
    """First viewable result contract should build successfully."""
    contract = build_visual_first_viewable_result_contract()

    assert contract.contract_id == "visual_first_viewable_result_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_viewable_result_contains_expected_entry() -> None:
    """First viewable result contract should contain canonical entry."""
    contract = build_visual_first_viewable_result_contract()
    entry = contract.entries[0]

    assert entry.viewable_result_id == "visual_first_viewable_result_001"
    assert entry.result_display_id == "visual_first_result_display_001"
    assert entry.viewable_result_mode == "first_viewable_result"
    assert entry.viewable_result_status == "viewable_result_ready"


def test_visual_first_viewable_result_preserves_truth_bound_read_only_boundary() -> None:
    """First viewable result should preserve truth-bound read-only boundary."""
    contract = build_visual_first_viewable_result_contract()
    entry = contract.entries[0]

    assert entry.result_ready is True
    assert entry.viewable_result_ready is True
    assert entry.truth_bound_viewable_result is True
    assert entry.read_only is True


def test_visual_first_viewable_result_binds_expected_visual_targets() -> None:
    """First viewable result should bind expected visual targets."""
    contract = build_visual_first_viewable_result_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
