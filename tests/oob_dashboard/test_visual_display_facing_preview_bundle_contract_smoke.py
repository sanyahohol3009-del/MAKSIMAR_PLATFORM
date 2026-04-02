from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_display_facing_preview_bundle_contract import (
    build_visual_display_facing_preview_bundle_contract,
)


def test_visual_display_facing_preview_bundle_contract_builds() -> None:
    """Display-facing preview bundle contract should build successfully."""
    contract = build_visual_display_facing_preview_bundle_contract()

    assert contract.contract_id == "visual_display_facing_preview_bundle_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_display_facing_preview_bundle_contains_expected_entry() -> None:
    """Display-facing preview bundle contract should contain canonical entry."""
    contract = build_visual_display_facing_preview_bundle_contract()
    entry = contract.entries[0]

    assert entry.bundle_id == "visual_display_facing_preview_bundle_001"
    assert entry.bridge_id == "visual_preview_render_artifact_bridge_001"
    assert entry.preview_state_id == "visual_hud_preview_state_001"
    assert entry.bundle_mode == "display_facing_preview_bundle"
    assert entry.bundle_status == "bundle_ready"


def test_visual_display_facing_preview_bundle_preserves_truth_bound_read_only_boundary() -> None:
    """Display-facing preview bundle should preserve truth-bound read-only boundary."""
    contract = build_visual_display_facing_preview_bundle_contract()
    entry = contract.entries[0]

    assert entry.display_facing_ready is True
    assert entry.truth_bound_bundle is True
    assert entry.read_only is True


def test_visual_display_facing_preview_bundle_binds_expected_visual_targets() -> None:
    """Display-facing preview bundle should bind expected visual targets."""
    contract = build_visual_display_facing_preview_bundle_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
