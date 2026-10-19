#!/usr/bin/env python3
"""STOP-GATE trigger for MAKSIMAR foundation services."""

from __future__ import annotations

import sys
import time
import fcntl
from contextlib import contextmanager

from CORE_ROOT.runtime_paths import (
    DEGRADED_MODE_FILE,
    LAST_DEGRADED_REASON_FILE,
    STOP_GATE_TRIGGER_FILE,
    SYSTEM_LOG_FILE,
    RUNTIME_STATE_DIR,
    ROOT,
    ensure_runtime_layout,
)


@contextmanager
def _transition_lock():
    ensure_runtime_layout()
    with (RUNTIME_STATE_DIR / "stop_gate_transition.lock").open("a") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield


def recover_previous_run_degradation() -> bool:
    """Clear only a previous run's diagnostic marker after verified WORK.

    Reuse the existing preflight ownership/health classifier. A STOP-GATE
    raised during this run remains active; preserve trigger/reason/history.
    This does not reset settings or alter host authorization.
    """
    from SUPERVISOR.runtime_preflight import inspect_runtime_state
    from CORE_ROOT.incident_history import write_incident_record
    with _transition_lock():
        if not DEGRADED_MODE_FILE.is_file():
            return True
        observation = inspect_runtime_state()
        if observation["decision"].get("healthy") is not True:
            return False
        pid_file = ROOT / "RUNTIME/runtime.pid"
        if not pid_file.is_file() or DEGRADED_MODE_FILE.stat().st_mtime_ns >= pid_file.stat().st_mtime_ns:
            return False
        reason = LAST_DEGRADED_REASON_FILE.read_text(encoding="utf-8").strip() if LAST_DEGRADED_REASON_FILE.is_file() else "previous run degradation"
        write_incident_record("Verified WORK recovered previous run: " + reason, status="recovered")
        DEGRADED_MODE_FILE.unlink()
        log("RECOVERED previous run degradation after owned runtime and full heartbeat chain verification")
        return True


def log(message: str) -> None:
    """Write a STOP-GATE message to stdout and the shared system log."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[STOP-GATE] {timestamp} {message}"
    print(line, flush=True)
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as file_obj:
        file_obj.write(line + "\n")


def main() -> None:
    """Record a STOP-GATE activation."""
    ensure_runtime_layout()

    reason = " ".join(sys.argv[1:]).strip() or "stop-gate triggered"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with _transition_lock():
        STOP_GATE_TRIGGER_FILE.write_text(
            f"{timestamp} | {reason}\n",
            encoding="utf-8",
        )
        DEGRADED_MODE_FILE.write_text("1\n", encoding="utf-8")
        LAST_DEGRADED_REASON_FILE.write_text(reason + "\n", encoding="utf-8")

    log(f"ACTIVATED: {reason}")


if __name__ == "__main__":
    main()
