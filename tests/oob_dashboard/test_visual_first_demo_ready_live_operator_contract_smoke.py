from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_demo_ready_live_operator_contract import (
    build_visual_first_demo_ready_live_operator_contract,
)


def test_visual_first_demo_ready_live_operator_contract_builds() -> None:
    """First demo-ready live operator contract should build successfully."""
    contract = build_visual_first_demo_ready_live_operator_contract()

    assert (
        contract.contract_id
        == "visual_first_demo_ready_live_operator_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_demo_ready_live_operator_contains_expected_entry() -> None:
    """First demo-ready live operator contract should contain canonical entry."""
    contract = build_visual_first_demo_ready_live_operator_contract()
    entry = contract.entries[0]

    assert (
        entry.demo_ready_live_operator_id
        == "visual_first_demo_ready_live_operator_001"
    )
    assert (
        entry.live_operator_showcase_id
        == "visual_first_live_operator_showcase_001"
    )
    assert entry.demo_ready_live_operator_mode == "first_demo_ready_live_operator"
    assert (
        entry.demo_ready_live_operator_status
        == "demo_ready_live_operator_ready"
    )


def test_visual_first_demo_ready_live_operator_preserves_truth_bound_read_only_boundary() -> None:
    """First demo-ready live operator should preserve truth-bound read-only boundary."""
    contract = build_visual_first_demo_ready_live_operator_contract()
    entry = contract.entries[0]

    assert entry.live_operator_showcase_ready is True
    assert entry.demo_ready_live_operator_ready is True
    assert entry.truth_bound_demo_ready_live_operator is True
    assert entry.read_only is True


def test_visual_first_demo_ready_live_operator_binds_expected_visual_targets() -> None:
    """First demo-ready live operator should bind expected visual targets."""
    contract = build_visual_first_demo_ready_live_operator_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
