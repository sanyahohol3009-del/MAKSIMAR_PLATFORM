from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class EventRecord:
    """Canonical append-only event record."""

    event_id: str
    event_type: str
    source: str
    created_at: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert event record to serializable dict."""
        return asdict(self)


def utc_now_iso() -> str:
    """Return canonical UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def build_event_record(
    *,
    event_id: str,
    event_type: str,
    source: str,
    payload: dict[str, Any],
) -> EventRecord:
    """Build canonical event record.

    Args:
        event_id: Unique event identifier.
        event_type: Logical event type.
        source: Event producer/source.
        payload: Event payload.

    Returns:
        Canonical event record.
    """
    return EventRecord(
        event_id=event_id,
        event_type=event_type,
        source=source,
        created_at=utc_now_iso(),
        payload=payload,
    )
