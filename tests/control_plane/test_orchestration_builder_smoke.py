from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane import (
    IncomingRequest,
    build_orchestration_request,
)


def test_build_orchestration_request_for_ai() -> None:
    request = IncomingRequest(query_text="analyze this system")
    result = build_orchestration_request(request)

    assert result.target == "ai_service"
    assert result.destination == "ai_services"
    assert result.dispatched is True
    assert result.confidence > 0.0


def test_build_orchestration_request_for_unknown() -> None:
    request = IncomingRequest(query_text="random stone river")
    result = build_orchestration_request(request)

    assert result.target == "unknown"
    assert result.destination == "unresolved"
    assert result.dispatched is False
    assert result.confidence == 0.0
