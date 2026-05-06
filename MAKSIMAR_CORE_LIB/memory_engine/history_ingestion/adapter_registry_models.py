from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.adapter_base import (
    ArchiveAdapterCapability,
    ArchiveAdapterProtocolContract,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.source_type_models import (
    SUPPORTED_ARCHIVE_SOURCE_TYPES,
    ArchiveSourceType,
)


def _ensure_unique_adapter_ids(
    capabilities: Tuple[ArchiveAdapterCapability, ...],
) -> None:
    adapter_ids = [cap.adapter_id for cap in capabilities]
    if len(adapter_ids) != len(set(adapter_ids)):
        raise ValueError("adapter_id values must be unique")


def _ensure_supported_source_matrix(
    capabilities: Tuple[ArchiveAdapterCapability, ...],
) -> None:
    seen_source_types = {cap.source_type for cap in capabilities}
    missing = set(SUPPORTED_ARCHIVE_SOURCE_TYPES) - seen_source_types
    if missing:
        raise ValueError(
            f"Adapter registry missing source_type support for: {tuple(sorted(missing))}",
        )


@dataclass(frozen=True)
class AdapterRegistry:
    capabilities: Tuple[ArchiveAdapterCapability, ...]
    protocols: Tuple[ArchiveAdapterProtocolContract, ...]

    def __post_init__(self) -> None:
        if not self.capabilities:
            raise ValueError("capabilities must not be empty")

        if not self.protocols:
            raise ValueError("protocols must not be empty")

        _ensure_unique_adapter_ids(self.capabilities)
        _ensure_supported_source_matrix(self.capabilities)

        capability_source_types = {cap.source_type for cap in self.capabilities}
        protocol_source_types = {protocol.supported_source_type for protocol in self.protocols}

        if capability_source_types != protocol_source_types:
            raise ValueError(
                "capability and protocol source_type sets must match exactly",
            )

    def get_capability_for_source_type(
        self,
        source_type: ArchiveSourceType,
    ) -> ArchiveAdapterCapability:
        for capability in self.capabilities:
            if capability.source_type == source_type:
                return capability
        raise KeyError(f"No capability registered for source_type={source_type}")

    def get_protocol_for_source_type(
        self,
        source_type: ArchiveSourceType,
    ) -> ArchiveAdapterProtocolContract:
        for protocol in self.protocols:
            if protocol.supported_source_type == source_type:
                return protocol
        raise KeyError(f"No protocol registered for source_type={source_type}")

    @property
    def supported_source_type_matrix(self) -> Tuple[ArchiveSourceType, ...]:
        return tuple(cap.source_type for cap in self.capabilities)

    @property
    def parallel_safe_registry(self) -> bool:
        return all(cap.parallel_safe_by_design for cap in self.capabilities)

    @property
    def deterministic_registry(self) -> bool:
        return all(cap.deterministic_output_required for cap in self.capabilities)

    def as_index(self) -> Dict[ArchiveSourceType, str]:
        return {cap.source_type: cap.adapter_id for cap in self.capabilities}
