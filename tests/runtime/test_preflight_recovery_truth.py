"""Offline recovery truth: actual classifier, proc collector and StopGate consumer."""
from __future__ import annotations

import copy
import json
import os
from types import SimpleNamespace

import pytest

from CORE_ROOT import heartbeat_io, incident_history, stop_gate
from SUPERVISOR import runtime_preflight as preflight
from pathlib import Path

ROOT = Path(preflight.__file__).resolve().parents[1]


def _observation(*, healthy: bool = True):
    def identity(pid, module):
        argv = ["python", "-m", module]
        if module == "uvicorn":
            argv.append("CONTROL_PLANE.api_server:app")
        return {"pid": pid, "alive": True, "process_verified": True, "matches": True, "argv": argv,
                "cwd": str(ROOT), "process_start_ticks": str(pid + 100)}

    peers = {
        "runtime": (1234, "process_supervisor", "SUPERVISOR.process_supervisor"),
        "guard": (1235, "stop_gate_watcher", "CORE_ROOT.stop_gate_watcher"),
        "core_guard": (1236, "core_guard", "CORE_ROOT.core_guard"),
        "kernel_guard": (1237, "kernel_watchdog", "CORE_ROOT.kernel_watchdog"),
    }
    return {
        "observed_wall_time": 1000.0, "observed_monotonic_time": 500.0,
        "run_metadata": {"schema_version": 1, "run_id": "current-project-run",
                         "boot_id": "project-lifecycle-not-os-boot", "status": "running",
                         "wall_time": 900.0, "monotonic_time": 400.0},
        "tmux": {"available": True, "sessions": sorted(preflight.EXPECTED_SESSIONS) if healthy else []},
        "pid_file_exists": healthy, "runtime_pid": 1234 if healthy else None,
        "runtime_pid_identity": identity(1234, "SUPERVISOR.process_supervisor") if healthy
                                else {"alive": False, "matches": False},
        "heartbeats": {scope: {
            "exists": healthy, "fresh": healthy, "age_seconds": 1.0, "error": "",
            "schema_version": 1, "status": "alive", "source": source,
            "ts": 999.0, "monotonic_ts": 499.0, "pid": pid,
            "process_start_ticks": str(pid + 100), "process_verified": True,
            "run_id": "current-project-run", "boot_id": "project-lifecycle-not-os-boot",
            "run_monotonic_time": 400.0, "identity": identity(pid, module),
        } for scope, (pid, source, module) in peers.items()},
        "port": {"listening": healthy, "owner_pids": [2345] if healthy else [],
                 "owner_identities": [identity(2345, "uvicorn")] if healthy else [],
                 "owned_by_project": healthy},
        "health": {"ok": healthy, "status": 200 if healthy else None},
    }



# Each mutation changes one necessary fact while retaining all other evidence.
BAD_CASES = [
    (("heartbeats", "guard", "status"), value)
    for value in ("stopped", "booting", "broken", "degraded", "recovery_pending", None)
] + [
    (("heartbeats", "guard", "source"), "foreign_owner"),
    (("heartbeats", "guard", "source"), " stop_gate_watcher "),
    (("heartbeats", "guard"), None),
    (("heartbeats", "extra"), {}),
    (("heartbeats", "guard", "run_id"), "previous-run"),
    (("heartbeats", "guard", "boot_id"), "linux-os-boot-not-project-boot"),
    (("heartbeats", "guard", "run_monotonic_time"), 399.0),
    (("heartbeats", "guard", "process_verified"), False),
    (("heartbeats", "guard", "pid"), 1234),
    (("heartbeats", "guard", "pid"), True),
    (("heartbeats", "guard", "process_start_ticks"), None),
    (("heartbeats", "guard", "process_start_ticks"), "reused"),
    (("heartbeats", "guard", "identity", "alive"), False),
    (("heartbeats", "guard", "identity", "process_start_ticks"), "999"),
    (("heartbeats", "guard", "identity", "argv"), ["python", "writer.py", "CORE_ROOT.stop_gate_watcher"]),
    (("heartbeats", "guard", "identity", "cwd"), "/another-project"),
    (("heartbeats", "guard", "identity"), {}),
    (("heartbeats", "guard", "error"), "corrupt"),
    (("heartbeats", "guard", "schema_version"), True),
    (("heartbeats", "guard", "fresh"), 1),
    (("heartbeats", "guard", "exists"), False),
    (("run_metadata", "run_id"), "different-run"),
    (("run_metadata", "boot_id"), "different-project-boot"),
    (("run_metadata", "status"), "booting"),
    (("run_metadata", "status"), "degraded"),
    (("run_metadata", "schema_version"), True),
    (("run_metadata",), None),
    (("runtime_pid",), 1235),
    (("runtime_pid_identity", "process_start_ticks"), "999"),
    (("runtime_pid_identity", "matches"), False),
    (("tmux", "available"), False),
    (("tmux", "sessions"), []),
    (("tmux", "sessions"), [None]),
    (("tmux", "error"), "observation failed"),
    (("port", "owner_pids"), [2345, 9999]),
    (("port", "owner_pids"), []),
    (("port", "owner_identities"), []),
    (("port", "owner_identities", 0, "argv"), ["python", "-m", "uvicorn", "foreign:app"]),
    (("port", "listening"), False),
    (("port", "owned_by_project"), False),
    (("port", "error"), "ss failed"),
    (("health", "ok"), False),
    (("health", "ok"), "true"),
    (("health", "status"), 500),
    (("health", "error"), "ambiguous"),
] + [
    (("heartbeats", "guard", key), value)
    for key, values in (
        ("ts", (980.0, 1001.0, float("nan"), float("inf"), True, "999", None, 10**400)),
        ("monotonic_ts", (480.0, 501.0, float("nan"), float("inf"), True, None)),
    ) for value in values
]


