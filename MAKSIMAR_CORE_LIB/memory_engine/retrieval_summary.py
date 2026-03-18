from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.memory_models import MemoryEntityDefinition
from MAKSIMAR_CORE_LIB.memory_engine.query_models import (
    MemoryQuery,
    MemoryRetrievalItem,
)


@dataclass(slots=True)
class MemoryRetrievalSummary:
    """Aggregated summary for one memory retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[MemoryRetrievalItem]


def build_retrieval_summary(
    query: MemoryQuery,
    definitions: list[MemoryEntityDefinition],
) -> MemoryRetrievalSummary:
    """Build retrieval summary from loaded memory definitions.

    Current matching model:
    - match if query text is contained in entity_id
    - limit output by query.limit

    Args:
        query: Canonical memory query.
        definitions: Loaded memory definitions.

    Returns:
        Retrieval summary.
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.entity_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        MemoryRetrievalItem(
            entity_id=definition.entity_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return MemoryRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
