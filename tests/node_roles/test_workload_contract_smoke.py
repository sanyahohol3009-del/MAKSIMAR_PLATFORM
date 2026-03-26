from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_workload_placement_contract,
)


def test_workload_placement_contract_builds() -> None:
    """Workload placement contract should build successfully."""
    contract = build_workload_placement_contract()

    assert contract.total_rules == 5
    assert len(contract.rules) == 5


def test_workload_placement_contract_contains_home_node_heavy_tasks() -> None:
    """Workload placement contract should place heavy tasks on home node."""
    contract = build_workload_placement_contract()

    pairs = {(rule.workload_type, rule.allowed_node_role) for rule in contract.rules}

    assert ("heavy_inference", "home_node") in pairs
    assert ("simulation_task", "home_node") in pairs
