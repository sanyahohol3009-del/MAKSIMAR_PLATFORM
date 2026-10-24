#!/usr/bin/env python3
"""STOP-GATE trigger for MAKSIMAR foundation services."""

from __future__ import annotations

import sys
import time
import fcntl
import os
import threading
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


_transition_local = threading.local()


@contextmanager
def _transition_lock():
    """Mutation -> transition, one actual transition FD per thread/process scope."""
    held = getattr(_transition_local, "handle", None)
    if held is not None:
        if getattr(_transition_local, "pid", None) == os.getpid():
            raise RuntimeError("StopGate transition scope is not reentrant")
        held.close()  # Child copy only; never unlock a parent's file description.
        _transition_local.handle = None
    ensure_runtime_layout()
    from CORE_ROOT.run_context import runtime_mutation, _coordination_fd
    with runtime_mutation():
        fd = _coordination_fd(RUNTIME_STATE_DIR / "stop_gate_transition.lock")
        with os.fdopen(fd, "a") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            _transition_local.handle, _transition_local.pid = handle, os.getpid()
            try:
                yield
            finally:
                _transition_local.handle = None


def _require_transition_scope() -> None:
    """Private mutation requires the live Core-owned kernel lock, not a proof token."""
    handle = getattr(_transition_local, "handle", None)
    if (handle is None or handle.closed
            or getattr(_transition_local, "pid", None) != os.getpid()):
        raise RuntimeError("previous-run mutation requires the active StopGate transition scope")
    opened = os.fstat(handle.fileno())
    current = os.stat(RUNTIME_STATE_DIR / "stop_gate_transition.lock", follow_symlinks=False)
    if (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino):
        raise RuntimeError("StopGate transition inode changed")


def _capture_previous_run_marker():
    """Capture immutable marker/PID evidence; no marker keeps existing no-op success."""
    _require_transition_scope()
    from CORE_ROOT.incident_history import _evidence_file_identity
    try:
        DEGRADED_MODE_FILE.lstat()
    except FileNotFoundError:
        return None
    marker = _evidence_file_identity(DEGRADED_MODE_FILE)
    data = DEGRADED_MODE_FILE.read_bytes()
    if _evidence_file_identity(DEGRADED_MODE_FILE) != marker:
        raise RuntimeError("degradation marker changed during capture")
    pid_file = ROOT / "RUNTIME/runtime.pid"
    pid = _evidence_file_identity(pid_file)
    return (tuple(sorted(marker.items())), data, tuple(sorted(pid.items())))


def _previous_run_marker_eligible(state, epoch) -> bool:
    """Recheck local identity/order only; health authority stays in Supervisor."""
    _require_transition_scope()
    from CORE_ROOT.incident_history import _evidence_file_identity
    from CORE_ROOT.run_context import read_run_metadata, _identity
    try:
        metadata = read_run_metadata()
        if not isinstance(metadata, dict):
            return False
        if (_identity(metadata) + (metadata.get("status"),)) != epoch[0]:
            return False
        marker = _evidence_file_identity(DEGRADED_MODE_FILE)
        pid_file = ROOT / "RUNTIME/runtime.pid"
        pid = _evidence_file_identity(pid_file)
        if tuple(sorted(marker.items())) != state[0] or tuple(sorted(pid.items())) != state[2]:
            return False
        if pid_file.read_text(encoding="utf-8").strip() != str(epoch[1]):
            return False
        return (marker["st_mtime_ns"] < int(metadata["wall_time"] * 1_000_000_000)
                and marker["st_mtime_ns"] < pid["st_mtime_ns"])
    except (OSError, ValueError, TypeError, KeyError, UnicodeError):
        return False


def _prepare_previous_run_recovery(state, epoch) -> bool:
    """Durable intent before mutation, never a completed recovery receipt."""
    if not _previous_run_marker_eligible(state, epoch):
        return False
    from CORE_ROOT.incident_history import write_incident_record
    reason = (LAST_DEGRADED_REASON_FILE.read_text(encoding="utf-8").strip()
              if LAST_DEGRADED_REASON_FILE.is_file() else "previous run degradation")
    write_incident_record("Verified WORK preparing previous-run recovery: " + reason, status="recovery_pending")
    return True


def _commit_previous_run_recovery(state, epoch) -> bool:
    """Private marker commit in the existing scope; accepts no health override."""
    if not _previous_run_marker_eligible(state, epoch):
        return False
    from CORE_ROOT.incident_history import write_incident_record
    reason = (LAST_DEGRADED_REASON_FILE.read_text(encoding="utf-8").strip()
              if LAST_DEGRADED_REASON_FILE.is_file() else "previous run degradation")
    # The second full inspection has just completed under this same lock.
    # Revalidate after reading diagnostic text, immediately before mutation.
    if not _previous_run_marker_eligible(state, epoch):
        return False
    DEGRADED_MODE_FILE.unlink()
    try:
        write_incident_record("Verified WORK recovered previous run: " + reason, status="recovered")
    except BaseException:
        # Restore only our absent marker; never overwrite an independent activation.
        try:
            with DEGRADED_MODE_FILE.open("xb") as handle:
                handle.write(state[1])
                handle.flush()
                os.fsync(handle.fileno())
            previous = dict(state[0])
            os.chmod(DEGRADED_MODE_FILE, previous["st_mode"] & 0o777)
            os.utime(DEGRADED_MODE_FILE, ns=(previous["st_mtime_ns"], previous["st_mtime_ns"]))
        except FileExistsError:
            pass
        try:
            write_incident_record("Previous-run recovery completion failed; degradation retained", status="recovery_failed")
        except (OSError, ValueError):
            pass
        raise
    try:
        log("RECOVERED previous run degradation after owned runtime and full heartbeat chain verification")
    except OSError:
        # Authoritative completion is durable; an auxiliary log failure is not a failed mutation.
        pass
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
