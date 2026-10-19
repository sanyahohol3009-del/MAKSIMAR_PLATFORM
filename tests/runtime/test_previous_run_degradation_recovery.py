import os
import pytest
from CORE_ROOT import stop_gate
from CORE_ROOT import incident_history
from SUPERVISOR import runtime_preflight


@pytest.fixture
def environment(monkeypatch, tmp_path):
    state = tmp_path / "RUNTIME/state"
    state.mkdir(parents=True)
    pid = tmp_path / "RUNTIME/runtime.pid"
    pid.write_text("123")
    flag = state / "degraded_mode.flag"
    flag.write_text("1")
    reason = state / "last_degraded_reason.txt"
    reason.write_text("historical heartbeat timeout")
    trigger = state / "stop_gate_trigger.txt"
    trigger.write_text("original incident evidence")
    os.utime(flag, ns=(1_000_000_000, 1_000_000_000))
    os.utime(pid, ns=(2_000_000_000, 2_000_000_000))
    for name, value in {"ROOT":tmp_path,"RUNTIME_STATE_DIR":state,"DEGRADED_MODE_FILE":flag,
                        "LAST_DEGRADED_REASON_FILE":reason,"STOP_GATE_TRIGGER_FILE":trigger}.items():
        monkeypatch.setattr(stop_gate, name, value)
    monkeypatch.setattr(stop_gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(stop_gate, "log", lambda text: None)
    records = []
    monkeypatch.setattr(incident_history, "write_incident_record", lambda reason, status: records.append((reason,status)))
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: {"decision":{"healthy":True}})
    return flag, pid, trigger, reason, records


def test_verified_new_run_recovers_marker_and_preserves_incident(environment):
    flag, _, trigger, reason, records = environment
    assert stop_gate.recover_previous_run_degradation()
    assert not flag.exists()
    assert trigger.read_text() == "original incident evidence"
    assert reason.read_text() == "historical heartbeat timeout"
    assert records[0][1] == "recovered"


def test_current_run_incident_is_never_cleared(environment):
    flag, _, _, _, records = environment
    os.utime(flag, ns=(3_000_000_000, 3_000_000_000))
    assert stop_gate.recover_previous_run_degradation() is False
    assert flag.exists() and records == []


def test_incomplete_health_or_foreign_ownership_cannot_clear_marker(environment, monkeypatch):
    flag, _, _, _, records = environment
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: {"decision":{"healthy":False}})
    assert stop_gate.recover_previous_run_degradation() is False
    assert flag.exists() and records == []
