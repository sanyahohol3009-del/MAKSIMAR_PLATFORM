"""A suspended observer must recheck freshness; a dead source still stops."""
import importlib
import pytest


@pytest.mark.parametrize("name,evaluate,kill,heartbeat", [
    ("stop_gate_watcher", "evaluate_runtime", "activate_guard_kill_chain", "write_self_heartbeat"),
    ("core_guard", "evaluate_guard", "activate_core_kill_chain", "write_self_heartbeat"),
    ("kernel_watchdog", "evaluate_core_guard", "activate_kernel_kill_chain", "write_kernel_heartbeat"),
])
@pytest.mark.parametrize("peer_recovers", [True, False])
def test_delayed_resynchronization_republishes_before_next_peer_evaluation(monkeypatch, name, evaluate, kill, heartbeat, peer_recovers):
    module = importlib.import_module("CORE_ROOT." + name)
    clock = {"now":100.0,"sleeps":0,"checks":0}
    written, killed = [], []
    monkeypatch.setattr(module, "ensure_runtime_layout", lambda:None)
    monkeypatch.setattr(module, "log", lambda message:None)
    monkeypatch.setattr(module.time, "time", lambda:clock["now"])
    monkeypatch.setattr(module, heartbeat, lambda **kwargs:written.append(clock["now"]))
    monkeypatch.setattr(module, kill, lambda reason, **kwargs: killed.append(reason))
    def sleep(seconds):
        clock["sleeps"] += 1
        if clock["sleeps"] <= 2:
            clock["now"] += 20  # both the initial poll and recovery itself stall
        elif clock["sleeps"] == 3:
            clock["now"] += seconds
        else:
            raise KeyboardInterrupt
    def check(**kwargs):
        clock["checks"] += 1
        if clock["checks"] == 1:
            return False,"fresh",0
        assert clock["sleeps"] == 3 and written[-1] == 140.0
        return not peer_recovers,"source remains stale",0
    monkeypatch.setattr(module.time, "sleep", sleep)
    monkeypatch.setattr(module, evaluate, check)
    module.main()
    assert killed == ([] if peer_recovers else ["source remains stale"])
    assert clock["checks"] == 2 and clock["now"] <= 144.0


@pytest.mark.parametrize("name,evaluate,kill,heartbeat", [
    ("stop_gate_watcher", "evaluate_runtime", "activate_guard_kill_chain", "write_self_heartbeat"),
    ("core_guard", "evaluate_guard", "activate_core_kill_chain", "write_self_heartbeat"),
    ("kernel_watchdog", "evaluate_core_guard", "activate_kernel_kill_chain", "write_kernel_heartbeat"),
])
@pytest.mark.parametrize("peer_recovers", [True, False])
def test_common_pause_allows_delayed_peer_but_not_permanent_source_loss(monkeypatch, name, evaluate, kill, heartbeat, peer_recovers):
    module = importlib.import_module("CORE_ROOT." + name)
    clock = {"now":100.0,"sleeps":0,"checks":0}
    written = []
    killed = []
    monkeypatch.setattr(module, "ensure_runtime_layout", lambda:None)
    monkeypatch.setattr(module, "log", lambda message:None)
    monkeypatch.setattr(module.time, "time", lambda:clock["now"])
    monkeypatch.setattr(module, heartbeat, lambda **kwargs:written.append(clock["now"]))
    monkeypatch.setattr(module, kill, lambda reason, **kwargs: killed.append(reason))
    def sleep(seconds):
        clock["sleeps"] += 1
        if clock["sleeps"] == 1:
            clock["now"] += 20  # write/fsync/scheduling of all peers was delayed
        elif clock["sleeps"] == 2:
            assert written[-1] == 120  # republish self after the blocked old write
            clock["now"] += seconds
        else:
            raise KeyboardInterrupt
    def check(**kwargs):
        clock["checks"] += 1
        if clock["checks"] == 1:
            return False,"fresh",0
        # A peer resumes slightly later than one 2s poll. A permanently dead
        # peer never produces a new sample and must still activate the chain.
        fresh = peer_recovers and clock["now"] >= 123
        return not fresh,"source remains stale",0
    monkeypatch.setattr(module.time, "sleep", sleep)
    monkeypatch.setattr(module, evaluate, check)
    module.main()
    assert killed == ([] if peer_recovers else ["source remains stale"])
    assert clock["now"] <= 124  # bounded grace, no indefinitely masked death


