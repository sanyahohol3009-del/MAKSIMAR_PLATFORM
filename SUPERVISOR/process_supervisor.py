#!/usr/bin/env python3
"""MAKSIMAR runtime process supervisor."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import threading

from CORE_ROOT.heartbeat_io import atomic_write_json, build_heartbeat
from CORE_ROOT import run_context
from CORE_ROOT.runtime_paths import (
    CONTROL_PLANE_HOST,
    DEGRADED_MODE_FILE,
    CONTROL_PLANE_PORT,
    RUNTIME_HEARTBEAT_FILE,
    ROOT,
    SYSTEM_LOG_FILE,
    ensure_runtime_layout,
    resolve_canonical_python,
)

RESTART_DELAY_SEC = 2
POLL_INTERVAL_SEC = 2


def log(message: str) -> None:
    """Write a timestamped message to stdout and the shared system log."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[SUPERVISOR] {timestamp} {message}"
    print(line, flush=True)
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as file_obj:
        file_obj.write(line + "\n")


def write_heartbeat(status: str = "alive", *, recovery_deadline_ts: float | None = None) -> None:
    """Write runtime heartbeat atomically."""
    ensure_runtime_layout()
    payload = build_heartbeat(source="process_supervisor", status=status)
    if recovery_deadline_ts is not None:
        payload["recovery_deadline_ts"] = recovery_deadline_ts
    atomic_write_json(RUNTIME_HEARTBEAT_FILE, payload)


def build_environment() -> dict[str, str]:
    """Return environment for the Control Plane child process."""
    env = dict(os.environ)
    env.setdefault("JARVIS_HELPER_INPUT_CORRECTION_ENABLED", "true")
    env.setdefault("JARVIS_HELPER_MODEL", "jarvis:helper3b")
    env.setdefault("OLLAMA_NUM_PARALLEL", "1")
    env.setdefault("OLLAMA_MAX_LOADED_MODELS", "1")
    return env


def record_child_lifecycle(event_type: str, *, child_pid: int, exit_code: int | None = None) -> None:
    """Publish actual child facts through the existing platform event journal."""
    from uuid import uuid4
    from MAKSIMAR_CORE_LIB.event_bus.event_models import EventRecord
    from MAKSIMAR_CORE_LIB.event_bus.event_writer import append_event_record
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import utc_observed_at
    try:
        append_event_record(EventRecord(event_id="runtime_" + uuid4().hex,
            event_type=event_type, source="process_supervisor", created_at=utc_observed_at(),
            payload={"child_pid": child_pid, "supervisor_pid": os.getpid(),
                     "exit_code": exit_code, "project_root": str(ROOT)}))
    except OSError as exc:
        log(f"Lifecycle event persistence failed: {type(exc).__name__}")


def build_command() -> list[str]:
    """Return command for starting Control Plane with canonical interpreter."""
    python_path = resolve_canonical_python()
    return [
        str(python_path),
        "-m",
        "uvicorn",
        "CONTROL_PLANE.api_server:app",
        "--host",
        CONTROL_PLANE_HOST,
        "--port",
        str(CONTROL_PLANE_PORT),
    ]


def _prepare_run_context() -> None:
    # A new supervisor may not relabel a previous live guard/API as a new run.
    from CORE_ROOT.heartbeat_io import find_owned_module_process_pids
    from SUPERVISOR.runtime_preflight import _port_snapshot
    modules = ("SUPERVISOR.process_supervisor", "CORE_ROOT.stop_gate_watcher",
               "CORE_ROOT.core_guard", "CORE_ROOT.kernel_watchdog", "uvicorn")
    for module in modules:
        pids = find_owned_module_process_pids(module)
        expected = (os.getpid(),) if module == "SUPERVISOR.process_supervisor" else ()
        if pids is None or pids != expected:
            raise RuntimeError("new run refused: existing/unknown owned process: " + module)
    port = _port_snapshot()
    if port.get("listening") is not False or port.get("error"):
        raise RuntimeError("new run refused: control-plane port not proven free")


