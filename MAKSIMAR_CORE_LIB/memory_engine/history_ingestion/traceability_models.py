from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class TraceabilityProjection:
    memory_id: str
    source_ref: str
    affected_files: Tuple[str, ...]
    related_flow_nodes: Tuple[str, ...]
    timeline_id: str
    traceability_ready: bool

    def __post_init__(self) -> None:
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        timeline_id = _ensure_non_empty_str(self.timeline_id, "timeline_id")

        if not self.affected_files:
            raise ValueError("affected_files must not be empty")
        if not self.related_flow_nodes:
            raise ValueError("related_flow_nodes must not be empty")
        if not self.traceability_ready:
            raise ValueError("traceability_ready must be True")

        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "timeline_id", timeline_id)
