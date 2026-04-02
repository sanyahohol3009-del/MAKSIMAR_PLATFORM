from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presentable_display_contract import (
    build_visual_first_presentable_display_contract,
)


def test_visual_first_presentable_display_contract_builds() -> None:
    """First presentable display contract should build successfully."""
    contract = build_visual_first_presentable_display_contract()

    assert contract.contract_id == "visual_first_presentable_display_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_presentable_display_contains_expected_entry() -> None:
    """First presentable display contract should contain canonical entry."""
    contract = build_visual_first_presentable_display_contract()
    entry = contract.entries[0]

    assert entry.display_id == "visual_first_presentable_display_001"
    assert entry.displayable_view_id == "visual_first_displayable_view_001"
    assert entry.display_mode == "first_presentable_display"
    assert entry.display_status == "presentable_display_ready"


def test_visual_first_presentable_display_preserves_truth_bound_read_only_boundary() -> None:
    """First presentable display should preserve truth-bound read-only boundary."""
    contract = build_visual_first_presentable_display_contract()
    entry = contract.entries[0]

    assert entry.displayable_ready is True
    assert entry.presentable_display_ready is True
    assert entry.truth_bound_display is True
    assert entry.read_only is True


def test_visual_first_presentable_display_binds_expected_visual_targets() -> None:
    """First presentable display should bind expected visual targets."""
    contract = build_visual_first_presentable_display_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
