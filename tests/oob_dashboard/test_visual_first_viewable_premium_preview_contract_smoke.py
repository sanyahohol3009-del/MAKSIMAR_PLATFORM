from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_viewable_premium_preview_contract import (
    build_visual_first_viewable_premium_preview_contract,
)


def test_visual_first_viewable_premium_preview_contract_builds() -> None:
    """First viewable premium preview contract should build successfully."""
    contract = build_visual_first_viewable_premium_preview_contract()

    assert (
        contract.contract_id
        == "visual_first_viewable_premium_preview_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_viewable_premium_preview_contains_expected_entry() -> None:
    """First viewable premium preview contract should contain canonical entry."""
    contract = build_visual_first_viewable_premium_preview_contract()
    entry = contract.entries[0]

    assert entry.preview_id == "visual_first_viewable_premium_preview_001"
    assert (
        entry.operator_preview_id
        == "visual_operator_facing_premium_preview_001"
    )
    assert entry.preview_mode == "first_viewable_premium_preview"
    assert entry.preview_status == "viewable_preview_ready"


def test_visual_first_viewable_premium_preview_preserves_truth_bound_read_only_boundary() -> None:
    """First viewable premium preview should preserve truth-bound read-only boundary."""
    contract = build_visual_first_viewable_premium_preview_contract()
    entry = contract.entries[0]

    assert entry.operator_facing_ready is True
    assert entry.display_facing_ready is True
    assert entry.truth_bound_preview is True
    assert entry.read_only is True


def test_visual_first_viewable_premium_preview_binds_expected_visual_targets() -> None:
    """First viewable premium preview should bind expected visual targets."""
    contract = build_visual_first_viewable_premium_preview_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
