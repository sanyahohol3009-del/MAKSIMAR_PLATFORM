from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_models import (
    KnowledgeObjectDefinition,
)
from MAKSIMAR_CORE_LIB.knowledge_engine.query_models import KnowledgeQuery
from MAKSIMAR_CORE_LIB.knowledge_engine.retrieval_summary import (
    build_retrieval_summary,
)


def test_build_retrieval_summary_matches_object_ids() -> None:
    """Retrieval summary should match by object_id substring."""
    definitions = [
        KnowledgeObjectDefinition(
            object_id="knowledge_object",
            version="knowledge_object.v1",
            file_path=Path("knowledge_object.v1.yaml"),
            payload={},
        ),
        KnowledgeObjectDefinition(
            object_id="knowledge_source",
            version="knowledge_source.v1",
            file_path=Path("knowledge_source.v1.yaml"),
            payload={},
        ),
    ]

    query = KnowledgeQuery(query_text="object", limit=10)
    summary = build_retrieval_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].object_id == "knowledge_object"


def test_build_retrieval_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        KnowledgeObjectDefinition(
            object_id="knowledge_object",
            version="knowledge_object.v1",
            file_path=Path("knowledge_object.v1.yaml"),
            payload={},
        ),
        KnowledgeObjectDefinition(
            object_id="knowledge_source",
            version="knowledge_source.v1",
            file_path=Path("knowledge_source.v1.yaml"),
            payload={},
        ),
    ]

    query = KnowledgeQuery(query_text="knowledge", limit=1)
    summary = build_retrieval_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
