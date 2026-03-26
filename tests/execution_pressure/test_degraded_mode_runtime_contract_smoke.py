from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.degraded_mode import (
    build_degraded_mode_runtime_contract,
)


def test_degraded_mode_runtime_contract_builds() -> None:
    """Degraded mode runtime contract should build successfully."""
    contract = build_degraded_mode_runtime_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3
    assert contract.active_entries == 0


def test_degraded_mode_runtime_contract_contains_expected_nodes() -> None:
    """Degraded mode runtime contract should expose expected nodes."""
    contract = build_degraded_mode_runtime_contract()

    assert contract.entries[0].node_id == "mobile_001"
    assert contract.entries[-1].node_id == "home_001"


def test_degraded_mode_runtime_contract_keeps_current_nodes_inactive() -> None:
    """Current runtime profile should keep degraded mode inactive."""
    contract = build_degraded_mode_runtime_contract()

    first = contract.entries[0]
    last = contract.entries[-1]

    assert first.pressure_level == "normal"
    assert first.degraded_mode_active is False
    assert first.trigger_scope == "none"
    assert first.routing_policy == "no_reroute"

    assert last.pressure_level == "elevated"
    assert last.degraded_mode_active is False
    assert last.trigger_scope == "none"
    assert last.routing_policy == "no_reroute"
