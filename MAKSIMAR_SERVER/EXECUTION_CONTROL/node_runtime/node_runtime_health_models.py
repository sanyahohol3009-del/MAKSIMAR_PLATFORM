from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import (
    CanonicalNodeId,
)


ThermalState = Literal[
    "normal",
    "elevated",
    "critical",
]


@dataclass(frozen=True, slots=True)
class NodeRuntimeHealthEntry:
    """Server-side live node runtime health entry."""

    node_id: CanonicalNodeId

    cpu_vendor: str
    cpu_model: str
    cpu_arch: str
    cpu_cores: int
    cpu_threads: int
    cpu_pressure_percent: int

    ram_total_gb: int
    ram_free_gb: int
    ram_pressure_percent: int
    ram_generation: str
    ram_frequency_mhz: int

    gpu_present: bool
    gpu_vendor: str
    gpu_model: str
    accelerator_class: str
    vram_total_gb: int
    vram_free_gb: int
    vram_pressure_percent: int

    thermal_state: ThermalState
    queue_depth: int
    worker_capacity_available: int
    health_score: int
    degraded_active: bool


@dataclass(frozen=True, slots=True)
class NodeRuntimeHealthContract:
    """Unified server-side node runtime health contract."""

    total_nodes: int
    nodes: tuple[NodeRuntimeHealthEntry, ...]
