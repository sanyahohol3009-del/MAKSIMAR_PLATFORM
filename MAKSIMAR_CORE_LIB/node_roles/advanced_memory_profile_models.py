from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class AdvancedMemoryProfile:
    """Canonical advanced memory profile."""

    node_id: CanonicalNodeId
    ram_total_gb: int
    ram_generation: str
    ram_frequency_mhz: int
    ram_module_count: int
    ram_channels: int
    ram_layout: str
    ecc_present: bool
    registered_or_buffered: str
    slot_population: str


@dataclass(frozen=True, slots=True)
class AdvancedMemoryProfileContract:
    """Unified advanced memory profile contract."""

    total_nodes: int
    nodes: tuple[AdvancedMemoryProfile, ...]
