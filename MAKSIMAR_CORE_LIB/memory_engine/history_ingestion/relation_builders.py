from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_models import (
    MemoryRelation,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_validators import (
    validate_relation_set_ready,
)


def build_memory_relations(memory_object: MemoryObject) -> Tuple[MemoryRelation, ...]:
    relations = (
        MemoryRelation(
            relation_id="REL-0101",
            from_memory_id=memory_object.memory_id,
            to_ref=memory_object.next_step_id,
            relation_type="next_step",
            graph_ready=True,
            timeline_ready=True,
        ),
        MemoryRelation(
            relation_id="REL-0102",
            from_memory_id=memory_object.memory_id,
            to_ref=memory_object.affects[0],
            relation_type="affects",
            graph_ready=True,
            timeline_ready=True,
        ),
    )
    validate_relation_set_ready(relations)
    return relations


def build_relation_preview(memory_object: MemoryObject) -> Dict[str, object]:
    relations = build_memory_relations(memory_object)
    return {
        "relation_count": len(relations),
        "first_relation_type": relations[0].relation_type,
        "graph_ready": all(r.graph_ready for r in relations),
        "timeline_ready": all(r.timeline_ready for r in relations),
    }
