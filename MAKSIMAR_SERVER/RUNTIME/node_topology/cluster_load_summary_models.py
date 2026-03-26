from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


ClusterState = Literal[
    "stable",
    "elevated",
    "critical",
]


@dataclass(frozen=True, slots=True)
class ClusterLoadDistributionSummaryContract:
    """Unified cluster load distribution summary contract."""

    summary_id: str
    total_nodes: int
    healthy_nodes: int
    gpu_enabled_nodes: int
    total_workload_decisions: int
    total_remote_routes: int
    busiest_node_id: CanonicalNodeId
    max_queue_depth: int
    cluster_state: ClusterState
