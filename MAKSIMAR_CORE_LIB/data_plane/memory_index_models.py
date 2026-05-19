from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryIndexReference:
    memory_index_id: str
    domain_id: str
    source_ref: str
    evidence_ref: str
    object_ref: str
    vector_ref: str
    producer_layer_id: str
    trace_id: str
    dashboard_safe: bool = True
    inline_memory_payload_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("memory_index_id", self.memory_index_id),
            ("domain_id", self.domain_id),
            ("source_ref", self.source_ref),
            ("evidence_ref", self.evidence_ref),
            ("object_ref", self.object_ref),
            ("vector_ref", self.vector_ref),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.inline_memory_payload_allowed:
            raise ValueError("inline_memory_payload_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MemoryIndexReadinessReadModel:
    memory_index_id: str
    domain_id: str
    object_ref: str
    vector_ref: str
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("memory_index_id", self.memory_index_id),
            ("domain_id", self.domain_id),
            ("object_ref", self.object_ref),
            ("vector_ref", self.vector_ref),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
