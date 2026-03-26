from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RouteTarget = Literal[
    "ai_service",
    "voice",
    "workflow",
    "action",
    "unknown",
]


@dataclass(frozen=True, slots=True)
class RouteDecision:
    """Routing decision for incoming request."""

    target: RouteTarget
    confidence: float
    reason: str


@dataclass(frozen=True, slots=True)
class IncomingRequest:
    """Unified incoming request model."""

    query_text: str


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """Final dispatch result after routing decision."""

    target: RouteTarget
    destination: str
    dispatched: bool
    reason: str
