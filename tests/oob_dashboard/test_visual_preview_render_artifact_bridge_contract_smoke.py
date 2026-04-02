from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_artifact_bridge_contract import (
    build_visual_preview_render_artifact_bridge_contract,
)


def test_visual_preview_render_artifact_bridge_contract_builds() -> None:
    """Preview/render artifact bridge contract should build successfully."""
    contract = build_visual_preview_render_artifact_bridge_contract()

    assert contract.contract_id == "visual_preview_render_artifact_bridge_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_preview_render_artifact_bridge_contains_expected_entry() -> None:
    """Preview/render artifact bridge contract should contain canonical entry."""
    contract = build_visual_preview_render_artifact_bridge_contract()
    entry = contract.entries[0]

    assert entry.bridge_id == "visual_preview_render_artifact_bridge_001"
    assert entry.output_id == "visual_preview_render_output_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
    assert entry.bridge_mode == "preview_render_artifact_bridge"
    assert entry.bridge_status == "bridge_ready"


def test_visual_preview_render_artifact_bridge_preserves_truth_bound_read_only_boundary() -> None:
    """Preview/render artifact bridge should preserve truth-bound read-only boundary."""
    contract = build_visual_preview_render_artifact_bridge_contract()
    entry = contract.entries[0]

    assert entry.truth_bound_bridge is True
    assert entry.read_only is True


def test_visual_preview_render_artifact_bridge_binds_expected_visual_targets() -> None:
    """Preview/render artifact bridge should bind expected visual targets."""
    contract = build_visual_preview_render_artifact_bridge_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.artifact_state == "artifact_ready"
