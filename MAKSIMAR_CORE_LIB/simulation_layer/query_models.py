from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SimulationScope = Literal[
    "request",
    "result",
    "environment",
    "engine",
    "proposal",
    "evaluator",
]


@dataclass(frozen=True, slots=True)
class SimulationQuery:
    """Canonical simulation query model."""

    query_text: str
    scope: SimulationScope | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class SimulationRetrievalItem:
    """Canonical simulation retrieval item."""

    request_id: str
    version: str
