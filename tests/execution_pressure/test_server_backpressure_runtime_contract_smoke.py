from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.backpressure import (
    build_server_backpressure_runtime_contract,
)


def test_server_backpressure_runtime_contract_builds() -> None:
    """Server-side backpressure runtime contract should build successfully."""
    contract = build_server_backpressure_runtime_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_server_backpressure_runtime_contract_contains_expected_nodes() -> None:
    """Server-side backpressure runtime contract should expose expected nodes."""
    contract = build_server_backpressure_runtime_contract()

    assert contract.entries[0].node_id == "mobile_001"
    assert contract.entries[-1].node_id == "home_001"


def test_server_backpressure_runtime_contract_keeps_normal_nodes_open() -> None:
    """Normal nodes should keep pressure action open."""
    contract = build_server_backpressure_runtime_contract()

    first = contract.entries[0]

    assert first.pressure_level == "normal"
    assert first.primary_action == "allow"
    assert first.admission_decision == "accept"
    assert first.throttling_active is False
    assert first.degraded_mode_required is False


def test_server_backpressure_runtime_contract_elevates_home_node() -> None:
    """Home node should resolve elevated pressure under current runtime profile."""
    contract = build_server_backpressure_runtime_contract()

    last = contract.entries[-1]

    assert last.node_id == "home_001"
    assert last.pressure_level == "elevated"
    assert last.admission_decision == "accept_with_throttle"
    assert last.throttling_active is True
    assert last.degraded_mode_required is False
