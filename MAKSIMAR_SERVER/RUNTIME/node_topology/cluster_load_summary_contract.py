from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology.cluster_load_summary_models import (
    ClusterLoadDistributionSummaryContract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.distributed_routing_contract import (
    build_distributed_routing_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_contract import (
    build_multi_node_health_registry_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.workload_placement_contract import (
    build_distributed_workload_placement_contract,
)


def build_cluster_load_distribution_summary_contract() -> (
    ClusterLoadDistributionSummaryContract
):
    """Build cluster load distribution summary from runtime topology data."""
    health_registry = build_multi_node_health_registry_contract()
    workload_placement = build_distributed_workload_placement_contract()
    routing = build_distributed_routing_contract()

    busiest_node = max(
        health_registry.nodes,
        key=lambda entry: (entry.queue_depth, -entry.health_score, entry.node_id),
    )

    gpu_enabled_nodes = sum(1 for entry in health_registry.nodes if entry.gpu_enabled)

    total_remote_routes = sum(
        1 for route in routing.lease_routes if route.route_status == "remote_route"
    ) + sum(
        1 for route in routing.artifact_routes if route.route_status == "remote_route"
    )

    if health_registry.critical_nodes > 0:
        cluster_state = "critical"
    elif health_registry.warning_nodes > 0:
        cluster_state = "elevated"
    else:
        cluster_state = "stable"

    return ClusterLoadDistributionSummaryContract(
        summary_id="cluster_load_distribution_summary",
        total_nodes=health_registry.total_nodes,
        healthy_nodes=health_registry.healthy_nodes,
        gpu_enabled_nodes=gpu_enabled_nodes,
        total_workload_decisions=workload_placement.total_decisions,
        total_remote_routes=total_remote_routes,
        busiest_node_id=busiest_node.node_id,
        max_queue_depth=busiest_node.queue_depth,
        cluster_state=cluster_state,
    )
