from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.ai_services.query_models import (
    AIServiceQuery,
    AIServiceRetrievalItem,
)
from MAKSIMAR_CORE_LIB.ai_services.service_models import AIServiceDefinition


@dataclass(slots=True)
class AIServiceRetrievalSummary:
    """Aggregated summary for one AI service retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[AIServiceRetrievalItem]


def build_service_summary(
    query: AIServiceQuery,
    definitions: list[AIServiceDefinition],
) -> AIServiceRetrievalSummary:
    """Build retrieval summary from loaded AI service definitions.

    Current matching model:
    - match if query text is contained in service_id
    - limit output by query.limit

    Args:
        query: Canonical AI service query.
        definitions: Loaded AI service definitions.

    Returns:
        Retrieval summary.
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.service_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        AIServiceRetrievalItem(
            service_id=definition.service_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return AIServiceRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
