from __future__ import annotations
import pathlib
import os
import shlex
import subprocess
import pytest
from CORE_ROOT import heartbeat_io


def _proc(proc_root, pid, module, cwd):
    p = proc_root / str(pid)
    p.mkdir(parents=True)
    (p / "cmdline").write_bytes(f"python3\0-m\0{module}\0".encode())
    (p / "stat").write_text(f"{pid} (python3) " + " ".join(["S"] + ["0"] * 18 + ["123"]))
    (p / "cwd").symlink_to(cwd, target_is_directory=True)


def test_module_discovery_ignores_foreign_pidfile_and_wrong_identity(monkeypatch, tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(heartbeat_io, "ROOT", project)
    proc = tmp_path / "proc"
    _proc(proc, 10, "CORE_ROOT.stop_gate_watcher_extra", project)
    _proc(proc, 11, "CORE_ROOT.stop_gate_watcher", tmp_path)
    _proc(proc, 12, "CORE_ROOT.stop_gate_watcher", project)
    pidfile = tmp_path / "guard.pid"
    pidfile.write_text("10")
    assert heartbeat_io.find_owned_module_process_pid("CORE_ROOT.stop_gate_watcher", pidfile=pidfile, proc_root=proc) == 12


def test_module_discovery_fails_closed_on_duplicate_owned_processes(monkeypatch, tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(heartbeat_io, "ROOT", project)
    proc = tmp_path / "proc"
    for pid in (10, 11):
        _proc(proc, pid, "CORE_ROOT.core_guard", project)
    assert heartbeat_io.find_owned_module_process_pid("CORE_ROOT.core_guard", proc_root=proc) is None


def test_module_discovery_missing_process_is_not_pidfile_liveness(monkeypatch, tmp_path):
    proc = tmp_path / "proc"
    proc.mkdir()
    pidfile = tmp_path / "runtime.pid"
    pidfile.write_text("123")
    assert heartbeat_io.find_owned_module_process_pid("SUPERVISOR.process_supervisor", pidfile=pidfile, proc_root=proc) is None


def test_runtime_ctl_stale_heartbeat_cannot_publish_alive():
    script = pathlib.Path("tools/ctl").read_text().split('case "${1:-}" in', 1)[0]
    overrides = """
session_exists() { return 0; }
process_exists() { return 0; }
heartbeat_is_fresh() { return 1; }
heartbeat_age() { printf '1000\n'; }
http_health() { return 0; }
port_listening() { return 0; }
degraded_active() { return 1; }
process_age_seconds() { printf '1000\n'; }
normalized_state
"""
    result = subprocess.run(["bash"], input=script + overrides, text=True, capture_output=True, check=True)
    assert result.stdout.strip() != "ALIVE"


@pytest.mark.parametrize("script_name, finder", [("tools/guard_ctl", "find_guard_pid"), ("tools/core_guard_ctl", "find_pid"), ("tools/kernel_guard_ctl", "find_pid")])
def test_guard_pidfile_cannot_select_unrelated_live_process(tmp_path, script_name, finder):
    script = pathlib.Path(script_name).read_text().split('main "$@"', 1)[0]
    pidfile = tmp_path / "foreign.pid"
    pidfile.write_text(str(os.getpid()))
    # Only discover; never stop/kill a process. Old kill -0 trusts this parent PID.
    result = subprocess.run(["bash"], input=script + f"\nPID_FILE={shlex.quote(str(pidfile))}\n{finder} || true\n", text=True, capture_output=True, check=True)
    assert result.stdout.strip() != str(os.getpid())


@pytest.mark.parametrize("status, source", [("stopped", "process_supervisor"), ("alive", "foreign_writer")])
def test_runtime_ctl_fresh_time_without_canonical_status_source_is_not_alive(tmp_path, status, source):
    import json, time
    script = pathlib.Path("tools/ctl").read_text().split('case "${1:-}" in', 1)[0]
    heartbeat = tmp_path / "heartbeat.json"
    heartbeat.write_text(json.dumps({"ts":time.time(), "status":status, "source":source, "pid":os.getpid(), "process_start_ticks":"1"}))
    result = subprocess.run(["bash"], input=script + f"\nHEARTBEAT_FILE={shlex.quote(str(heartbeat))}\nheartbeat_is_fresh && printf 'ACCEPTED\n' || printf 'REJECTED\n'\n", text=True, capture_output=True, check=True)
    assert result.stdout.strip() == "REJECTED"


def test_ctl_displayed_age_uses_same_canonical_monotonic_clock(tmp_path):
    import json, time
    script = pathlib.Path("tools/ctl").read_text().split('case "${1:-}" in', 1)[0]
    heartbeat = tmp_path / "heartbeat.json"
    heartbeat.write_text(json.dumps({"ts":time.time()-1000, "monotonic_ts":time.monotonic()-5}))
    result = subprocess.run(["bash"], input=script + f"\nHEARTBEAT_FILE={shlex.quote(str(heartbeat))}\nheartbeat_age\n", text=True, capture_output=True, check=True)
    assert 4 <= float(result.stdout.strip()) <= 10


@pytest.mark.parametrize("rest_status,work_status,expected", [(0,0,["REST","WORK"]),(7,0,["REST"]),(0,5,["REST","WORK"])])
def test_ctl_restart_delegates_full_guard_ordering_and_propagates_failure(tmp_path, rest_status, work_status, expected):
    source=pathlib.Path("tools/ctl").read_text()
    prefix,dispatch=source.split('case "${1:-}" in',1)
    fake_root=tmp_path/"project with spaces"
    (fake_root/"tools").mkdir(parents=True)
    calls=tmp_path/"calls"
    for name,status in (("rest",rest_status),("work",work_status)):
        (fake_root/"tools"/name).write_text(
            "#!/bin/bash\nprintf '%s\\n' "+shlex.quote(name.upper())+" >> "+shlex.quote(str(calls))+"\nexit "+str(status)+"\n")
    # Execute the actual public case branch, with only owned lifecycle targets isolated.
    # Unsafe old stop/start branches cannot touch the real runtime in this test.
    overrides="\nROOT="+shlex.quote(str(fake_root))+"\nstart() { return 99; }\nstop() { return 99; }\n"
    script=prefix+overrides+'case "${1:-}" in'+dispatch
    result=subprocess.run(["bash","-s","restart"],input=script,text=True,capture_output=True)
    assert result.returncode == (rest_status or work_status),result.stdout+result.stderr
    assert calls.read_text().splitlines() == expected
