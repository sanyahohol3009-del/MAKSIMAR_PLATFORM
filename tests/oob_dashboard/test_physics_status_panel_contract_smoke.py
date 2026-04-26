from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.physics_status_panel_contract import (
    build_physics_status_panel_contract,
)


def test_physics_status_panel_contract_builds() -> None:
    contract = build_physics_status_panel_contract()

    assert contract.panel_id == "panel_physics_status"
    assert contract.total_entries == 3
    assert contract.operator_visible is True


def test_physics_status_panel_contract_contains_expected_entries() -> None:
    contract = build_physics_status_panel_contract()

    states = tuple(
        (entry.subsystem_id, entry.physics_mode, entry.validation_state)
        for entry in contract.entries
    )

    assert states == (
        ("surface_intelligence", "engineering_realistic", "validated"),
        ("simulation_engine", "strict_physics", "validated"),
        ("candidate_evaluation", "control_learning", "review_required"),
    )
