from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane import (
    IncomingRequest,
    dispatch_request,
)


def test_dispatch_ai_service() -> None:
    result = dispatch_request(IncomingRequest(query_text="analyze this"))
    assert result.target == "ai_service"
    assert result.destination == "ai_services"
    assert result.dispatched is True


def test_dispatch_voice() -> None:
    result = dispatch_request(IncomingRequest(query_text="speak this"))
    assert result.target == "voice"
    assert result.destination == "voice_layer"
    assert result.dispatched is True


def test_dispatch_workflow() -> None:
    result = dispatch_request(IncomingRequest(query_text="workflow pipeline"))
    assert result.target == "workflow"
    assert result.destination == "workflow_engine"
    assert result.dispatched is True


def test_dispatch_action() -> None:
    result = dispatch_request(IncomingRequest(query_text="execute task"))
    assert result.target == "action"
    assert result.destination == "action_executor"
    assert result.dispatched is True


def test_dispatch_unknown() -> None:
    result = dispatch_request(IncomingRequest(query_text="table mountain blue"))
    assert result.target == "unknown"
    assert result.destination == "unresolved"
    assert result.dispatched is False
