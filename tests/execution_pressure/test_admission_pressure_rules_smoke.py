from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_admission_pressure_rules_contract,
)


def test_admission_pressure_rules_contract_builds() -> None:
    """Admission pressure rules contract should build successfully."""
    contract = build_admission_pressure_rules_contract()

    assert contract.total_rules == 4
    assert len(contract.rules) == 4


def test_admission_pressure_rules_contract_contains_expected_levels() -> None:
    """Admission pressure rules contract should expose expected pressure levels."""
    contract = build_admission_pressure_rules_contract()

    assert contract.rules[0].pressure_level == "normal"
    assert contract.rules[1].pressure_level == "elevated"
    assert contract.rules[2].pressure_level == "high"
    assert contract.rules[3].pressure_level == "critical"


def test_admission_pressure_rules_contract_enforces_high_and_critical_protection() -> None:
    """High and critical pressure should enforce stronger admission protection."""
    contract = build_admission_pressure_rules_contract()

    high = contract.rules[2]
    critical = contract.rules[3]

    assert high.admission_decision == "delay_new_work"
    assert high.throttling_required is True
    assert high.delay_required is True
    assert high.rejection_required is False
    assert high.degraded_mode_required is True

    assert critical.admission_decision == "reject_new_work"
    assert critical.new_task_admission_allowed is False
    assert critical.rejection_required is True
    assert critical.remote_reroute_preferred is True


def test_admission_pressure_rules_contract_keeps_normal_flow_open() -> None:
    """Normal pressure should keep task admission fully open."""
    contract = build_admission_pressure_rules_contract()

    normal = contract.rules[0]
    elevated = contract.rules[1]

    assert normal.admission_decision == "accept"
    assert normal.new_task_admission_allowed is True
    assert normal.throttling_required is False
    assert normal.degraded_mode_required is False

    assert elevated.admission_decision == "accept_with_throttle"
    assert elevated.new_task_admission_allowed is True
    assert elevated.throttling_required is True
