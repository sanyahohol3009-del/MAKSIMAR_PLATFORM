from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class DetectedCpuSnapshot:
    """Vendor-neutral detected CPU snapshot."""

    cpu_vendor: str
    cpu_model: str
    cpu_arch: str
    cpu_cores: int
    cpu_threads: int
    cpu_features: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DetectedMemorySnapshot:
    """Vendor-neutral detected memory snapshot."""

    ram_total_gb: int
    ram_free_gb: int
    ram_pressure_percent: int
    ram_generation: str
    ram_frequency_mhz: int
    ram_module_count: int
    ram_channels: int
    ram_layout: str
    ecc_present: bool
    registered_or_buffered: str
    slot_population: str


@dataclass(frozen=True, slots=True)
class DetectedGpuSnapshot:
    """Vendor-neutral detected GPU/accelerator snapshot."""

    gpu_index: int
    gpu_vendor: str
    gpu_model: str
    accelerator_class: str
    vram_total_gb: int
    vram_free_gb: int
    shared_memory_mode: bool
    gpu_capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NodeHardwareDetectionContract:
    """Server-side detected hardware contract for a node."""

    node_id: CanonicalNodeId
    cpu: DetectedCpuSnapshot
    memory: DetectedMemorySnapshot
    gpu_count: int
    gpus: tuple[DetectedGpuSnapshot, ...]
    detection_sources: tuple[str, ...]
