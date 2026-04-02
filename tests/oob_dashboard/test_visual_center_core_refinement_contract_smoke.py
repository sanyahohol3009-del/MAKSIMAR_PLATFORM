from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_center_core_refinement_contract import (
    build_visual_center_core_refinement_contract,
)


def test_visual_center_core_refinement_contract_builds() -> None:
    """Visual center-core refinement contract should build successfully."""
    contract = build_visual_center_core_refinement_contract()

    assert contract.contract_id == "visual_center_core_refinement_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.stronger_gravity_entries == 1
    assert contract.stronger_signal_entries == 1


def test_visual_center_core_refinement_contains_expected_entry() -> None:
    """Visual center-core refinement contract should contain canonical entry."""
    contract = build_visual_center_core_refinement_contract()
    entry = contract.entries[0]

    assert entry.refinement_id == "visual_center_core_refinement_001"
    assert entry.hierarchy_hardening_id == "visual_panel_hierarchy_hardening_001"
    assert entry.refinement_mode == "phase_1_center_core_refinement"
    assert entry.core_gravity_profile == "strong_center_gravity"
    assert entry.signal_route_profile == "readable_core_signal_routes"
    assert entry.depth_discipline_profile == "controlled_center_depth"


def test_visual_center_core_refinement_preserves_static_truthful_boundary() -> None:
    """Visual center-core refinement should preserve truthful static boundary."""
    contract = build_visual_center_core_refinement_contract()
    entry = contract.entries[0]

    assert entry.rotation_policy == "rotation_not_enabled_yet"
    assert entry.no_fake_runtime_activity is True
    assert entry.read_only is True


def test_visual_center_core_refinement_enables_allowed_phase_1_strengthening() -> None:
    """Visual center-core refinement should enable allowed Phase 1 strengthening."""
    contract = build_visual_center_core_refinement_contract()
    entry = contract.entries[0]

    assert entry.total_signal_routes > 0
    assert entry.topology_overlay_entries > 0
    assert entry.stronger_center_core_gravity is True
    assert entry.stronger_signal_route_readability is True
    assert entry.stronger_depth_hierarchy is True
