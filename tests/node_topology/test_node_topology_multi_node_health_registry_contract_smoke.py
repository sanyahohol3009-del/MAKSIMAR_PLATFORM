from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_multi_node_health_registry_contract,
)


def test_multi_node_health_registry_contract_builds() -> None:
    """Multi-node health registry contract should build successfully."""
    contract = build_multi_node_health_registry_contract()

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.healthy_nodes >= 1
    assert contract.critical_nodes == 0


def test_multi_node_health_registry_contract_contains_expected_nodes() -> None:
    """Multi-node health registry should expose expected nodes and health states."""
    contract = build_multi_node_health_registry_contract()

    assert contract.nodes[0].node_id == "mobile_001"
    assert contract.nodes[-1].node_id == "home_001"
    assert all(entry.health_state in ("healthy", "warning", "critical") for entry in contract.nodes)
    assert all(entry.connectivity_state in ("online", "degraded", "offline") for entry in contract.nodes)
