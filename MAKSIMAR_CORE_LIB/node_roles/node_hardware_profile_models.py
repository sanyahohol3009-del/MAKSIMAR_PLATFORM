from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import (
    CanonicalNodeId,
)


@dataclass(frozen=True, slots=True)
class CpuHardwareProfile:
    """Vendor-neutral CPU hardware profile."""

    cpu_vendor: str
    cpu_model: str
    cpu_arch: str
    cpu_cores: int
    cpu_threads: int
    cpu_features: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GpuHardwareProfile:
    """Vendor-neutral GPU/accelerator hardware profile."""

    gpu_present: bool
    gpu_vendor: str
    gpu_model: str
    accelerator_class: str
    vram_total_gb: int
    gpu_capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MemoryHardwareProfile:
    """Vendor-neutral RAM hardware profile."""

    ram_total_gb: int
    ram_generation: str
    ram_frequency_mhz: int


@dataclass(frozen=True, slots=True)
class NodeHardwareProfile:
    """Canonical hardware profile bound to a node."""

    node_id: CanonicalNodeId
    cpu_profile: CpuHardwareProfile
    gpu_profile: GpuHardwareProfile
    memory_profile: MemoryHardwareProfile


@dataclass(frozen=True, slots=True)
class NodeHardwareProfileContract:
    """Unified canonical node hardware profile contract."""

    total_nodes: int
    nodes: tuple[NodeHardwareProfile, ...]
