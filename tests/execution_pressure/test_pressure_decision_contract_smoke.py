from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_pressure_decision_contract,
)


def test_pressure_decision_contract_builds() -> None:
    """Pressure decision contract should build successfully."""
    contract = build_pressure_decision_contract()

    assert contract.total_rules == 4
    assert len(contract.rules) == 4


def test_pressure_decision_contract_contains_expected_actions() -> None:
    """Pressure decision contract should expose expected pressure actions."""
    contract = build_pressure_decision_contract()

    assert contract.rules[0].pressure_level == "normal"
    assert contract.rules[0].primary_action == "allow"
    assert contract.rules[2].pressure_level == "high"
    assert contract.rules[2].primary_action == "degrade"
    assert contract.rules[3].pressure_level == "critical"
    assert contract.rules[3].primary_action == "reject"


def test_pressure_decision_contract_enforces_protection_semantics() -> None:
    """Pressure decision contract should enforce degraded and admission semantics."""
    contract = build_pressure_decision_contract()

    normal = contract.rules[0]
    critical = contract.rules[3]

    assert normal.new_task_admission_allowed is True
    assert normal.degraded_mode_required is False

    assert critical.admission_decision == "reject_new_work"
    assert critical.new_task_admission_allowed is False
    assert critical.degraded_mode_required is True
    assert critical.remote_reroute_preferred is True
