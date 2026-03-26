from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.control_plane.orchestration_builder import (
    build_orchestration_request,
)
from MAKSIMAR_CORE_LIB.control_plane.router_models import IncomingRequest


@dataclass(frozen=True, slots=True)
class OrchestrationExecutionResult:
    """Final result of orchestration execution."""

    target: str
    destination: str
    executed: bool
    status: str
    reason: str


def execute_orchestration(
    request: IncomingRequest,
) -> OrchestrationExecutionResult:
    """Execute orchestration flow for one incoming request."""
    orchestration_request = build_orchestration_request(request)

    if not orchestration_request.dispatched:
        return OrchestrationExecutionResult(
            target=orchestration_request.target,
            destination=orchestration_request.destination,
            executed=False,
            status="blocked",
            reason=orchestration_request.routing_reason,
        )

    return OrchestrationExecutionResult(
        target=orchestration_request.target,
        destination=orchestration_request.destination,
        executed=True,
        status="executed",
        reason=orchestration_request.routing_reason,
    )
