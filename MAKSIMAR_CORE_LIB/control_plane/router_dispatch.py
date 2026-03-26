from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane.request_classifier import classify_request
from MAKSIMAR_CORE_LIB.control_plane.router_models import (
    DispatchResult,
    IncomingRequest,
    RouteDecision,
)


def _dispatch_ai_service(decision: RouteDecision) -> DispatchResult:
    """Dispatch request to AI services."""
    return DispatchResult(
        target=decision.target,
        destination="ai_services",
        dispatched=True,
        reason=decision.reason,
    )


def _dispatch_voice(decision: RouteDecision) -> DispatchResult:
    """Dispatch request to voice layer."""
    return DispatchResult(
        target=decision.target,
        destination="voice_layer",
        dispatched=True,
        reason=decision.reason,
    )


def _dispatch_workflow(decision: RouteDecision) -> DispatchResult:
    """Dispatch request to workflow engine."""
    return DispatchResult(
        target=decision.target,
        destination="workflow_engine",
        dispatched=True,
        reason=decision.reason,
    )


def _dispatch_action(decision: RouteDecision) -> DispatchResult:
    """Dispatch request to action executor."""
    return DispatchResult(
        target=decision.target,
        destination="action_executor",
        dispatched=True,
        reason=decision.reason,
    )


def _dispatch_unknown(decision: RouteDecision) -> DispatchResult:
    """Handle unknown route target."""
    return DispatchResult(
        target=decision.target,
        destination="unresolved",
        dispatched=False,
        reason=decision.reason,
    )


def dispatch_request(request: IncomingRequest) -> DispatchResult:
    """Classify and dispatch one incoming request."""
    decision = classify_request(request)

    if decision.target == "ai_service":
        return _dispatch_ai_service(decision)

    if decision.target == "voice":
        return _dispatch_voice(decision)

    if decision.target == "workflow":
        return _dispatch_workflow(decision)

    if decision.target == "action":
        return _dispatch_action(decision)

    return _dispatch_unknown(decision)
