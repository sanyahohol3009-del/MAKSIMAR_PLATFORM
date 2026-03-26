from __future__ import annotations

from MAKSIMAR_CORE_LIB.control_plane import (
    IncomingRequest,
    classify_request,
)


def test_classifier_ai() -> None:
    r = classify_request(IncomingRequest(query_text="analyze this data"))
    assert r.target == "ai_service"


def test_classifier_voice() -> None:
    r = classify_request(IncomingRequest(query_text="speak this text"))
    assert r.target == "voice"


def test_classifier_workflow() -> None:
    r = classify_request(IncomingRequest(query_text="run workflow pipeline"))
    assert r.target == "workflow"


def test_classifier_action() -> None:
    r = classify_request(IncomingRequest(query_text="execute task"))
    assert r.target == "action"
