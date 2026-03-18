from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AIServiceRole = Literal[
    "code_generation",
    "reasoning_planning",
    "vision_analysis",
]


@dataclass(frozen=True, slots=True)
class AIServiceQuery:
    """Canonical AI service query model."""

    query_text: str
    role: AIServiceRole | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class AIServiceRetrievalItem:
    """Canonical AI service retrieval item."""

    service_id: str
    version: str
