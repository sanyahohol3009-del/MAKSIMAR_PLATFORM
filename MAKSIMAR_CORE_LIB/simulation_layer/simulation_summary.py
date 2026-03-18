from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.simulation_layer.query_models import (
    SimulationQuery,
    SimulationRetrievalItem,
)
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_models import (
    SimulationRequestDefinition,
)


@dataclass(slots=True)
class SimulationRetrievalSummary:
    """Aggregated summary for one simulation retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[SimulationRetrievalItem]


def build_simulation_summary(
    query: SimulationQuery,
    definitions: list[SimulationRequestDefinition],
) -> SimulationRetrievalSummary:
    """Build retrieval summary from loaded simulation definitions.

    Current matching model:
    - match if query text is contained in request_id
    - limit output by query.limit

    Args:
        query: Canonical simulation query.
        definitions: Loaded simulation definitions.

    Returns:
        Retrieval summary.
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.request_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        SimulationRetrievalItem(
            request_id=definition.request_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return SimulationRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
