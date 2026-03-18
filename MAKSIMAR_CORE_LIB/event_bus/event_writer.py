from __future__ import annotations

import json
from pathlib import Path

from MAKSIMAR_CORE_LIB.event_bus.event_models import EventRecord
from MAKSIMAR_CORE_LIB.event_bus.event_paths import get_event_journal_path


def append_event_record(event: EventRecord, journal_path: Path | None = None) -> Path:
    """Append one event record to append-only journal.

    Args:
        event: Event record to append.
        journal_path: Optional custom journal path.

    Returns:
        Path to journal file.
    """
    target_path = journal_path if journal_path is not None else get_event_journal_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=False) + "\n"

    with target_path.open("a", encoding="utf-8") as file_handle:
        file_handle.write(line)
        file_handle.flush()

    return target_path
