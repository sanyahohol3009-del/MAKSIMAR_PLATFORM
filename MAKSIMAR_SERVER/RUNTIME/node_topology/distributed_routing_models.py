from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


RouteStatus = Literal[
    "local_route",
    "remote_route",
    "degraded_route",
]


@dataclass(frozen=True, slots=True)
class DistributedLeaseRoutingEntry:
    """Distributed lease routing decision entry."""

    lease_id: str
    owner_task_id: str
    owner_worker_id: str
    selected_node_id: CanonicalNodeId
    route_status: RouteStatus
    reason: str


@dataclass(frozen=True, slots=True)
class DistributedArtifactRoutingEntry:
    """Distributed artifact routing decision entry."""

    artifact_ref: str
    artifact_type: str
    selected_node_id: CanonicalNodeId
    route_status: RouteStatus
    reason: str


@dataclass(frozen=True, slots=True)
class DistributedRoutingContract:
    """Unified distributed lease and artifact routing contract."""

    total_lease_routes: int
    total_artifact_routes: int
    lease_routes: tuple[DistributedLeaseRoutingEntry, ...]
    artifact_routes: tuple[DistributedArtifactRoutingEntry, ...]
