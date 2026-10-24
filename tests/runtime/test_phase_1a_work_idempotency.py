from __future__ import annotations

from pathlib import Path

from SUPERVISOR.runtime_preflight import EXPECTED_SESSIONS, classify_runtime_observation


ROOT = Path(__file__).resolve().parents[2]


def _observation(*, healthy: bool = True) -> dict[str, object]:
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
        "tmux": {"available": True, "sessions": sorted(EXPECTED_SESSIONS) if healthy else []},
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


def test_healthy_runtime_is_already_running_not_stale_or_conflict() -> None:
    decision = classify_runtime_observation(_observation())

    assert decision["classification"] == "already_running_healthy"
    assert decision["healthy"] is True
    assert decision["reasons"] == []
    assert decision["all_heartbeats_fresh"] is True
    assert decision["port_owned_by_project"] is True


def test_real_stale_pid_is_detected() -> None:
    observation = _observation(healthy=False)
    observation["pid_file_exists"] = True
    observation["runtime_pid"] = 999999
    observation["runtime_pid_identity"] = {"alive": False, "matches": False}

    decision = classify_runtime_observation(observation)

    assert decision["classification"] == "stale_runtime_state"
    assert "stale_or_mismatched_runtime_pid" in decision["reasons"]


def test_foreign_process_on_8000_is_a_port_conflict() -> None:
    observation = _observation(healthy=False)
    observation["port"] = {"listening": True, "owner_pids": [4321], "owned_by_project": False}

    decision = classify_runtime_observation(observation)

    assert decision["classification"] == "port_conflict_foreign_process"
    assert decision["reasons"][0] == "foreign_process_on_control_plane_port"


def test_work_healthy_branch_exits_before_cleanup_or_start() -> None:
    source = (ROOT / "tools/work").read_text(encoding="utf-8")
    healthy_branch = source.split("if preflight_reports_healthy_runtime; then", 1)[1].split("fi", 1)[0]

    assert 'log "already running / healthy"' in healthy_branch
    assert "exit 0" in healthy_branch
    assert "rest" not in healthy_branch
    assert "start_runtime" not in healthy_branch
    assert source.index("if preflight_reports_healthy_runtime; then") < source.index(
        "remove_disposable_runtime_artifacts", source.index("main()")
    )


def test_preflight_rejection_does_not_call_rest() -> None:
    source = (ROOT / "tools/work").read_text(encoding="utf-8")
    rejection_branch = source.split("if ! run_preflight; then", 1)[1].split("\n  fi\n", 1)[0]

    assert "rest" not in rejection_branch
    assert "ui_open" not in rejection_branch
    assert "start_runtime" not in rejection_branch
    assert "exit 1" in rejection_branch


def test_rest_chain_contains_no_broad_process_kill() -> None:
    paths = [
        ROOT / "tools/rest",
        ROOT / "tools/ctl",
        ROOT / "tools/guard_ctl",
        ROOT / "tools/core_guard_ctl",
        ROOT / "tools/kernel_guard_ctl",
        ROOT / "tools/oob_dashboard_ctl",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    for forbidden in (
        "tmux kill-server", "pkill ", "killall ", "taskkill", "Stop-Process",
        "wsl --shutdown", "wsl.exe --shutdown",
    ):
        assert forbidden not in combined


def test_dashboard_cleanup_is_exactly_owned_and_excludes_manual_and_codex_sessions() -> None:
    work = (ROOT / "tools/work").read_text(encoding="utf-8")
    rest = (ROOT / "tools/rest").read_text(encoding="utf-8")
    ui_open = (ROOT / "tools/ui_open").read_text(encoding="utf-8")

    assert 'DASHBOARD_SESSION="maksimar_dashboard"' in work
    assert "dashboard_session_ownership.env" in work
    assert "operator_shell_owned=false" in work
    assert "codex_session_owned=false" in work
    assert "dashboard_ownership_is_exact" in rest
    assert 'tmux kill-session -t "$DASHBOARD_SESSION"' in rest
    assert "maksimar_operator" not in rest
    assert 'tmux kill-session -t "$CODEX' not in rest
    assert 'WINDOW_ID="JARVIS_RUNTIME_DASHBOARDS"' in ui_open
    assert "-w 0" not in ui_open
    assert "Command Console" not in ui_open
    assert '--cd "$ROOT" --exec tmux attach -t "$DASHBOARD_SESSION:dashboard"' in ui_open
    assert '--cd "$ROOT" --exec tmux attach -t "$OOB_SESSION"' in ui_open
    assert "; exec bash" not in ui_open


def test_healthy_repeat_returns_before_duplicate_windows_or_sessions() -> None:
    source = (ROOT / "tools/work").read_text(encoding="utf-8")
    healthy_branch = source.split("if preflight_reports_healthy_runtime; then", 1)[1].split("fi", 1)[0]
    assert "exit 0" in healthy_branch
    assert "ui_open" not in healthy_branch
    assert "tmux new-session" not in healthy_branch


def test_parallel_windows_edge_runtime_launcher_is_absent() -> None:
    assert not (ROOT / "tools/jarvis_live_runtime/start_jarvis_edge.ps1").exists()
    policy = (ROOT / "tools/jarvis_live_runtime/voice_edge_v2_policy.py").read_text(encoding="utf-8")
    assert "127.0.0.1:8000" in policy
    assert "127.0.0.1:8765" not in policy
