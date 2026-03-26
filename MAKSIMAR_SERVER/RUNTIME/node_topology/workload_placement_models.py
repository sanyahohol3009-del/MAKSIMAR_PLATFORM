from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


DistributedWorkloadKind = Literal[
    "ai_chat",
    "media_render",
    "simulation_task",
]

PlacementDecisionStatus = Literal[
    "selected",
    "degraded_selected",
    "unavailable",
]


@dataclass(frozen=True, slots=True)
class DistributedWorkloadPlacementEntry:
    """Distributed workload placement decision entry."""

    workload_id: str
    workload_kind: DistributedWorkloadKind
    selected_node_id: CanonicalNodeId | str
    decision_status: PlacementDecisionStatus
    reason: str
    selected_node_health_state: str
    selected_feature_availability: str


@dataclass(frozen=True, slots=True)
class DistributedWorkloadPlacementContract:
    """Unified distributed workload placement contract."""

    total_decisions: int
    decisions: tuple[DistributedWorkloadPlacementEntry, ...]
