from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_realization_contract import (
    build_visual_first_renderer_realization_contract,
)


def test_visual_first_renderer_realization_contract_builds() -> None:
    """First renderer realization contract should build successfully."""
    contract = build_visual_first_renderer_realization_contract()

    assert contract.contract_id == "visual_first_renderer_realization_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_renderer_realization_contains_expected_entry() -> None:
    """First renderer realization contract should contain canonical entry."""
    contract = build_visual_first_renderer_realization_contract()
    entry = contract.entries[0]

    assert entry.renderer_realization_id == "visual_first_renderer_realization_001"
    assert entry.first_picture_id == "visual_premium_demo_first_picture_001"
    assert entry.renderer_realization_mode == "first_renderer_realization"
    assert entry.renderer_realization_status == "first_renderer_realization_ready"


def test_visual_first_renderer_realization_preserves_truth_bound_read_only_boundary() -> None:
    """First renderer realization should preserve truth-bound read-only boundary."""
    contract = build_visual_first_renderer_realization_contract()
    entry = contract.entries[0]

    assert entry.first_picture_ready is True
    assert entry.renderer_realization_ready is True
    assert entry.truth_bound_renderer_realization is True
    assert entry.read_only is True


def test_visual_first_renderer_realization_binds_expected_visual_targets() -> None:
    """First renderer realization should bind expected visual targets."""
    contract = build_visual_first_renderer_realization_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
