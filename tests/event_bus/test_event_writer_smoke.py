from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.event_bus.event_models import build_event_record
from MAKSIMAR_CORE_LIB.event_bus.event_reader import read_event_journal
from MAKSIMAR_CORE_LIB.event_bus.event_writer import append_event_record


def test_event_writer_appends_and_reader_reads(tmp_path: Path) -> None:
    """Append-only writer should persist one event and reader should load it."""
    journal_path = tmp_path / "event_journal.jsonl"

    event = build_event_record(
        event_id="evt-001",
        event_type="runtime.started",
        source="test_suite",
        payload={"ok": True},
    )

    append_event_record(event, journal_path=journal_path)
    events = read_event_journal(journal_path=journal_path)

    assert len(events) == 1
    assert events[0].event_id == "evt-001"
    assert events[0].event_type == "runtime.started"
    assert events[0].source == "test_suite"
    assert events[0].payload["ok"] is True
