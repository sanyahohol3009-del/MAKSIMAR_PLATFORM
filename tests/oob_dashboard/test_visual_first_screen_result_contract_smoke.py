from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_result_contract import (
    build_visual_first_screen_result_contract,
)


def test_visual_first_screen_result_contract_builds() -> None:
    """First screen result contract should build successfully."""
    contract = build_visual_first_screen_result_contract()

    assert contract.contract_id == "visual_first_screen_result_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_screen_result_contains_expected_entry() -> None:
    """First screen result contract should contain canonical entry."""
    contract = build_visual_first_screen_result_contract()
    entry = contract.entries[0]

    assert entry.screen_result_id == "visual_first_screen_result_001"
    assert (
        entry.screen_presentable_result_id
        == "visual_first_screen_presentable_result_001"
    )
    assert entry.screen_result_mode == "first_screen_result"
    assert entry.screen_result_status == "screen_result_ready"


def test_visual_first_screen_result_preserves_truth_bound_read_only_boundary() -> None:
    """First screen result should preserve truth-bound read-only boundary."""
    contract = build_visual_first_screen_result_contract()
    entry = contract.entries[0]

    assert entry.screen_presentable_result_ready is True
    assert entry.screen_result_ready is True
    assert entry.truth_bound_screen_result is True
    assert entry.read_only is True


def test_visual_first_screen_result_binds_expected_visual_targets() -> None:
    """First screen result should bind expected visual targets."""
    contract = build_visual_first_screen_result_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
