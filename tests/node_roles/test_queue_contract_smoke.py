from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_queue_policy_contract,
)


def test_queue_policy_contract_builds() -> None:
    """Queue policy contract should build successfully."""
    contract = build_queue_policy_contract()

    assert contract.total_rules == 5
    assert len(contract.rules) == 5


def test_queue_policy_contract_contains_critical_queue() -> None:
    """Queue policy contract should contain critical queue rule."""
    contract = build_queue_policy_contract()

    pairs = {(rule.queue_type, rule.overflow_action) for rule in contract.rules}

    assert ("critical_queue", "reject_noncritical") in pairs
