from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_models import (
    KnowledgeObjectDefinition,
)
from MAKSIMAR_CORE_LIB.knowledge_engine.query_models import (
    KnowledgeQuery,
    KnowledgeRetrievalItem,
)


@dataclass(slots=True)
class KnowledgeRetrievalSummary:
    """Aggregated summary for one knowledge retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[KnowledgeRetrievalItem]


def build_retrieval_summary(
    query: KnowledgeQuery,
    definitions: list[KnowledgeObjectDefinition],
) -> KnowledgeRetrievalSummary:
    """Build retrieval summary from loaded knowledge definitions.

    Current matching model:
    - match if query text is contained in object_id
    - limit output by query.limit

    Args:
        query: Canonical knowledge query.
        definitions: Loaded knowledge definitions.

    Returns:
        Retrieval summary.
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.object_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        KnowledgeRetrievalItem(
            object_id=definition.object_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return KnowledgeRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
