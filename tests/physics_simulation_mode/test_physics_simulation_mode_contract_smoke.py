from __future__ import annotations

from MAKSIMAR_CORE_LIB.physics_simulation_mode import (
    build_physics_simulation_mode_contract,
)


def test_physics_simulation_mode_contract_builds() -> None:
    """Physics simulation mode contract should build successfully."""
    contract = build_physics_simulation_mode_contract()

    assert contract.total_entries == 4
    assert contract.production_path_entries == 2
    assert contract.research_path_entries == 2
    assert contract.execution_allowed_entries == 1
    assert contract.defined_entries == 4


def test_physics_simulation_mode_contract_contains_expected_strict_entry() -> None:
    """Physics simulation mode contract should expose expected strict entry."""
    contract = build_physics_simulation_mode_contract()
    entry = contract.entries[0]

    assert entry.simulation_mode == "strict_physics"
    assert entry.truth_class == "strict_engineering_truth"
    assert entry.execution_eligibility == "allowed_for_execution"
    assert entry.strict_validation_required is True
    assert entry.documentation_level == "full_trace_required"
    assert entry.production_path_allowed is True
    assert entry.research_path_allowed is False


def test_physics_simulation_mode_contract_contains_expected_engineering_entry() -> None:
    """Physics simulation mode contract should expose expected engineering entry."""
    contract = build_physics_simulation_mode_contract()
    entry = contract.entries[1]

    assert entry.simulation_mode == "engineering_realistic"
    assert entry.truth_class == "engineering_candidate"
    assert entry.execution_eligibility == "requires_validation_gate"
    assert entry.strict_validation_required is True
    assert entry.documentation_level == "engineering_summary_required"
    assert entry.production_path_allowed is True
    assert entry.research_path_allowed is False


def test_physics_simulation_mode_contract_contains_expected_research_entry() -> None:
    """Physics simulation mode contract should expose expected research entry."""
    contract = build_physics_simulation_mode_contract()
    entry = contract.entries[2]

    assert entry.simulation_mode == "research_relaxed"
    assert entry.truth_class == "research_only"
    assert entry.execution_eligibility == "forbidden_for_execution"
    assert entry.strict_validation_required is False
    assert entry.documentation_level == "research_trace_required"
    assert entry.production_path_allowed is False
    assert entry.research_path_allowed is True


def test_physics_simulation_mode_contract_contains_expected_control_learning_entry() -> None:
    """Physics simulation mode contract should expose expected control-learning entry."""
    contract = build_physics_simulation_mode_contract()
    entry = contract.entries[3]

    assert entry.simulation_mode == "control_learning"
    assert entry.truth_class == "control_feedback_only"
    assert entry.execution_eligibility == "forbidden_for_execution"
    assert entry.strict_validation_required is False
    assert entry.documentation_level == "control_feedback_trace_required"
    assert entry.production_path_allowed is False
    assert entry.research_path_allowed is True
