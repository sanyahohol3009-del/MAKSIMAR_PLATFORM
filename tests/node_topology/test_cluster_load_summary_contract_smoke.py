from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology.cluster_load_summary_contract import (
    build_cluster_load_distribution_summary_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_contract import (
    build_multi_node_health_registry_contract,
)


def test_cluster_load_distribution_summary_contract_builds() -> None:
    """Cluster load summary should reflect the current health registry, not stale counts."""
    contract = build_cluster_load_distribution_summary_contract()
    health_registry = build_multi_node_health_registry_contract()

    expected_gpu_enabled_nodes = sum(
        1 for entry in health_registry.nodes if entry.gpu_enabled
    )
    expected_busiest_node = max(
        health_registry.nodes,
        key=lambda entry: entry.queue_depth,
    )

    assert contract.summary_id == "cluster_load_distribution_summary"
    assert contract.total_nodes == health_registry.total_nodes
    assert contract.healthy_nodes == health_registry.healthy_nodes
    assert contract.gpu_enabled_nodes == expected_gpu_enabled_nodes
    assert contract.busiest_node_id == expected_busiest_node.node_id
    assert contract.max_queue_depth == expected_busiest_node.queue_depth
    assert contract.total_workload_decisions >= contract.total_nodes
    assert contract.total_remote_routes >= 0
    assert contract.cluster_state in {"healthy", "elevated", "warning", "critical"}

    if health_registry.healthy_nodes == 0:
        assert contract.cluster_state in {"elevated", "warning", "critical"}
