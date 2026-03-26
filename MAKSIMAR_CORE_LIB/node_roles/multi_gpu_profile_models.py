from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class AcceleratorProfileEntry:
    """Canonical per-accelerator profile."""

    gpu_index: int
    gpu_vendor: str
    gpu_model: str
    accelerator_class: str
    vram_total_gb: int
    vram_free_gb: int
    shared_memory_mode: bool
    gpu_capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MultiGpuProfile:
    """Canonical multi-GPU / accelerator profile bound to a node."""

    node_id: CanonicalNodeId
    gpu_count: int
    accelerators: tuple[AcceleratorProfileEntry, ...]


@dataclass(frozen=True, slots=True)
class MultiGpuProfileContract:
    """Unified multi-GPU / accelerator profile contract."""

    total_nodes: int
    nodes: tuple[MultiGpuProfile, ...]
