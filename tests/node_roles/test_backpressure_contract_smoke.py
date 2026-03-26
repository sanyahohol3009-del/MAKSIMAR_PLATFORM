from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_backpressure_contract,
)


def test_backpressure_contract_builds() -> None:
    """Backpressure contract should build successfully."""
    contract = build_backpressure_contract()

    assert contract.total_rules == 3
    assert len(contract.rules) == 3


def test_backpressure_contract_blocks_heavy_requests() -> None:
    """Backpressure contract should contain heavy-request blocking rule."""
    contract = build_backpressure_contract()

    assert any(rule.heavy_requests_blocked for rule in contract.rules)
