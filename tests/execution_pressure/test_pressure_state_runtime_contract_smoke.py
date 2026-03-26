from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.pressure_state import (
    build_pressure_state_runtime_contract,
)


def test_pressure_state_runtime_contract_builds() -> None:
    """Pressure state runtime contract should build successfully."""
    contract = build_pressure_state_runtime_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3
    assert contract.elevated_or_higher_entries == 1
    assert contract.degraded_active_entries == 0


def test_pressure_state_runtime_contract_contains_expected_nodes() -> None:
    """Pressure state runtime contract should expose expected nodes."""
    contract = build_pressure_state_runtime_contract()

    assert contract.entries[0].node_id == "mobile_001"
    assert contract.entries[-1].node_id == "home_001"


def test_pressure_state_runtime_contract_keeps_mobile_node_open() -> None:
    """Mobile node should remain in open pressure state."""
    contract = build_pressure_state_runtime_contract()

    first = contract.entries[0]

    assert first.pressure_level == "normal"
    assert first.runtime_state == "open"
    assert first.admission_decision == "accept"
    assert first.throttling_active is False
    assert first.degraded_mode_active is False


def test_pressure_state_runtime_contract_marks_home_node_throttled() -> None:
    """Home node should remain throttled under elevated pressure."""
    contract = build_pressure_state_runtime_contract()

    last = contract.entries[-1]

    assert last.node_id == "home_001"
    assert last.pressure_level == "elevated"
    assert last.runtime_state == "throttled"
    assert last.admission_decision == "accept_with_throttle"
    assert last.throttling_active is True
    assert last.degraded_mode_active is False
