from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_premium_demo_system_contract import (
    build_visual_first_premium_demo_system_contract,
)


def test_visual_first_premium_demo_system_contract_builds() -> None:
    """First premium demo system contract should build successfully."""
    contract = build_visual_first_premium_demo_system_contract()

    assert contract.contract_id == "visual_first_premium_demo_system_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_first_premium_demo_system_contains_expected_entry() -> None:
    """First premium demo system contract should contain canonical entry."""
    contract = build_visual_first_premium_demo_system_contract()
    entry = contract.entries[0]

    assert entry.premium_demo_system_id == "visual_first_premium_demo_system_001"
    assert entry.premium_showable_system_id == "visual_first_premium_showable_system_001"
    assert entry.premium_demo_system_mode == "first_premium_demo_system"
    assert entry.premium_demo_system_status == "premium_demo_system_ready"


def test_visual_first_premium_demo_system_preserves_truth_bound_read_only_boundary() -> None:
    """First premium demo system should preserve truth-bound read-only boundary."""
    contract = build_visual_first_premium_demo_system_contract()
    entry = contract.entries[0]

    assert entry.premium_showable_system_ready is True
    assert entry.premium_demo_system_ready is True
    assert entry.truth_bound_premium_demo_system is True
    assert entry.read_only is True


def test_visual_first_premium_demo_system_binds_expected_visual_targets() -> None:
    """First premium demo system should bind expected visual targets."""
    contract = build_visual_first_premium_demo_system_contract()
    entry = contract.entries[0]

    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.screen_id == "visual_hud_screen_001"
    assert entry.preview_artifact_id == "visual_hud_preview_artifact_001"
