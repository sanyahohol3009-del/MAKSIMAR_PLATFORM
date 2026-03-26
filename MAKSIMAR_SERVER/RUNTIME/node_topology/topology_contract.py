from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_node_role_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_multi_gpu_profile_contract,
    build_node_runtime_health_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.topology_models import (
    NodeTopologyEntry,
    NodeTopologyRuntimeContract,
)


def build_node_topology_runtime_contract() -> NodeTopologyRuntimeContract:
    """Build multi-node topology runtime contract from canonical roles and live runtime state."""
    node_roles = build_node_role_contract()
    node_runtime = build_node_runtime_health_contract()
    gpu_profiles = build_multi_gpu_profile_contract()

    runtime_by_node = {entry.node_id: entry for entry in node_runtime.nodes}
    gpu_by_node = {entry.node_id: entry for entry in gpu_profiles.nodes}

    topology_entries: list[NodeTopologyEntry] = []

    for node in node_roles.nodes:
        runtime = runtime_by_node[node.node_id]
        gpu_profile = gpu_by_node[node.node_id]

        connectivity_state = "online"
        if runtime.degraded_active:
            connectivity_state = "degraded"
        elif runtime.health_score <= 0:
            connectivity_state = "offline"

        topology_entries.append(
            NodeTopologyEntry(
                node_id=node.node_id,
                node_type=node.role_type,
                connectivity_state=connectivity_state,
                heavy_execution_allowed=node.heavy_execution_allowed,
                gpu_enabled=gpu_profile.gpu_count > 0,
                queue_depth=runtime.queue_depth,
                health_score=runtime.health_score,
                topology_visible=True,
            )
        )

    online_nodes = sum(
        1 for entry in topology_entries if entry.connectivity_state == "online"
    )
    degraded_nodes = sum(
        1 for entry in topology_entries if entry.connectivity_state == "degraded"
    )
    offline_nodes = sum(
        1 for entry in topology_entries if entry.connectivity_state == "offline"
    )

    return NodeTopologyRuntimeContract(
        total_nodes=len(topology_entries),
        online_nodes=online_nodes,
        degraded_nodes=degraded_nodes,
        offline_nodes=offline_nodes,
        nodes=tuple(topology_entries),
    )
