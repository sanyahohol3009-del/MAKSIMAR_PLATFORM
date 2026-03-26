from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


NodeHealthState = Literal[
    "healthy",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class MultiNodeHealthEntry:
    """Multi-node live health registry entry."""

    node_id: CanonicalNodeId
    connectivity_state: str
    health_state: NodeHealthState
    cpu_pressure_percent: int
    ram_pressure_percent: int
    gpu_enabled: bool
    vram_pressure_percent: int
    queue_depth: int
    health_score: int
    degraded_active: bool


@dataclass(frozen=True, slots=True)
class MultiNodeHealthRegistryContract:
    """Unified multi-node health registry contract."""

    total_nodes: int
    healthy_nodes: int
    warning_nodes: int
    critical_nodes: int
    nodes: tuple[MultiNodeHealthEntry, ...]
