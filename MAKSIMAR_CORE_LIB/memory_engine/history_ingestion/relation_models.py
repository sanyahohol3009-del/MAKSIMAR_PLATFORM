from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RelationType = Literal[
    "depends_on",
    "affects",
    "replaces",
    "related_test",
    "related_artifact",
    "next_step",
]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class MemoryRelation:
    relation_id: str
    from_memory_id: str
    to_ref: str
    relation_type: RelationType
    graph_ready: bool
    timeline_ready: bool

    def __post_init__(self) -> None:
        relation_id = _ensure_non_empty_str(self.relation_id, "relation_id")
        from_memory_id = _ensure_non_empty_str(self.from_memory_id, "from_memory_id")
        to_ref = _ensure_non_empty_str(self.to_ref, "to_ref")

        if self.relation_type not in (
            "depends_on",
            "affects",
            "replaces",
            "related_test",
            "related_artifact",
            "next_step",
        ):
            raise ValueError("Unsupported relation_type")

        if not self.graph_ready:
            raise ValueError("graph_ready must be True")

        if not self.timeline_ready:
            raise ValueError("timeline_ready must be True")

        object.__setattr__(self, "relation_id", relation_id)
        object.__setattr__(self, "from_memory_id", from_memory_id)
        object.__setattr__(self, "to_ref", to_ref)
