from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_sidebar_navigation_refinement_contract import (
    build_visual_sidebar_navigation_refinement_contract,
)


def test_visual_sidebar_navigation_refinement_contract_builds() -> None:
    """Visual sidebar/navigation refinement contract should build successfully."""
    contract = build_visual_sidebar_navigation_refinement_contract()

    assert contract.contract_id == "visual_sidebar_navigation_refinement_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.stronger_navigation_entries == 1
    assert contract.stronger_sidebar_entries == 1


def test_visual_sidebar_navigation_refinement_contains_expected_entry() -> None:
    """Visual sidebar/navigation refinement contract should contain canonical entry."""
    contract = build_visual_sidebar_navigation_refinement_contract()
    entry = contract.entries[0]

    assert entry.refinement_id == "visual_sidebar_navigation_refinement_001"
    assert entry.center_core_refinement_id == "visual_center_core_refinement_001"
    assert entry.hierarchy_hardening_id == "visual_panel_hierarchy_hardening_001"
    assert entry.refinement_mode == "phase_1_sidebar_navigation_refinement"
    assert entry.navigation_clarity_profile == "strong_left_navigation_readability"
    assert entry.sidebar_clarity_profile == "strong_right_explainability_readability"
    assert entry.operator_trust_profile == "clear_operator_guidance"


def test_visual_sidebar_navigation_refinement_preserves_read_only_boundary() -> None:
    """Visual sidebar/navigation refinement should preserve read-only boundary."""
    contract = build_visual_sidebar_navigation_refinement_contract()
    entry = contract.entries[0]

    assert entry.read_only is True
    assert entry.explainability_entries > 0


def test_visual_sidebar_navigation_refinement_enables_allowed_phase_1_strengthening() -> None:
    """Visual sidebar/navigation refinement should enable allowed Phase 1 strengthening."""
    contract = build_visual_sidebar_navigation_refinement_contract()
    entry = contract.entries[0]

    assert entry.stronger_left_navigation_hierarchy is True
    assert entry.stronger_right_sidebar_hierarchy is True
    assert entry.stronger_active_state_readability is True
    assert entry.stronger_operator_guidance_clarity is True
