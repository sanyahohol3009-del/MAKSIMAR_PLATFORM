from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_task_priority_contract,
)


def test_task_priority_contract_builds() -> None:
    """Task priority contract should build successfully."""
    contract = build_task_priority_contract()

    assert contract.total_rules == 5
    assert len(contract.rules) == 5


def test_task_priority_contract_contains_critical_rule() -> None:
    """Task priority contract should contain critical safety rule."""
    contract = build_task_priority_contract()

    pairs = {(rule.task_type, rule.priority) for rule in contract.rules}

    assert ("safety_check", "critical") in pairs
