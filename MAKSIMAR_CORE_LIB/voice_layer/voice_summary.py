from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.voice_layer.query_models import (
    VoiceQuery,
    VoiceRetrievalItem,
)
from MAKSIMAR_CORE_LIB.voice_layer.voice_models import VoicePolicyDefinition


@dataclass(slots=True)
class VoiceRetrievalSummary:
    """Aggregated summary for one voice retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[VoiceRetrievalItem]


def build_voice_summary(
    query: VoiceQuery,
    definitions: list[VoicePolicyDefinition],
) -> VoiceRetrievalSummary:
    """Build retrieval summary from loaded voice definitions.

    Current matching model:
    - match if query text is contained in policy_id
    - limit output by query.limit
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.policy_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        VoiceRetrievalItem(
            policy_id=definition.policy_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return VoiceRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
