from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane import (
    IncomingRequest,
    execute_orchestration,
)


def test_execute_orchestration_for_ai() -> None:
    result = execute_orchestration(
        IncomingRequest(query_text="analyze this system")
    )

    assert result.target == "ai_service"
    assert result.destination == "ai_services"
    assert result.executed is True
    assert result.status == "executed"


def test_execute_orchestration_for_unknown() -> None:
    result = execute_orchestration(
        IncomingRequest(query_text="random stone river")
    )

    assert result.target == "unknown"
    assert result.destination == "unresolved"
    assert result.executed is False
    assert result.status == "blocked"
