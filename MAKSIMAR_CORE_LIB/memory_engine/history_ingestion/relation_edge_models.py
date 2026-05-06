from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_id_models import (
    RelationId,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class RelationEdge:
    relation_id: RelationId
    from_id: str
    to_id: str
    relation_type: str
    graph_ready: bool

    def __post_init__(self) -> None:
        from_id = _ensure_non_empty_str(self.from_id, "from_id")
        to_id = _ensure_non_empty_str(self.to_id, "to_id")
        relation_type = _ensure_non_empty_str(self.relation_type, "relation_type")

        if not self.graph_ready:
            raise ValueError("graph_ready must be True")

        object.__setattr__(self, "from_id", from_id)
        object.__setattr__(self, "to_id", to_id)
        object.__setattr__(self, "relation_type", relation_type)