def _update_run_readiness(process) -> None:
    from SUPERVISOR.runtime_preflight import _port_snapshot, _health_snapshot
    # Only current-run degradation blocks running; old markers await StopGate.
    metadata = run_context.read_run_metadata()
    if (DEGRADED_MODE_FILE.is_file() and metadata is not None
            and DEGRADED_MODE_FILE.stat().st_mtime >= metadata["wall_time"]):
        run_context.set_run_status(run_context.RUN_STATUS_DEGRADED)
        return
    if run_context.read_run_status() not in (
            run_context.RUN_STATUS_BOOTING, run_context.RUN_STATUS_DEGRADED):
        return
    port = _port_snapshot()
    if (port.get("owned_by_project") is True and not port.get("error")
            and port.get("owner_pids") == [process.pid]):
        health = _health_snapshot()
        if (health.get("ok") is True and health.get("status") == 200
                and not health.get("error") and process.poll() is None):
            run_context.set_run_status(run_context.RUN_STATUS_RUNNING)


def main() -> None:
    """Own exactly one project run across child retries and orderly shutdown."""
    ensure_runtime_layout()
    canonical_python = resolve_canonical_python()
    if not canonical_python.is_file():
        raise FileNotFoundError(str(canonical_python))
    process = None
    stop_requested = False
    stop_event = threading.Event()
    initialized = False
    recovery_deadline_ts = None

    def handle_stop(signum, frame):
        nonlocal stop_requested
        stop_requested = True
        stop_event.set()
        log(f"Received stop signal: {signum}")
        if process is not None and process.poll() is None:
            process.terminate()

    def finish_child():
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=POLL_INTERVAL_SEC)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=POLL_INTERVAL_SEC)
                return False
        return True

    with run_context.run_lifecycle():
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, handle_stop)
        try:
            _prepare_run_context()
            run_context.initialize_run_metadata()
            initialized = True
            # The same existing hint marks the actual run boundary for StopGate epochs.
            with run_context.runtime_mutation():
                pidfile = ROOT / "RUNTIME/runtime.pid"
                temporary = pidfile.with_suffix(".pid.tmp")
                with temporary.open("w") as handle:
                    handle.write(str(os.getpid()) + "\n")
                    handle.flush()
                    os.fsync(handle.fileno())
                temporary.replace(pidfile)
            while not stop_requested:
                run_context.initialize_run_metadata()  # idempotent identity fence
                cmd = build_command()
                write_heartbeat("booting", recovery_deadline_ts=recovery_deadline_ts)
                if stop_requested:
                    break
                log(f"Starting Control Plane: {' '.join(cmd)}")
                process = subprocess.Popen(cmd, cwd=str(ROOT), text=True, env=build_environment())
                record_child_lifecycle("runtime.child.started", child_pid=process.pid)
                while not stop_requested and process.poll() is None:
                    run_context.initialize_run_metadata()  # detects replacement/loss
                    write_heartbeat("alive", recovery_deadline_ts=time.time() + 2 * POLL_INTERVAL_SEC)
                    _update_run_readiness(process)
                    recovery_deadline_ts = None
                    stop_event.wait(POLL_INTERVAL_SEC)
                if stop_requested:
                    break
                return_code = process.poll()
                run_context.set_run_status(run_context.RUN_STATUS_DEGRADED)
                recovery_deadline_ts = time.time() + 12.0
                record_child_lifecycle("runtime.child.exited", child_pid=process.pid, exit_code=return_code)
                write_heartbeat("broken", recovery_deadline_ts=recovery_deadline_ts)
                log(f"Control Plane exited with code {return_code}. Restarting in {RESTART_DELAY_SEC}s...")
                stop_event.wait(RESTART_DELAY_SEC)
            orderly_child = finish_child()
            run_context.set_run_status(run_context.RUN_STATUS_SHUTDOWN if orderly_child else run_context.RUN_STATUS_CRASHED)
            if process is not None:
                record_child_lifecycle("runtime.child.stopped", child_pid=process.pid, exit_code=process.poll())
            write_heartbeat("stopped" if orderly_child else "broken")
            log("Supervisor exited cleanly." if orderly_child else "Supervisor exit required forced child cleanup.")
        except BaseException:
            try:
                finish_child()
            finally:
                if initialized:
                    run_context.set_run_status(run_context.RUN_STATUS_CRASHED)
                    write_heartbeat("broken")
            raise


if __name__ == "__main__":
    main()
