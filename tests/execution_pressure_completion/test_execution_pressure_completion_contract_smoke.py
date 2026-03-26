from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure_completion import (
    build_execution_pressure_completion_contract,
)


def test_execution_pressure_completion_contract_builds() -> None:
    """Execution pressure completion contract should build successfully."""
    contract = build_execution_pressure_completion_contract()

    assert contract.total_entries == 4
    assert contract.throttled_or_higher_entries == 3
    assert contract.degraded_candidate_entries == 2
    assert contract.completed_entries == 4


def test_execution_pressure_completion_contract_contains_expected_normal_entry() -> None:
    """Execution pressure completion should expose expected normal entry."""
    contract = build_execution_pressure_completion_contract()
    entry = contract.entries[0]

    assert entry.pressure_level == "normal"
    assert entry.primary_action == "allow"
    assert entry.admission_decision == "accept"
    assert entry.runtime_state == "open"
    assert entry.throttling_required is False
    assert entry.degraded_mode_candidate is False
    assert entry.degraded_trigger_enabled is False


def test_execution_pressure_completion_contract_contains_expected_elevated_entry() -> None:
    """Execution pressure completion should expose expected elevated entry."""
    contract = build_execution_pressure_completion_contract()
    entry = contract.entries[1]

    assert entry.pressure_level == "elevated"
    assert entry.primary_action == "throttle"
    assert entry.admission_decision == "accept_with_throttle"
    assert entry.runtime_state == "throttled"
    assert entry.throttling_required is True


def test_execution_pressure_completion_contract_contains_expected_high_entry() -> None:
    """Execution pressure completion should expose expected high entry."""
    contract = build_execution_pressure_completion_contract()
    entry = contract.entries[2]

    assert entry.pressure_level == "high"
    assert entry.primary_action == "restrict"
    assert entry.admission_decision == "reject_new_work"
    assert entry.runtime_state == "restricted"
    assert entry.degraded_mode_candidate is True
    assert entry.degraded_trigger_enabled is True


def test_execution_pressure_completion_contract_contains_expected_critical_entry() -> None:
    """Execution pressure completion should expose expected critical entry."""
    contract = build_execution_pressure_completion_contract()
    entry = contract.entries[3]

    assert entry.pressure_level == "critical"
    assert entry.primary_action == "reject"
    assert entry.admission_decision == "reject"
    assert entry.runtime_state == "blocked"
    assert entry.degraded_mode_candidate is True
    assert entry.degraded_trigger_enabled is True


def test_execution_pressure_completion_contract_preserves_completion_status() -> None:
    """Execution pressure completion should preserve completed status."""
    contract = build_execution_pressure_completion_contract()

    for entry in contract.entries:
        assert entry.total_signal_kinds == 5
        assert entry.runtime_entries_observed > 0
        assert entry.completion_valid is True
        assert entry.completion_status == "completed"
