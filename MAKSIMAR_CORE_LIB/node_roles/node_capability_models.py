from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_capacity_class_models import (
    StaticCapacityClass,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import (
    CanonicalNodeId,
    CanonicalNodeType,
)


AllowedWorkloadClass = Literal[
    "ui_action",
    "chat_request",
    "automation_job",
    "simulation_task",
    "media_job",
    "evaluation_job",
]

NodeFeatureFlag = Literal[
    "supports_low_latency_io",
    "supports_background_jobs",
    "supports_gpu",
]


@dataclass(frozen=True, slots=True)
class NodeCapabilityEntry:
    """Canonical static node capability entry."""

    node_id: CanonicalNodeId
    node_type: CanonicalNodeType
    heavy_execution_allowed: bool
    security_root: bool
    static_capacity_class: StaticCapacityClass
    allowed_workload_classes: tuple[AllowedWorkloadClass, ...]
    feature_flags: tuple[NodeFeatureFlag, ...]


@dataclass(frozen=True, slots=True)
class NodeCapabilityContract:
    """Unified canonical node capability contract."""

    total_nodes: int
    nodes: tuple[NodeCapabilityEntry, ...]
