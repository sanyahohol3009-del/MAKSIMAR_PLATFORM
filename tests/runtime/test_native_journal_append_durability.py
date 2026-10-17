from __future__ import annotations

import json
import os

import pytest


@pytest.mark.parametrize("journal_kind", ["events", "incidents"])
@pytest.mark.parametrize("fsync_fails", [False, True])
def test_native_append_flushes_before_durability_confirmation_and_preserves_prior_records(
    tmp_path, monkeypatch, journal_kind, fsync_fails,
):
    from MAKSIMAR_CORE_LIB.event_bus import event_writer
    from MAKSIMAR_CORE_LIB.event_bus.event_models import build_event_record
    from CORE_ROOT import incident_history
    path = tmp_path / "native.jsonl"
    prior = b'{"existing":"historical record retained"}\n'
    path.write_bytes(prior)
    persisted_sizes = []

    def confirm_durability(fd):
        persisted_sizes.append(os.fstat(fd).st_size)
        if fsync_fails:
            raise OSError("durability confirmation unavailable")

    monkeypatch.setattr(event_writer.os, "fsync", confirm_durability)
    if journal_kind == "events":
        event = build_event_record(event_id="test-event", event_type="runtime.child.started",
            source="isolated-test", payload={"child_pid": 42})
        append = lambda: event_writer.append_event_record(event, journal_path=path)
    else:
        monkeypatch.setattr(incident_history, "INCIDENT_HISTORY_FILE", path)
        monkeypatch.setattr(incident_history, "ensure_runtime_layout", lambda: None)
        monkeypatch.setattr(incident_history, "read_run_metadata", lambda: {})
        append = lambda: incident_history.write_incident_record("isolated test", status="recovered")
    if fsync_fails:
        with pytest.raises(OSError, match="durability confirmation unavailable"):
            append()
    else:
        append()
    current = path.read_bytes()
    assert current.startswith(prior)
    assert len(persisted_sizes) == 1 and persisted_sizes[0] == len(current) > len(prior)
    appended = json.loads(current[len(prior):])
    assert appended.get("event_id") == "test-event" if journal_kind == "events" else appended["status"] == "recovered"
