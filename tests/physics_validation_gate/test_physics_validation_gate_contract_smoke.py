from __future__ import annotations

from MAKSIMAR_CORE_LIB.physics_validation_gate import (
    build_physics_validation_gate_contract,
)


def test_physics_validation_gate_contract_builds() -> None:
    """Physics validation gate contract should build successfully."""
    contract = build_physics_validation_gate_contract()

    assert contract.total_entries == 4
    assert contract.approved_entries == 1
    assert contract.review_entries == 1
    assert contract.rejected_entries == 2
    assert contract.execution_allowed_entries == 1
    assert contract.validated_entries == 4


def test_physics_validation_gate_contract_contains_expected_strict_entry() -> None:
    """Physics validation gate should expose expected strict entry."""
    contract = build_physics_validation_gate_contract()
    entry = contract.entries[0]

    assert entry.gate_entry_id == "physgate_strict_physics_001"
    assert entry.simulation_mode == "strict_physics"
    assert entry.validation_decision == "approved"
    assert entry.validation_reason == "strict_execution_ready"
    assert entry.execution_allowed is True


def test_physics_validation_gate_contract_contains_expected_engineering_entry() -> None:
    """Physics validation gate should expose expected engineering entry."""
    contract = build_physics_validation_gate_contract()
    entry = contract.entries[1]

    assert entry.gate_entry_id == "physgate_engineering_realistic_001"
    assert entry.simulation_mode == "engineering_realistic"
    assert entry.validation_decision == "requires_review"
    assert entry.validation_reason == "engineering_candidate_requires_review"
    assert entry.execution_allowed is False


def test_physics_validation_gate_contract_contains_expected_research_entry() -> None:
    """Physics validation gate should expose expected research entry."""
    contract = build_physics_validation_gate_contract()
    entry = contract.entries[2]

    assert entry.gate_entry_id == "physgate_research_relaxed_001"
    assert entry.simulation_mode == "research_relaxed"
    assert entry.validation_decision == "rejected"
    assert entry.validation_reason == "research_mode_forbidden_for_execution"
    assert entry.execution_allowed is False


def test_physics_validation_gate_contract_contains_expected_control_entry() -> None:
    """Physics validation gate should expose expected control-learning entry."""
    contract = build_physics_validation_gate_contract()
    entry = contract.entries[3]

    assert entry.gate_entry_id == "physgate_control_learning_001"
    assert entry.simulation_mode == "control_learning"
    assert entry.validation_decision == "rejected"
    assert entry.validation_reason == "control_learning_forbidden_for_execution"
    assert entry.execution_allowed is False
