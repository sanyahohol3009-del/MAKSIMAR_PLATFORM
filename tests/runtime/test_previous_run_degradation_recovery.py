import os
import copy
import json
import pytest
from CORE_ROOT import stop_gate
from CORE_ROOT import incident_history, run_context
from SUPERVISOR import runtime_preflight


@pytest.fixture
def environment(monkeypatch, tmp_path):
    state = tmp_path / "RUNTIME/state"
    state.mkdir(parents=True)
    pid = tmp_path / "RUNTIME/runtime.pid"
    pid.write_text("1234")
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
    from tests.runtime.test_preflight_recovery_truth import _observation
    snapshot = _observation()
    snapshot["run_metadata"]["wall_time"] = 1.5
    monkeypatch.setattr(run_context, "RUNTIME_STATE_DIR", state)
    monkeypatch.setattr(run_context, "RUN_METADATA_FILE", state / "run_metadata.json")
    run_context.RUN_METADATA_FILE.write_text(json.dumps(snapshot["run_metadata"]))
    records = []
    monkeypatch.setattr(incident_history, "write_incident_record", lambda reason, status: records.append((reason,status)))
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: copy.deepcopy(snapshot))
    return flag, pid, trigger, reason, records


def test_verified_new_run_recovers_marker_and_preserves_incident(environment):
    flag, _, trigger, reason, records = environment
    assert runtime_preflight.recover_previous_run_degradation()
    assert not flag.exists()
    assert trigger.read_text() == "original incident evidence"
    assert reason.read_text() == "historical heartbeat timeout"
    assert records[-1][1] == "recovered"
    assert [status for _, status in records] == ["recovery_pending", "recovered"]


def test_current_run_incident_is_never_cleared(environment):
    flag, _, _, _, records = environment
    os.utime(flag, ns=(3_000_000_000, 3_000_000_000))
    assert runtime_preflight.recover_previous_run_degradation() is False
    assert flag.exists() and records == []


def test_incomplete_health_or_foreign_ownership_cannot_clear_marker(environment, monkeypatch):
    flag, _, _, _, records = environment
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: {"decision":{"healthy":False}})
    assert runtime_preflight.recover_previous_run_degradation() is False
    assert flag.exists() and records == []


@pytest.mark.parametrize("argument", ["healthy", "observation", "inspect", "callback"])
def test_public_recovery_does_not_accept_caller_authority(environment, argument):
    flag, _, _, _, records = environment
    with pytest.raises(TypeError):
        runtime_preflight.recover_previous_run_degradation(**{argument: {"healthy": True}})
    assert flag.exists() and records == []


def test_private_marker_commit_requires_actual_transition_scope(environment):
    flag, _, _, _, records = environment
    with pytest.raises(RuntimeError, match="active StopGate transition"):
        stop_gate._commit_previous_run_recovery((), ())
    assert flag.exists() and records == []


