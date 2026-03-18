from __future__ import annotations

from MAKSIMAR_CORE_LIB.event_bus.event_models import EventRecord


def filter_events_by_type(
    events: list[EventRecord],
    event_type: str,
) -> list[EventRecord]:
    """Return events matching one event type."""
    return [event for event in events if event.event_type == event_type]


def filter_events_by_source(
    events: list[EventRecord],
    source: str,
) -> list[EventRecord]:
    """Return events matching one source."""
    return [event for event in events if event.source == source]


def get_last_event_by_type(
    events: list[EventRecord],
    event_type: str,
) -> EventRecord | None:
    """Return last event matching type or None."""
    filtered = filter_events_by_type(events, event_type)
    if not filtered:
        return None
    return filtered[-1]
