from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_present_contract import (
    build_visual_first_screen_present_contract,
)


def test_visual_first_screen_present_contract_builds() -> None:
    """First screen-present contract should build successfully."""
    contract = build_visual_first_screen_present_contract()

    assert contract.contract_id == "visual_first_screen_present_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_screen_present_contains_expected_entry() -> None:
    """First screen-present contract should contain canonical entry."""
    contract = build_visual_first_screen_present_contract()
    entry = contract.entries[0]

    assert entry.screen_present_id == "visual_first_screen_present_001"
    assert entry.screen_render_ready_id == "visual_first_screen_render_ready_001"
    assert entry.screen_present_mode == "first_screen_present"
    assert entry.screen_present_status == "first_screen_present_ready"


def test_visual_first_screen_present_preserves_truth_bound_read_only_boundary() -> None:
    """First screen-present should preserve truth-bound read-only boundary."""
    contract = build_visual_first_screen_present_contract()
    entry = contract.entries[0]

    assert entry.screen_render_ready is True
    assert entry.screen_present_ready is True
    assert entry.truth_bound_screen_present is True
    assert entry.read_only is True


def test_visual_first_screen_present_binds_expected_visual_targets() -> None:
    """First screen-present should bind expected visual targets."""
    contract = build_visual_first_screen_present_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
