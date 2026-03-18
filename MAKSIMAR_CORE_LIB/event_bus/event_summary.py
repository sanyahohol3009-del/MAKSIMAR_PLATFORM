from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.event_bus.event_models import EventRecord


@dataclass(slots=True)
class EventSummary:
    """Aggregated summary for event journal."""

    total_events: int = 0
    by_type: dict[str, int] = field(default_factory=dict)
    by_source: dict[str, int] = field(default_factory=dict)

    def register_event(self, event: EventRecord) -> None:
        """Register one event in summary."""
        self.total_events += 1
        self.by_type[event.event_type] = self.by_type.get(event.event_type, 0) + 1
        self.by_source[event.source] = self.by_source.get(event.source, 0) + 1


def build_event_summary(events: list[EventRecord]) -> EventSummary:
    """Build summary from event records.

    Args:
        events: Event records.

    Returns:
        Aggregated event summary.
    """
    summary = EventSummary()
    for event in events:
        summary.register_event(event)
    return summary
