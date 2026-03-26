from __future__ import annotations

from MAKSIMAR_CORE_LIB.constraint_profile_registry import (
    build_constraint_profile_registry_contract,
)


def test_constraint_profile_registry_contract_builds() -> None:
    """Constraint profile registry contract should build successfully."""
    contract = build_constraint_profile_registry_contract()

    assert contract.total_entries == 4
    assert contract.production_allowed_entries == 2
    assert contract.research_only_entries == 2
    assert contract.validation_gate_entries == 2
    assert contract.registered_entries == 4


def test_constraint_profile_registry_contract_contains_expected_strict_entry() -> None:
    """Constraint profile registry should expose expected strict entry."""
    contract = build_constraint_profile_registry_contract()
    entry = contract.entries[0]

    assert entry.constraint_profile_id == "constraint_strict_execution_001"
    assert entry.simulation_mode == "strict_physics"
    assert entry.production_execution_allowed is True
    assert entry.validation_gate_required is True
    assert entry.research_only is False


def test_constraint_profile_registry_contract_contains_expected_engineering_entry() -> None:
    """Constraint profile registry should expose expected engineering entry."""
    contract = build_constraint_profile_registry_contract()
    entry = contract.entries[1]

    assert entry.constraint_profile_id == "constraint_engineering_candidate_001"
    assert entry.simulation_mode == "engineering_realistic"
    assert entry.production_execution_allowed is True
    assert entry.validation_gate_required is True
    assert entry.research_only is False


def test_constraint_profile_registry_contract_contains_expected_research_entry() -> None:
    """Constraint profile registry should expose expected research entry."""
    contract = build_constraint_profile_registry_contract()
    entry = contract.entries[2]

    assert entry.constraint_profile_id == "constraint_research_exploratory_001"
    assert entry.simulation_mode == "research_relaxed"
    assert entry.production_execution_allowed is False
    assert entry.validation_gate_required is False
    assert entry.research_only is True


def test_constraint_profile_registry_contract_contains_expected_control_entry() -> None:
    """Constraint profile registry should expose expected control entry."""
    contract = build_constraint_profile_registry_contract()
    entry = contract.entries[3]

    assert entry.constraint_profile_id == "constraint_control_feedback_001"
    assert entry.simulation_mode == "control_learning"
    assert entry.production_execution_allowed is False
    assert entry.validation_gate_required is False
    assert entry.research_only is True
