"""Existing supervisor API command/event linkage, with synthetic persistence."""
from pathlib import Path
import pytest
from SUPERVISOR import process_supervisor as supervisor
from MAKSIMAR_CORE_LIB.event_bus import event_writer


def test_supervisor_starts_same_api_entrypoint_without_model_command(monkeypatch):
    monkeypatch.setattr(supervisor,"resolve_canonical_python",lambda:Path("/synthetic/canonical/python"))
    command=supervisor.build_command()
    assert command[:4]==["/synthetic/canonical/python","-m","uvicorn","CONTROL_PLANE.api_server:app"]
    assert "warm" not in " ".join(command) and "ollama" not in command


@pytest.mark.parametrize("kind,code",[("runtime.child.started",None),("runtime.child.exited",7),("runtime.child.stopped",0)])
def test_actual_child_event_uses_existing_typed_journal_owner(monkeypatch,kind,code):
    records=[]
    monkeypatch.setattr(event_writer,"append_event_record",records.append)
    supervisor.record_child_lifecycle(kind,child_pid=12345,exit_code=code)
    assert len(records)==1
    record=records[0]
    assert record.event_type==kind and record.source=="process_supervisor"
    assert record.payload["child_pid"]==12345 and record.payload["exit_code"]==code
    assert record.payload["supervisor_pid"]>0


def test_child_event_write_error_is_visible_without_fake_receipt(monkeypatch):
    logs=[]
    monkeypatch.setattr(supervisor,"log",logs.append)
    def unavailable(record):raise OSError("synthetic journal unavailable")
    monkeypatch.setattr(event_writer,"append_event_record",unavailable)
    supervisor.record_child_lifecycle("runtime.child.started",child_pid=12345)
    assert logs and "persistence failed" in logs[0]
