from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_realization_output_contract import (
    build_visual_premium_demo_realization_output_contract,
)


def test_visual_premium_demo_realization_output_contract_builds() -> None:
    """Premium demo realization output contract should build successfully."""
    contract = build_visual_premium_demo_realization_output_contract()

    assert contract.contract_id == "visual_premium_demo_realization_output_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_premium_demo_realization_output_contains_expected_entry() -> None:
    """Premium demo realization output contract should contain canonical entry."""
    contract = build_visual_premium_demo_realization_output_contract()
    entry = contract.entries[0]

    assert entry.realization_output_id == "visual_premium_demo_realization_output_001"
    assert entry.realization_artifact_id == "visual_premium_demo_realization_artifact_001"
    assert entry.realization_output_mode == "premium_demo_realization_output"
    assert entry.realization_output_status == "premium_demo_realization_output_ready"


def test_visual_premium_demo_realization_output_preserves_truth_bound_read_only_boundary() -> None:
    """Premium demo realization output should preserve truth-bound read-only boundary."""
    contract = build_visual_premium_demo_realization_output_contract()
    entry = contract.entries[0]

    assert entry.realization_artifact_ready is True
    assert entry.realization_output_ready is True
    assert entry.truth_bound_realization_output is True
    assert entry.read_only is True


def test_visual_premium_demo_realization_output_binds_expected_visual_targets() -> None:
    """Premium demo realization output should bind expected visual targets."""
    contract = build_visual_premium_demo_realization_output_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
