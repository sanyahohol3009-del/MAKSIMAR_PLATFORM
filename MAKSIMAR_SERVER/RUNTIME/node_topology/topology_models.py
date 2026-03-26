from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import (
    CanonicalNodeId,
    CanonicalNodeType,
)


NodeConnectivityState = Literal[
    "online",
    "degraded",
    "offline",
]


@dataclass(frozen=True, slots=True)
class NodeTopologyEntry:
    """Server-side runtime topology entry for a node."""

    node_id: CanonicalNodeId
    node_type: CanonicalNodeType
    connectivity_state: NodeConnectivityState
    heavy_execution_allowed: bool
    gpu_enabled: bool
    queue_depth: int
    health_score: int
    topology_visible: bool


@dataclass(frozen=True, slots=True)
class NodeTopologyRuntimeContract:
    """Unified multi-node topology runtime contract."""

    total_nodes: int
    online_nodes: int
    degraded_nodes: int
    offline_nodes: int
    nodes: tuple[NodeTopologyEntry, ...]
