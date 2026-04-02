from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_operator_demo_preview_contract import (
    build_visual_operator_demo_preview_contract,
)


def test_visual_operator_demo_preview_contract_builds() -> None:
    """Operator demo preview contract should build successfully."""
    contract = build_visual_operator_demo_preview_contract()

    assert contract.contract_id == "visual_operator_demo_preview_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_operator_demo_preview_contains_expected_entry() -> None:
    """Operator demo preview contract should contain canonical entry."""
    contract = build_visual_operator_demo_preview_contract()
    entry = contract.entries[0]

    assert entry.preview_id == "visual_operator_demo_preview_001"
    assert entry.presentable_preview_id == "visual_first_presentable_preview_001"
    assert entry.preview_mode == "operator_demo_preview"
    assert entry.preview_status == "demo_preview_ready"


def test_visual_operator_demo_preview_preserves_truth_bound_read_only_boundary() -> None:
    """Operator demo preview should preserve truth-bound read-only boundary."""
    contract = build_visual_operator_demo_preview_contract()
    entry = contract.entries[0]

    assert entry.presentable_ready is True
    assert entry.operator_demo_ready is True
    assert entry.truth_bound_preview is True
    assert entry.read_only is True


def test_visual_operator_demo_preview_binds_expected_visual_targets() -> None:
    """Operator demo preview should bind expected visual targets."""
    contract = build_visual_operator_demo_preview_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
