from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MemoryLevel = Literal[
    "L0_ephemeral",
    "L1_operational",
    "L2_project",
    "L3_stable_personal",
    "L4_restricted",
]


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    """Canonical memory query model."""

    query_text: str
    level: MemoryLevel | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class MemoryRetrievalItem:
    """Canonical memory retrieval item."""

    entity_id: str
    version: str
