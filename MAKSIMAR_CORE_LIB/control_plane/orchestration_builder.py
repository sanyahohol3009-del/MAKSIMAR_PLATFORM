from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane.orchestration_models import (
    OrchestrationRequest,
)
from MAKSIMAR_CORE_LIB.control_plane.router_dispatch import dispatch_request
from MAKSIMAR_CORE_LIB.control_plane.request_classifier import classify_request
from MAKSIMAR_CORE_LIB.control_plane.router_models import IncomingRequest


def build_orchestration_request(
    request: IncomingRequest,
) -> OrchestrationRequest:
    """Build canonical orchestration request from incoming request."""
    decision = classify_request(request)
    dispatch = dispatch_request(request)

    return OrchestrationRequest(
        request_text=request.query_text,
        target=dispatch.target,
        destination=dispatch.destination,
        confidence=decision.confidence,
        dispatched=dispatch.dispatched,
        routing_reason=dispatch.reason,
    )
