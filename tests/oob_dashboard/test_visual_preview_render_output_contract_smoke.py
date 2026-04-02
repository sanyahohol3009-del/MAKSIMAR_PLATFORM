from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_output_contract import (
    build_visual_preview_render_output_contract,
)


def test_visual_preview_render_output_contract_builds() -> None:
    """Preview/render output contract should build successfully."""
    contract = build_visual_preview_render_output_contract()

    assert contract.contract_id == "visual_preview_render_output_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_preview_render_output_contains_expected_entry() -> None:
    """Preview/render output contract should contain canonical entry."""
    contract = build_visual_preview_render_output_contract()
    entry = contract.entries[0]

    assert entry.output_id == "visual_preview_render_output_001"
    assert entry.readiness_id == "visual_preview_render_polish_readiness_001"
    assert entry.render_result_id == "visual_hud_render_result_001"
    assert entry.output_mode == "phase_1_preview_render_output"
    assert entry.output_status == "output_ready"


def test_visual_preview_render_output_preserves_truth_bound_read_only_boundary() -> None:
    """Preview/render output should preserve truth-bound read-only boundary."""
    contract = build_visual_preview_render_output_contract()
    entry = contract.entries[0]

    assert entry.stable_output is True
    assert entry.truth_bound_output is True
    assert entry.read_only is True


def test_visual_preview_render_output_binds_expected_visual_targets() -> None:
    """Preview/render output should bind expected visual targets."""
    contract = build_visual_preview_render_output_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
