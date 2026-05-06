from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_builders import (
    build_memory_relations,
)


def test_relation_graph_ready_smoke() -> None:
    relations = build_memory_relations(build_minimal_memory_object())
    assert all(relation.graph_ready for relation in relations)