def mutated(path, value):
    observation = _observation()
    target = observation
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return observation


@pytest.mark.parametrize("path,value", BAD_CASES)
def test_incomplete_contradictory_or_foreign_chain_cannot_recover(monkeypatch, tmp_path, path, value):
    observation = mutated(path, value)
    before = copy.deepcopy(observation)
    decision = preflight.classify_runtime_observation(observation)
    assert decision["healthy"] is False
    assert decision["clean"] is False
    assert decision["reasons"]
    # Use the actual classifier verdict, not a fabricated healthy boolean.
    state = tmp_path / "RUNTIME/state"
    state.mkdir(parents=True)
    pid = tmp_path / "RUNTIME/runtime.pid"
    pid.write_text("1234")
    flag, reason, trigger = [state / name for name in ("degraded.flag", "reason", "trigger")]
    for artifact in (flag, reason, trigger):
        artifact.write_text("retain original " + artifact.name)
    os.utime(flag, ns=(1_000_000_000, 1_000_000_000))
    os.utime(pid, ns=(2_000_000_000, 2_000_000_000))
    originals = {f: f.read_bytes() for f in (flag, reason, trigger)}
    for name, value in {"ROOT": tmp_path, "RUNTIME_STATE_DIR": state,
            "DEGRADED_MODE_FILE": flag, "LAST_DEGRADED_REASON_FILE": reason,
            "STOP_GATE_TRIGGER_FILE": trigger}.items():
        monkeypatch.setattr(stop_gate, name, value)
    monkeypatch.setattr(stop_gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(stop_gate, "log", lambda _: pytest.fail("false recovery log"))
    monkeypatch.setattr(preflight, "inspect_runtime_state", lambda: {"decision": decision})
    monkeypatch.setattr(incident_history, "write_incident_record", lambda *a, **k: pytest.fail("false recovered incident"))
    assert stop_gate.recover_previous_run_degradation() is False
    assert all(f.read_bytes() == data for f, data in originals.items())
    # NaN is not equal to itself; structural input immutability is checked by bytes.
    assert json.dumps(observation, sort_keys=True) == json.dumps(before, sort_keys=True)


def test_missing_peer_and_duplicate_peer_alias_fail_closed():
    for replace in (False, True):
        observation = _observation()
        peer = observation["heartbeats"].pop("guard")
        if replace:
            observation["heartbeats"]["guard_duplicate"] = peer
        assert preflight.classify_runtime_observation(observation)["healthy"] is False


@pytest.mark.parametrize("value", [None, [], {}, {"tmux": None}])
def test_malformed_observation_is_neither_clean_nor_healthy(value):
    result = preflight.classify_runtime_observation(value)
    assert result["healthy"] is False and result["clean"] is False


def test_complete_current_run_and_original_false_positive_cases():
    original = _observation()
    assert preflight.classify_runtime_observation(original)["healthy"] is True
    for key, value in (("status", "stopped"), ("source", "foreign_owner")):
        broken = copy.deepcopy(original)
        broken["heartbeats"]["guard"][key] = value
        assert preflight.classify_runtime_observation(broken)["healthy"] is False


def test_clean_start_does_not_require_live_run_metadata():
    observation = _observation(healthy=False)
    observation.pop("run_metadata")
    assert preflight.classify_runtime_observation(observation)["classification"] == "clean_start"


@pytest.fixture
def synthetic_proc(tmp_path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    proc_root = tmp_path / "proc"
    proc = proc_root / "1235"
    proc.mkdir(parents=True)
    proc.joinpath("cwd").symlink_to(project, target_is_directory=True)
    proc.joinpath("stat").write_text("1235 (command (with spaces)) " + " ".join(["S"] + ["0"]*18 + ["1335"]))
    proc.joinpath("cmdline").write_bytes(b"python\0-m\0CORE_ROOT.stop_gate_watcher\0")
    monkeypatch.setattr(preflight, "ROOT", project)
    monkeypatch.setattr(heartbeat_io, "ROOT", project)
    payload = _observation()["heartbeats"]["guard"]
    path = tmp_path / "heartbeat.json"
    path.write_text(json.dumps(payload))
    return proc_root, proc, path, payload


@pytest.mark.parametrize("failure", [None, "dead", "reused", "foreign_cwd", "fake_argv", "substring", "missing_ticks", "generic_forged_source"])
def test_collector_uses_existing_exact_process_identity(synthetic_proc, failure):
    proc_root, proc, path, payload = synthetic_proc
    if failure == "dead":
        proc.joinpath("cmdline").unlink()
    if failure == "reused":
        proc.joinpath("stat").write_text("1235 (new process) " + " ".join(["S"] + ["0"]*18 + ["8888"]))
    if failure == "foreign_cwd":
        proc.joinpath("cwd").unlink()
        proc.joinpath("cwd").symlink_to(proc_root, target_is_directory=True)
    if failure in {"fake_argv", "generic_forged_source", "substring"}:
        argv = b"python\0writer.py\0--source\0stop_gate_watcher\0"
        if failure == "substring":
            argv = b"python\0-m\0CORE_ROOT.stop_gate_watcher_extra\0"
        proc.joinpath("cmdline").write_bytes(argv)
    if failure == "missing_ticks":
        del payload["process_start_ticks"]
        path.write_text(json.dumps(payload))
    result = preflight._heartbeat_status(path, expected_module="CORE_ROOT.stop_gate_watcher",
                                         now=1000.0, monotonic_now=500.0, proc_root=proc_root)
    assert result["fresh"] is True
    assert result["process_verified"] is (failure is None)
    if failure is None:
        assert result["run_id"] == payload["run_id"]
        assert result["boot_id"] == payload["boot_id"]
        assert result["process_start_ticks"] == "1335"


@pytest.mark.parametrize("payload", ["{broken", "[]", "null", "true", '"text"', '{"ts":true}', '{"ts":NaN}', '{"ts":Infinity}'])
def test_corrupt_heartbeat_never_raises_or_claims_fresh(tmp_path, payload):
    path = tmp_path / "heartbeat"
    path.write_text(payload)
    result = preflight._heartbeat_status(path, now=1000.0, monotonic_now=500.0)
    assert result["exists"] is True and result["fresh"] is False
    assert result["error"]


@pytest.mark.parametrize("argv,owned", [
    (["python", "-m", "uvicorn", "CONTROL_PLANE.api_server:app"], True),
    (["python", "-m", "uvicorn", "foreign:app"], False),
    (["python", "writer.py", "CONTROL_PLANE.api_server:app"], False),
    (["python", "-m", "SUPERVISOR.process_supervisor"], False),
])
def test_port_owner_is_exact_api_not_module_substring(monkeypatch, argv, owned):
    identity = _observation()["port"]["owner_identities"][0]
    identity["argv"] = argv
    monkeypatch.setattr(preflight, "_process_identity", lambda pid: identity)
    monkeypatch.setattr(preflight.subprocess, "run", lambda *a, **k: SimpleNamespace(
        returncode=0, stdout='LISTEN users:(("python",pid=2345,fd=3))', stderr=""))
    assert preflight._port_snapshot()["owned_by_project"] is owned


def test_inspection_is_read_only_and_run_transition_cannot_recover(monkeypatch):
    observation = _observation()
    metadata = observation["run_metadata"]
    states = iter([metadata, {**metadata, "run_id": "changed-during-read"}])
    monkeypatch.setattr(preflight, "safe_read_json", lambda _: next(states))
    monkeypatch.setattr(preflight.time, "time", lambda: 1000.0)
    monkeypatch.setattr(preflight.time, "monotonic", lambda: 500.0)
    monkeypatch.setattr(preflight, "_read_pid_file", lambda: (True, 1234))
    monkeypatch.setattr(preflight, "_runtime_pid_identity", lambda _: observation["runtime_pid_identity"])
    monkeypatch.setattr(preflight, "_tmux_snapshot", lambda: observation["tmux"])
    monkeypatch.setattr(preflight, "_port_snapshot", lambda: observation["port"])
    monkeypatch.setattr(preflight, "_health_snapshot", lambda: observation["health"])
    by_module = {module: observation["heartbeats"][scope]
                 for scope, (_, module) in preflight.EXPECTED_HEARTBEATS.items()}
    monkeypatch.setattr(preflight, "_heartbeat_status", lambda path, **kwargs: by_module[kwargs["expected_module"]])
    monkeypatch.setattr(preflight, "ensure_runtime_layout", lambda: pytest.fail("inspection wrote layout"))
    assert preflight.inspect_runtime_state()["decision"]["healthy"] is False


def test_preflight_report_does_not_upgrade_fresh_foreign_chain(monkeypatch):
    observation = mutated(("heartbeats", "guard", "source"), "foreign_owner")
    observation["decision"] = preflight.classify_runtime_observation(observation)
    for name in ("check_python", "check_runtime_directories", "check_imports"):
        monkeypatch.setattr(preflight, name, lambda _: True)
    monkeypatch.setattr(preflight, "inspect_runtime_state", lambda: observation)
    report = preflight.run_preflight()
    assert report.ok is False and report.already_running_healthy is False
    assert report.stale_heartbeat_found is True
    assert report.details["heartbeat"]["ok"] is False


@pytest.mark.parametrize("current_marker,incident_fails", [(False, False), (True, False), (False, True)])
def test_actual_healthy_verdict_preserves_marker_epoch_and_history(monkeypatch, tmp_path, current_marker, incident_fails):
    state = tmp_path / "RUNTIME/state"
    state.mkdir(parents=True)
    pid = tmp_path / "RUNTIME/runtime.pid"
    pid.write_text("1234")
    flag, trigger, reason = [state / f for f in ("degraded.flag", "trigger", "reason")]
    for path in (flag, trigger, reason):
        path.write_text("original " + path.name)
    os.utime(pid, ns=(2_000_000_000, 2_000_000_000))
    os.utime(flag, ns=((3 if current_marker else 1)*1_000_000_000,)*2)
    for key, value in {"ROOT":tmp_path, "RUNTIME_STATE_DIR":state, "DEGRADED_MODE_FILE":flag,
                       "STOP_GATE_TRIGGER_FILE":trigger, "LAST_DEGRADED_REASON_FILE":reason}.items():
        monkeypatch.setattr(stop_gate,key,value)
    monkeypatch.setattr(stop_gate,"ensure_runtime_layout",lambda:None)
    monkeypatch.setattr(stop_gate,"log",lambda _:None)
    records = []
    def append(reason, status):
        if incident_fails:
            raise OSError("synthetic append failure")
        records.append((reason,status))
    monkeypatch.setattr(incident_history,"write_incident_record",append)
    decision = preflight.classify_runtime_observation(_observation())
    assert decision["healthy"] is True
    monkeypatch.setattr(preflight,"inspect_runtime_state",lambda:{"decision":decision})
    if incident_fails:
        with pytest.raises(OSError):
            stop_gate.recover_previous_run_degradation()
        assert flag.exists() and records == []
    else:
        assert stop_gate.recover_previous_run_degradation() is (not current_marker)
        assert flag.exists() is current_marker
        assert [status for _,status in records] == ([] if current_marker else ["recovered"])
    assert trigger.read_text() == "original trigger"
    assert reason.read_text() == "original reason"


def test_end_to_end_collector_with_real_synthetic_files_and_proc(monkeypatch, tmp_path):
    observation = _observation()
    project, proc_root = tmp_path / "project", tmp_path / "proc"
    project.mkdir(); proc_root.mkdir()
    # This fixture's identity cwd is rebound only to the isolated synthetic root.
    monkeypatch.setattr(preflight,"ROOT",project)
    monkeypatch.setattr(heartbeat_io,"ROOT",project)
    monkeypatch.setattr(preflight.time,"time",lambda:1000.0)
    monkeypatch.setattr(preflight.time,"monotonic",lambda:500.0)
    metadata = project / "run_metadata.json"
    metadata.write_text(json.dumps(observation["run_metadata"]))
    monkeypatch.setattr(preflight,"RUN_METADATA_FILE",metadata)
    paths = dict(zip(preflight.EXPECTED_HEARTBEATS,
        ("RUNTIME_HEARTBEAT_FILE","GUARD_HEARTBEAT_FILE","CORE_GUARD_HEARTBEAT_FILE","KERNEL_HEARTBEAT_FILE")))
    def make_proc(pid, module):
        proc = proc_root / str(pid); proc.mkdir()
        proc.joinpath("cwd").symlink_to(project,target_is_directory=True)
        proc.joinpath("stat").write_text(str(pid)+" (worker) "+" ".join(["S"]+["0"]*18+[str(pid+100)]))
        argv = ["python","-m",module]
        if module == "uvicorn": argv.append("CONTROL_PLANE.api_server:app")
        proc.joinpath("cmdline").write_bytes(b"\0".join(v.encode() for v in argv)+b"\0")
    for scope,(_,module) in preflight.EXPECTED_HEARTBEATS.items():
        path = project / (scope+".json")
        payload = observation["heartbeats"][scope]
        path.write_text(json.dumps(payload)); monkeypatch.setattr(preflight,paths[scope],path)
        make_proc(payload["pid"],module)
    make_proc(2345,"uvicorn")
    process_identity, heartbeat_status = preflight._process_identity, preflight._heartbeat_status
    monkeypatch.setattr(preflight,"_process_identity",lambda pid, **kwargs:process_identity(pid,proc_root=proc_root))
    monkeypatch.setattr(preflight,"_heartbeat_status",lambda path,**kwargs:heartbeat_status(path,proc_root=proc_root,**kwargs))
    monkeypatch.setattr(preflight,"_read_pid_file",lambda:(True,1234))
    monkeypatch.setattr(preflight,"_tmux_snapshot",lambda:observation["tmux"])
    monkeypatch.setattr(preflight,"_health_snapshot",lambda:observation["health"])
    monkeypatch.setattr(preflight.subprocess,"run",lambda *a,**k:SimpleNamespace(
        returncode=0,stdout='LISTEN users:(("python",pid=2345,fd=3))',stderr=""))
    monkeypatch.setattr(preflight,"ensure_runtime_layout",lambda:pytest.fail("read-only inspection wrote layout"))
    result = preflight.inspect_runtime_state()
    assert result["decision"]["healthy"] is True
    # An unchanged fresh heartbeat cannot hide an exited/reused process.
    proc_root.joinpath("1235/stat").write_text("1235 (reused) "+" ".join(["S"]+["0"]*18+["8888"]))
    assert preflight.inspect_runtime_state()["decision"]["healthy"] is False


def test_non_utf8_heartbeat_and_process_metadata_fail_closed(synthetic_proc):
    proc_root, proc, path, _ = synthetic_proc
    path.write_bytes(b"\xff\xfe")
    assert preflight._heartbeat_status(path)["fresh"] is False
    proc.joinpath("stat").write_bytes(b"\xff\xfe")
    assert preflight._process_identity(1235,proc_root=proc_root)["alive"] is None


@pytest.mark.parametrize("removed", ["schema_version", "source", "status", "pid", "process_start_ticks", "run_id", "boot_id", "run_monotonic_time", "identity", "process_verified", "monotonic_ts", "ts"])
def test_any_missing_mandatory_heartbeat_fact_fails_closed(removed):
    observation = _observation()
    del observation["heartbeats"]["guard"][removed]
    assert preflight.classify_runtime_observation(observation)["healthy"] is False


def test_freshness_boundary_remains_fifteen_seconds():
    observation = _observation()
    for peer in observation["heartbeats"].values():
        peer["ts"], peer["monotonic_ts"] = 985.0, 485.0
    assert preflight.classify_runtime_observation(observation)["healthy"] is True
    observation["heartbeats"]["guard"]["monotonic_ts"] = 484.999
    assert preflight.classify_runtime_observation(observation)["healthy"] is False


@pytest.mark.parametrize("kind", ["foreign_live", "unreadable_metadata"])
def test_retained_stop_receipts_do_not_prove_a_foreign_or_unknown_pid_dead(synthetic_proc, kind):
    proc_root, proc, _, _ = synthetic_proc
    if kind == "foreign_live":
        proc.joinpath("cmdline").write_bytes(b"python\0foreign_writer.py\0")
    else:
        proc.joinpath("cmdline").write_bytes(b"\xff\xfe")
    identity = preflight._process_identity(1235,proc_root=proc_root)
    assert identity["alive"] is (True if kind == "foreign_live" else None)
    observation = _observation(healthy=False)
    observation.update(pid_file_exists=True,runtime_pid=1235,runtime_pid_identity=identity)
    for peer in observation["heartbeats"].values():
        peer.update(exists=True,fresh=False,status="stopped")
    decision = preflight.classify_runtime_observation(observation)
    assert decision["healthy"] is False and decision["clean"] is False
