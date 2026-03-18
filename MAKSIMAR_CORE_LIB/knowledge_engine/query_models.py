from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


KnowledgeTrustLevel = Literal[
    "unverified",
    "reviewed",
    "trusted",
]


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    """Canonical knowledge query model."""

    query_text: str
    trust_level: KnowledgeTrustLevel | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalItem:
    """Canonical knowledge retrieval item."""

    object_id: str
    version: str
