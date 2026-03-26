from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.control_plane.router_models import RouteTarget


@dataclass(frozen=True, slots=True)
class OrchestrationRequest:
    """Canonical orchestration request built after routing."""

    request_text: str
    target: RouteTarget
    destination: str
    confidence: float
    dispatched: bool
    routing_reason: str
