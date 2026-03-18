from __future__ import annotations

from MAKSIMAR_CORE_LIB.event_bus.event_filters import (
    filter_events_by_source,
    filter_events_by_type,
    get_last_event_by_type,
)
from MAKSIMAR_CORE_LIB.event_bus.event_models import build_event_record


def test_event_filters_and_last_event() -> None:
    """Typed event filters should return expected events."""
    events = [
        build_event_record(
            event_id="evt-001",
            event_type="runtime.started",
            source="runtime",
            payload={"n": 1},
        ),
        build_event_record(
            event_id="evt-002",
            event_type="runtime.started",
            source="runtime",
            payload={"n": 2},
        ),
        build_event_record(
            event_id="evt-003",
            event_type="workflow.triggered",
            source="workflow",
            payload={"n": 3},
        ),
    ]

    runtime_events = filter_events_by_type(events, "runtime.started")
    workflow_events = filter_events_by_source(events, "workflow")
    last_runtime = get_last_event_by_type(events, "runtime.started")

    assert len(runtime_events) == 2
    assert len(workflow_events) == 1
    assert last_runtime is not None
    assert last_runtime.event_id == "evt-002"
