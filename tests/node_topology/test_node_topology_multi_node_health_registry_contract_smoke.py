from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_contract import (
    build_multi_node_health_registry_contract,
)


def test_multi_node_health_registry_contract_builds() -> None:
    """Multi-node health registry contract should build and expose consistent counts."""
    contract = build_multi_node_health_registry_contract()

    assert contract.total_nodes == len(contract.nodes)
    assert contract.total_nodes == 3

    expected_healthy = sum(1 for node in contract.nodes if node.health_state == "healthy")
    expected_warning = sum(1 for node in contract.nodes if node.health_state == "warning")
    expected_critical = sum(1 for node in contract.nodes if node.health_state == "critical")

    assert contract.healthy_nodes == expected_healthy
    assert contract.warning_nodes == expected_warning
    assert contract.critical_nodes == expected_critical
    assert (
        contract.healthy_nodes
        + contract.warning_nodes
        + contract.critical_nodes
        == contract.total_nodes
    )

    for node in contract.nodes:
        assert node.node_id
        assert node.health_state in {"healthy", "warning", "critical"}
        assert 0 <= node.health_score <= 100
        assert node.queue_depth >= 0