def test_stop_gate_module_cli_writes_isolated_reason_with_canonical_python(tmp_path):
    import os
    import subprocess
    from CORE_ROOT.runtime_paths import ROOT, resolve_canonical_python
    env = dict(os.environ, HOME=str(tmp_path))
    result = subprocess.run([str(resolve_canonical_python()), "-m", "CORE_ROOT.stop_gate", "isolated CLI verification"],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=10, check=False)
    assert result.returncode == 0, result.stderr
    state = tmp_path / "MAKSIMAR_PLATFORM/RUNTIME/state"
    assert (state / "degraded_mode.flag").read_text().strip() == "1"
    assert (state / "last_degraded_reason.txt").read_text().strip() == "isolated CLI verification"


@pytest.mark.parametrize("name,evaluate,kill,heartbeat", [
    ("stop_gate_watcher", "evaluate_runtime", "activate_guard_kill_chain", "write_self_heartbeat"),
    ("core_guard", "evaluate_guard", "activate_core_kill_chain", "write_self_heartbeat"),
    ("kernel_watchdog", "evaluate_core_guard", "activate_kernel_kill_chain", "write_kernel_heartbeat"),
])
@pytest.mark.parametrize("source_recovers", [True, False])
def test_observer_resume_rechecks_without_masking_dead_source(monkeypatch, name, evaluate, kill, heartbeat, source_recovers):
    module = importlib.import_module("CORE_ROOT." + name)
    clock = {"now": 100.0, "sleeps": 0, "evaluations": 0}
    kills = []
    monkeypatch.setattr(module, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(module, "log", lambda message: None)
    monkeypatch.setattr(module, heartbeat, lambda **kwargs: None)
    monkeypatch.setattr(module.time, "time", lambda: clock["now"])
    monkeypatch.setattr(module, kill, lambda reason, **kwargs: kills.append(reason))

    def sleep(seconds):
        clock["sleeps"] += 1
        if clock["sleeps"] == 1:
            clock["now"] += 20.0  # whole observer was not scheduled
        elif clock["sleeps"] == 2:
            clock["now"] += seconds  # bounded resume recheck
        else:
            raise KeyboardInterrupt

    def check(**kwargs):
        clock["evaluations"] += 1
        if clock["evaluations"] == 1:
            return False, "fresh", 0
        assert clock["sleeps"] == 2  # no immediate kill from pre-resume age
        return not source_recovers, "source remains stale", 0

    monkeypatch.setattr(module.time, "sleep", sleep)
    monkeypatch.setattr(module, evaluate, check)
    module.main()
    assert kills == ([] if source_recovers else ["source remains stale"])


@pytest.mark.parametrize("remaining,source_alive,expected_critical", [(2, True, False), (-1, True, True), (40, True, True), (2, False, True)])
def test_supervisor_recovery_lease_is_bounded_and_requires_live_owner(monkeypatch, remaining, source_alive, expected_critical):
    module = importlib.import_module("CORE_ROOT.stop_gate_watcher")
    monkeypatch.setattr(module.time, "time", lambda: 100.0)
    monkeypatch.setattr(module, "safe_read_json", lambda path: {
        "source": "process_supervisor", "status": "broken", "ts": 99.0,
        "recovery_deadline_ts": 100.0 + remaining})
    monkeypatch.setattr(module, "heartbeat_age_seconds", lambda payload: 1.0)
    monkeypatch.setattr(module, "tmux_session_exists", lambda name: True)
    monkeypatch.setattr(module, "process_exists", lambda name: source_alive)
    assert module.evaluate_runtime(0.0, 0)[0] is expected_critical


@pytest.mark.parametrize("name,evaluate,source", [
    ("core_guard", "evaluate_guard", "stop_gate_watcher"),
    ("kernel_watchdog", "evaluate_core_guard", "core_guard"),
])
def test_peer_only_pause_gets_bounded_identity_checked_grace(monkeypatch, name, evaluate, source):
    module = importlib.import_module("CORE_ROOT." + name)
    now = {"value":100.0,"age":18.0,"identity":True,"session":True,"status":"alive"}
    monkeypatch.setattr(module, "safe_read_json", lambda path: {"source":source,"status":now["status"]})
    monkeypatch.setattr(module, "heartbeat_source", lambda payload:payload["source"])
    monkeypatch.setattr(module, "heartbeat_status", lambda payload:payload["status"])
    monkeypatch.setattr(module, "heartbeat_age_seconds", lambda payload:now["age"])
    monkeypatch.setattr(module.time, "monotonic", lambda:now["value"])
    monkeypatch.setattr(module, "heartbeat_process_alive", lambda *args:now["identity"])
    monkeypatch.setattr(module, "process_exists", lambda pattern:True)
    monkeypatch.setattr(module, "tmux_session_exists", lambda session:now["session"])
    state = {}
    evaluate_fn = getattr(module, evaluate)
    assert evaluate_fn(0,0,peer_stale_state=state)[0] is False
    now["value"] += 5;now["age"] = 1
    assert evaluate_fn(0,0,peer_stale_state=state)[0] is False and state == {}
    now["age"] = 18
    assert evaluate_fn(0,0,peer_stale_state=state)[0] is False
    now["value"] += module.PEER_RESYNCHRONIZATION_LIMIT_SEC
    assert evaluate_fn(0,0,peer_stale_state=state)[0] is True  # alive-but-hung is not masked forever
    for field in ("identity", "session"):
        state.clear();now[field] = False
        assert evaluate_fn(0,0,peer_stale_state=state)[0] is True
        now[field] = True
    state.clear();now["status"] = "stopped"
    assert evaluate_fn(0,0,peer_stale_state=state)[0] is True


def test_heartbeat_peer_identity_rejects_pid_reuse_foreign_root_and_fake_module_arguments(tmp_path, monkeypatch):
    from CORE_ROOT import heartbeat_io as io
    project = tmp_path / "project";project.mkdir()
    proc_root = tmp_path / "proc";proc = proc_root / "31337";proc.mkdir(parents=True)
    proc.joinpath("cwd").symlink_to(project, target_is_directory=True)
    monkeypatch.setattr(io, "ROOT", project)
    def stat(ticks): return "31337 (command with (parentheses)) " + " ".join(["S"] + ["0"]*18 + [str(ticks)])
    proc.joinpath("stat").write_text(stat(123))
    proc.joinpath("cmdline").write_bytes(b"python3\0-m\0CORE_ROOT.core_guard\0")
    payload = {"pid":31337,"process_start_ticks":"123"}
    assert io.heartbeat_process_alive(payload,"CORE_ROOT.core_guard",proc_root=proc_root)
    proc.joinpath("stat").write_text(stat(124))
    assert not io.heartbeat_process_alive(payload,"CORE_ROOT.core_guard",proc_root=proc_root)
    proc.joinpath("stat").write_text(stat(123))
    proc.joinpath("cmdline").write_bytes(b"python3\0-c\0pass\0-m\0CORE_ROOT.core_guard\0")
    assert not io.heartbeat_process_alive(payload,"CORE_ROOT.core_guard",proc_root=proc_root)
    proc.joinpath("cmdline").write_bytes(b"python3\0-m\0CORE_ROOT.core_guard\0")
    proc.joinpath("cwd").unlink();proc.joinpath("cwd").symlink_to(tmp_path,target_is_directory=True)
    assert not io.heartbeat_process_alive(payload,"CORE_ROOT.core_guard",proc_root=proc_root)
    assert not io.heartbeat_process_alive({"pid":31337},"CORE_ROOT.core_guard",proc_root=proc_root)
