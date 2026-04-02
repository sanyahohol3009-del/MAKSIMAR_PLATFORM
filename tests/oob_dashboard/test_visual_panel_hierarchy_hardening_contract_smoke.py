from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_panel_hierarchy_hardening_contract import (
    build_visual_panel_hierarchy_hardening_contract,
)


def test_visual_panel_hierarchy_hardening_contract_builds() -> None:
    """Visual panel hierarchy hardening contract should build successfully."""
    contract = build_visual_panel_hierarchy_hardening_contract()

    assert contract.contract_id == "visual_panel_hierarchy_hardening_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.stronger_foundation_entries == 1
    assert contract.stronger_operator_entries == 1


def test_visual_panel_hierarchy_hardening_contains_expected_entry() -> None:
    """Visual panel hierarchy hardening contract should contain canonical entry."""
    contract = build_visual_panel_hierarchy_hardening_contract()
    entry = contract.entries[0]

    assert entry.hardening_id == "visual_panel_hierarchy_hardening_001"
    assert entry.theme_hardening_id == "visual_theme_hardening_001"
    assert entry.hierarchy_hardening_mode == "phase_1_panel_hierarchy_hardening"
    assert entry.emphasis_profile == "operator_hud_priority_stack"
    assert entry.frame_consistency_profile == "premium_hud_frame_consistency"


def test_visual_panel_hierarchy_hardening_preserves_read_only_phase_1_boundary() -> None:
    """Visual panel hierarchy hardening should preserve read-only Phase 1 boundary."""
    contract = build_visual_panel_hierarchy_hardening_contract()
    entry = contract.entries[0]

    assert entry.read_only is True
    assert entry.total_panels > 0
    assert entry.primary_panels >= 0
    assert entry.secondary_panels >= 0
    assert entry.supporting_panels >= 0


def test_visual_panel_hierarchy_hardening_enables_allowed_hierarchy_strengthening() -> None:
    """Visual panel hierarchy hardening should enable allowed hierarchy strengthening."""
    contract = build_visual_panel_hierarchy_hardening_contract()
    entry = contract.entries[0]

    assert entry.stronger_foundation_hierarchy is True
    assert entry.stronger_operator_hierarchy is True
    assert entry.stronger_explainability_hierarchy is True
    assert entry.stronger_navigation_hierarchy is True
