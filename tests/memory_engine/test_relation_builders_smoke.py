from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_builders import (
    build_memory_relations,
)


def test_relation_builders_smoke() -> None:
    memory_object = build_minimal_memory_object()
    relations = build_memory_relations(memory_object)

    assert len(relations) == 2
    assert relations[0].graph_ready is True
