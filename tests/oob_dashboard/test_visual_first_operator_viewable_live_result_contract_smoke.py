from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_operator_viewable_live_result_contract import (
    build_visual_first_operator_viewable_live_result_contract,
)


def test_visual_first_operator_viewable_live_result_contract_builds() -> None:
    """First operator-viewable live result contract should build successfully."""
    contract = build_visual_first_operator_viewable_live_result_contract()

    assert (
        contract.contract_id
        == "visual_first_operator_viewable_live_result_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_operator_viewable_live_result_contains_expected_entry() -> None:
    """First operator-viewable live result contract should contain canonical entry."""
    contract = build_visual_first_operator_viewable_live_result_contract()
    entry = contract.entries[0]

    assert (
        entry.operator_viewable_live_result_id
        == "visual_first_operator_viewable_live_result_001"
    )
    assert entry.live_showcase_result_id == "visual_first_live_showcase_result_001"
    assert (
        entry.operator_viewable_live_result_mode
        == "first_operator_viewable_live_result"
    )
    assert (
        entry.operator_viewable_live_result_status
        == "operator_viewable_live_result_ready"
    )


def test_visual_first_operator_viewable_live_result_preserves_truth_bound_read_only_boundary() -> None:
    """First operator-viewable live result should preserve truth-bound read-only boundary."""
    contract = build_visual_first_operator_viewable_live_result_contract()
    entry = contract.entries[0]

    assert entry.live_showcase_result_ready is True
    assert entry.operator_viewable_live_result_ready is True
    assert entry.truth_bound_operator_viewable_live_result is True
    assert entry.read_only is True


def test_visual_first_operator_viewable_live_result_binds_expected_visual_targets() -> None:
    """First operator-viewable live result should bind expected visual targets."""
    contract = build_visual_first_operator_viewable_live_result_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