def test_fresh_complete_preflight_runs_twice_under_one_kernel_scope(environment, monkeypatch):
    import fcntl
    from tests.runtime.test_preflight_recovery_truth import _observation
    flag, _, _, _, records = environment
    seen = []
    def collect():
        with (stop_gate.RUNTIME_STATE_DIR / "stop_gate_transition.lock").open("a") as other:
            with pytest.raises(BlockingIOError):
                fcntl.flock(other.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        seen.append(stop_gate._transition_local.handle.fileno())
        raw = _observation()
        raw["run_metadata"]["wall_time"] = 1.5
        return raw
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", collect)
    assert runtime_preflight.recover_previous_run_degradation() is True
    assert len(seen) == 2 and seen[0] == seen[1]
    assert [status for _, status in records] == ["recovery_pending", "recovered"]
    assert not flag.exists()
    assert runtime_preflight.recover_previous_run_degradation() is True  # compatible no-marker path
    assert len(seen) == 2


@pytest.mark.parametrize("point", ["marker", "marker_same_mtime", "pid", "metadata"])
def test_changed_evidence_after_intent_cannot_commit(environment, monkeypatch, point):
    flag, pid, trigger, reason, records = environment
    originals = (trigger.read_bytes(), reason.read_bytes())
    def append(text, status):
        records.append((text, status))
        if status != "recovery_pending":
            return
        if point.startswith("marker"):
            timestamp = flag.stat().st_mtime_ns
            flag.write_text("concurrent incident")
            if point == "marker_same_mtime":
                os.utime(flag, ns=(timestamp, timestamp))
        elif point == "pid":
            pid.write_text("9999")
        else:
            value = json.loads(run_context.RUN_METADATA_FILE.read_text())
            value["run_id"] = "new-run"
            run_context.RUN_METADATA_FILE.write_text(json.dumps(value))
    monkeypatch.setattr(incident_history, "write_incident_record", append)
    assert runtime_preflight.recover_previous_run_degradation() is False
    assert flag.exists()
    assert all(status != "recovered" for _, status in records)
    assert (trigger.read_bytes(), reason.read_bytes()) == originals


@pytest.mark.parametrize("phase", ["intent", "unlink", "completion", "completion_after_append"])
def test_partial_failure_preserves_marker_and_does_not_claim_success(environment, monkeypatch, phase):
    flag, _, trigger, reason, records = environment
    original = (flag.read_bytes(), trigger.read_bytes(), reason.read_bytes())
    real_unlink = type(flag).unlink
    def append(text, status):
        if phase == "intent" and status == "recovery_pending":
            raise OSError("synthetic intent fsync failure")
        if phase == "completion" and status == "recovered":
            raise OSError("synthetic completion failure")
        if status == "recovery_pending":
            assert flag.exists()
        if status == "recovered":
            assert not flag.exists()
        records.append((text, status))
        if phase == "completion_after_append" and status == "recovered":
            raise OSError("synthetic completion fsync failure after append")
    def unlink(path, *a, **kw):
        if path == flag and phase == "unlink":
            raise OSError("synthetic unlink failure")
        return real_unlink(path, *a, **kw)
    monkeypatch.setattr(incident_history, "write_incident_record", append)
    monkeypatch.setattr(type(flag), "unlink", unlink)
    with pytest.raises(OSError):
        runtime_preflight.recover_previous_run_degradation()
    assert flag.exists() and (flag.read_bytes(), trigger.read_bytes(), reason.read_bytes()) == original
    if phase in {"completion", "completion_after_append"}:
        assert records[-1][1] == "recovery_failed"
    else:
        assert all(status != "recovered" for _, status in records)
    # No stale thread-local lease, even after an exception.
    with stop_gate._transition_lock():
        stop_gate._require_transition_scope()


@pytest.mark.parametrize("raw", [None, {}, {"decision": {"healthy": True}}, {"heartbeats": []}])
def test_prepared_or_malformed_snapshot_cannot_authorize(environment, monkeypatch, raw):
    flag, _, _, _, records = environment
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", lambda: raw)
    assert runtime_preflight.recover_previous_run_degradation() is False
    assert flag.exists() and records == []


@pytest.mark.parametrize("change", ["unavailable", "api_failed", "new_epoch", "new_pid_start"])
def test_second_full_inspection_cannot_reuse_initial_healthy_proof(environment, monkeypatch, change):
    from tests.runtime.test_preflight_recovery_truth import _observation
    flag, _, _, _, records = environment
    first = _observation()
    first["run_metadata"]["wall_time"] = 1.5
    second = copy.deepcopy(first)
    if change == "api_failed":
        second["health"]["ok"] = False
    elif change == "new_epoch":
        second["run_metadata"]["run_id"] = "next-run"
        for peer in second["heartbeats"].values():
            peer["run_id"] = "next-run"
        assert runtime_preflight.classify_runtime_observation(second)["healthy"] is True
    elif change == "new_pid_start":
        second["runtime_pid_identity"]["process_start_ticks"] = "999999"
        second["heartbeats"]["runtime"]["process_start_ticks"] = "999999"
        second["heartbeats"]["runtime"]["identity"]["process_start_ticks"] = "999999"
        assert runtime_preflight.classify_runtime_observation(second)["healthy"] is True
    seen = []
    def collect():
        seen.append(True)
        if len(seen) == 1:
            return first
        if change == "unavailable":
            raise OSError("synthetic second observation unavailable")
        return second
    monkeypatch.setattr(runtime_preflight, "inspect_runtime_state", collect)
    assert runtime_preflight.recover_previous_run_degradation() is False
    assert len(seen) == 2 and flag.exists()
    assert [status for _, status in records] == ["recovery_pending"]
