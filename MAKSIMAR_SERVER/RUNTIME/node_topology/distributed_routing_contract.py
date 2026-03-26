from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    build_artifact_ownership_contract,
)
from MAKSIMAR_CORE_LIB.execution_control import (
    build_lease_runtime_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_contract import (
    build_multi_node_health_registry_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.workload_placement_contract import (
    build_distributed_workload_placement_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.distributed_routing_models import (
    DistributedArtifactRoutingEntry,
    DistributedLeaseRoutingEntry,
    DistributedRoutingContract,
)


def _select_best_storage_node() -> str:
    """Select best node for artifact-heavy routing."""
    health_registry = build_multi_node_health_registry_contract()

    eligible = [
        entry
        for entry in health_registry.nodes
        if entry.connectivity_state != "offline" and entry.health_state != "critical"
    ]

    eligible.sort(
        key=lambda entry: (
            entry.queue_depth,
            -entry.health_score,
            not entry.gpu_enabled,
            entry.node_id,
        )
    )

    return eligible[0].node_id if eligible else "home_001"


def build_distributed_routing_contract() -> DistributedRoutingContract:
    """Build distributed lease and artifact routing contract."""
    placement = build_distributed_workload_placement_contract()
    leases = build_lease_runtime_contract()
    artifacts = build_artifact_ownership_contract()

    placement_by_feature = {
        entry.workload_kind: entry.selected_node_id for entry in placement.decisions
    }

    simulation_node_id = placement_by_feature["simulation_task"]
    ai_chat_node_id = placement_by_feature["ai_chat"]
    artifact_storage_node_id = _select_best_storage_node()

    lease_routes = (
        DistributedLeaseRoutingEntry(
            lease_id=leases.leases[0].lease_id,
            owner_task_id=leases.leases[0].owner_task_id,
            owner_worker_id=leases.leases[0].owner_worker_id,
            selected_node_id=ai_chat_node_id,
            route_status="remote_route" if ai_chat_node_id != "dev_001" else "local_route",
            reason="lease_routed_by_workload_selection",
        ),
        DistributedLeaseRoutingEntry(
            lease_id=leases.leases[1].lease_id,
            owner_task_id=leases.leases[1].owner_task_id,
            owner_worker_id=leases.leases[1].owner_worker_id,
            selected_node_id=simulation_node_id,
            route_status="remote_route" if simulation_node_id != "dev_001" else "local_route",
            reason="simulation_lease_routed_to_best_node",
        ),
    )

    artifact_routes = (
        DistributedArtifactRoutingEntry(
            artifact_ref=artifacts.artifacts[0].artifact_ref,
            artifact_type="simulation_output",
            selected_node_id=simulation_node_id,
            route_status="remote_route" if simulation_node_id != "dev_001" else "local_route",
            reason="simulation_artifact_follows_execution_node",
        ),
        DistributedArtifactRoutingEntry(
            artifact_ref=artifacts.artifacts[1].artifact_ref,
            artifact_type="runtime_log_bundle",
            selected_node_id=artifact_storage_node_id,
            route_status="remote_route" if artifact_storage_node_id != "dev_001" else "local_route",
            reason="artifact_routed_to_best_storage_node",
        ),
    )

    return DistributedRoutingContract(
        total_lease_routes=len(lease_routes),
        total_artifact_routes=len(artifact_routes),
        lease_routes=lease_routes,
        artifact_routes=artifact_routes,
    )
