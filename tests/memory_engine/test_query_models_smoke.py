from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.memory_models import MemoryEntityDefinition
from MAKSIMAR_CORE_LIB.memory_engine.query_models import MemoryQuery
from MAKSIMAR_CORE_LIB.memory_engine.retrieval_summary import build_retrieval_summary


def test_build_retrieval_summary_matches_entity_ids() -> None:
    """Retrieval summary should match by entity_id substring."""
    definitions = [
        MemoryEntityDefinition(
            entity_id="memory_entity",
            version="memory_entity.v1",
            file_path=Path("memory_entity.v1.yaml"),
            payload={},
        ),
        MemoryEntityDefinition(
            entity_id="memory_relation",
            version="memory_relation.v1",
            file_path=Path("memory_relation.v1.yaml"),
            payload={},
        ),
    ]

    query = MemoryQuery(query_text="entity", limit=10)
    summary = build_retrieval_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].entity_id == "memory_entity"


def test_build_retrieval_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        MemoryEntityDefinition(
            entity_id="memory_entity",
            version="memory_entity.v1",
            file_path=Path("memory_entity.v1.yaml"),
            payload={},
        ),
        MemoryEntityDefinition(
            entity_id="memory_event",
            version="memory_event.v1",
            file_path=Path("memory_event.v1.yaml"),
            payload={},
        ),
    ]

    query = MemoryQuery(query_text="memory", limit=1)
    summary = build_retrieval_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
