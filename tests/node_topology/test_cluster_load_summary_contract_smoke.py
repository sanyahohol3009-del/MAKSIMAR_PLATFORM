from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_cluster_load_distribution_summary_contract,
    build_multi_node_health_registry_contract,
)


def test_cluster_load_distribution_summary_contract_builds() -> None:
    """Cluster load distribution summary contract should build successfully."""
    contract = build_cluster_load_distribution_summary_contract()
    health_registry = build_multi_node_health_registry_contract()

    expected_gpu_enabled_nodes = sum(
        1 for entry in health_registry.nodes if entry.gpu_enabled
    )

    assert contract.summary_id == "cluster_load_distribution_summary"
    assert contract.total_nodes == 3
    assert contract.healthy_nodes == 2
    assert contract.gpu_enabled_nodes == expected_gpu_enabled_nodes
    assert contract.total_workload_decisions == 3
    assert contract.total_remote_routes == 4


def test_cluster_load_distribution_summary_contract_contains_expected_summary() -> None:
    """Cluster load distribution summary contract should expose expected summary data."""
    contract = build_cluster_load_distribution_summary_contract()

    assert contract.busiest_node_id == "home_001"
    assert contract.max_queue_depth == 4
    assert contract.cluster_state == "elevated"
