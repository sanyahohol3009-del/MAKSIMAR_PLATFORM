from __future__ import annotations

from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_models import (
    MemoryRelation,
)


def validate_relation_set_ready(
    relations: Tuple[MemoryRelation, ...],
) -> None:
    if not relations:
        raise ValueError("relations must not be empty")

    ids = [relation.relation_id for relation in relations]
    if len(ids) != len(set(ids)):
        raise ValueError("relation_id values must be unique")

    if not all(relation.graph_ready for relation in relations):
        raise ValueError("all relations must be graph_ready")

    if not all(relation.timeline_ready for relation in relations):
        raise ValueError("all relations must be timeline_ready")
