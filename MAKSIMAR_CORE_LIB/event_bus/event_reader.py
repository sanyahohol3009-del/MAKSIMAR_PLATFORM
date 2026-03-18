from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.event_bus.event_models import EventRecord
from MAKSIMAR_CORE_LIB.event_bus.event_paths import get_event_journal_path


def _parse_event_line(raw_line: str) -> EventRecord:
    """Parse one JSONL event line into canonical EventRecord."""
    payload: dict[str, Any] = json.loads(raw_line)

    return EventRecord(
        event_id=str(payload["event_id"]),
        event_type=str(payload["event_type"]),
        source=str(payload["source"]),
        created_at=str(payload["created_at"]),
        payload=dict(payload["payload"]),
    )


def read_event_journal(journal_path: Path | None = None) -> list[EventRecord]:
    """Read all events from append-only journal.

    Args:
        journal_path: Optional custom journal path.

    Returns:
        List of event records.
    """
    target_path = journal_path if journal_path is not None else get_event_journal_path()

    if not target_path.exists():
        return []

    events: list[EventRecord] = []
    with target_path.open("r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.strip()
            if not line:
                continue
            events.append(_parse_event_line(line))

    return events
