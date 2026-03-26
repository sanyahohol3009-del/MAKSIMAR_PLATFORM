from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.node_runtime_health_contract import (
    build_node_runtime_health_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.node_runtime_summary_models import (
    NodeRuntimeSummaryContract,
)


def build_node_runtime_summary_contract() -> NodeRuntimeSummaryContract:
    """Build server-side read-only node runtime summary contract."""
    runtime = build_node_runtime_health_contract()

    gpu_enabled_nodes = sum(1 for node in runtime.nodes if node.gpu_present)
    degraded_nodes = sum(1 for node in runtime.nodes if node.degraded_active)
    max_queue_depth = max(node.queue_depth for node in runtime.nodes)
    min_health_score = min(node.health_score for node in runtime.nodes)

    return NodeRuntimeSummaryContract(
        summary_id="node_runtime_summary",
        total_nodes=runtime.total_nodes,
        gpu_enabled_nodes=gpu_enabled_nodes,
        degraded_nodes=degraded_nodes,
        max_queue_depth=max_queue_depth,
        min_health_score=min_health_score,
    )
