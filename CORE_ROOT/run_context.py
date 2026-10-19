#!/usr/bin/env python3
"""Run context helpers for MAKSIMAR foundation services."""

from __future__ import annotations

import time
import os
import fcntl
from contextlib import contextmanager
import uuid
from typing import Any

from CORE_ROOT.runtime_paths import RUN_METADATA_FILE, RUNTIME_STATE_DIR, ensure_runtime_layout

RUN_METADATA_SCHEMA_VERSION = 1

RUN_STATUS_BOOTING = "booting"
RUN_STATUS_RUNNING = "running"
RUN_STATUS_DEGRADED = "degraded"
RUN_STATUS_MAINTENANCE = "maintenance"
RUN_STATUS_SHUTDOWN = "shutdown"
RUN_STATUS_CRASHED = "crashed"

ALLOWED_RUN_STATUSES = {
    RUN_STATUS_BOOTING,
    RUN_STATUS_RUNNING,
    RUN_STATUS_DEGRADED,
    RUN_STATUS_MAINTENANCE,
    RUN_STATUS_SHUTDOWN,
    RUN_STATUS_CRASHED,
}


_writer_pid: int | None = None
_writer_identity: tuple | None = None


@contextmanager
def run_lifecycle():
    """Fence the existing supervisor writer for its process lifetime.

    The lock is coordination, not a second state store. It is not inherited by
    the API child. Failed/duplicate acquisition never initializes metadata.
    """
    global _writer_pid, _writer_identity
    if _writer_pid is not None:
        raise RuntimeError("run lifecycle writer already active")
    ensure_runtime_layout()
    with os.fdopen(_coordination_fd(RUNTIME_STATE_DIR / "run_lifecycle.lock"), "a") as lease:
        fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        from CORE_ROOT.heartbeat_io import heartbeat_process_alive, _process_start_ticks
        from pathlib import Path
        pid = os.getpid()
        if not heartbeat_process_alive(
                {"pid": pid, "process_start_ticks": _process_start_ticks(Path("/proc") / str(pid))},
                "SUPERVISOR.process_supervisor"):
            raise RuntimeError("run lifecycle writer is not the canonical supervisor")
        _writer_pid, _writer_identity = pid, None
        try:
            yield
        finally:
            same_process = _writer_pid == os.getpid()
            _writer_pid, _writer_identity = None, None
            if same_process:
                fcntl.flock(lease.fileno(), fcntl.LOCK_UN)


def _require_run_writer() -> None:
    if _writer_pid != os.getpid():
        raise RuntimeError("run metadata mutation requires the supervisor lifecycle lease")


def _identity(payload: dict[str, Any]) -> tuple:
    return tuple(payload.get(key) for key in (
        "schema_version", "run_id", "boot_id", "wall_time", "monotonic_time"))


def new_run_id() -> str:
    """Generate a unique run identifier."""
    return uuid.uuid4().hex


def new_boot_id() -> str:
    """Generate a unique boot identifier."""
    return uuid.uuid4().hex


def validate_run_status(status: str) -> str:
    """Validate lifecycle status."""
    if not isinstance(status, str):
        raise ValueError("run status must be a string")

    normalized = status.strip().lower()
    if normalized not in ALLOWED_RUN_STATUSES:
        raise ValueError(f"unsupported run status: {status!r}")

    return normalized


def build_run_metadata(status: str = RUN_STATUS_BOOTING) -> dict[str, Any]:
    """Build initial run metadata payload."""
    normalized = validate_run_status(status)
    wall = time.time()
    mono = time.monotonic()

    return {
        "schema_version": RUN_METADATA_SCHEMA_VERSION,
        "run_id": new_run_id(),
        "boot_id": new_boot_id(),
        "wall_time": wall,
        "monotonic_time": mono,
        "status": normalized,
        "updated_wall_time": wall,
        "updated_monotonic_time": mono,
    }


def write_run_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    """Write run metadata atomically."""
    from CORE_ROOT.heartbeat_io import atomic_write_json

    if not isinstance(payload, dict):
        raise ValueError("run metadata payload must be a dict")

    _require_run_writer()
    if _writer_identity is not None:
        current = read_run_metadata()
        if (current is None or _identity(current) != _writer_identity
                or _identity(payload) != _writer_identity):
            raise RuntimeError("run metadata identity changed outside current lifecycle")
    atomic_write_json(RUN_METADATA_FILE, payload)
    # Metadata transitions also persist the rename/directory entry. Heartbeat
    # polling keeps its existing writer/cadence; this is only the run store.
    directory = os.open(RUN_METADATA_FILE.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return payload


def read_run_metadata() -> dict[str, Any] | None:
    """Read run metadata from disk."""
    from CORE_ROOT.heartbeat_io import safe_read_json

    try:
        payload = safe_read_json(RUN_METADATA_FILE)
    except UnicodeError:
        return None

    if not isinstance(payload, dict):
        return None

    return payload


def initialize_run_metadata(status: str = RUN_STATUS_BOOTING) -> dict[str, Any]:
    """Create once per actual supervisor lifetime; repeated calls preserve it."""
    global _writer_identity
    _require_run_writer()
    if _writer_identity is not None:
        payload = read_run_metadata()
        if payload is None or _identity(payload) != _writer_identity:
            raise RuntimeError("current lifecycle metadata is missing or replaced")
        return payload
    if validate_run_status(status) != RUN_STATUS_BOOTING:
        raise ValueError("new supervisor lifecycle must begin booting")
    payload = build_run_metadata(status=status)
    write_run_metadata(payload)
    _writer_identity = _identity(payload)
    return payload


def set_run_status(status: str) -> dict[str, Any]:
    """Update lifecycle status on existing run metadata."""
    _require_run_writer()
    if _writer_identity is None:
        raise RuntimeError("run lifecycle is not initialized")
    normalized = validate_run_status(status)

    payload = read_run_metadata()
    if payload is None:
        raise RuntimeError("run metadata file is missing")

    if _identity(payload) != _writer_identity:
        raise RuntimeError("run metadata belongs to another lifecycle")
    if payload.get("status") == normalized:
        return payload

    payload["status"] = normalized
    payload["updated_wall_time"] = time.time()
    payload["updated_monotonic_time"] = time.monotonic()

    return write_run_metadata(payload)


def read_run_status() -> str | None:
    """Return lifecycle status from metadata."""
    return run_status(read_run_metadata())


def run_id(payload: dict[str, Any] | None) -> str | None:
    """Return run_id from run metadata."""
    if not payload:
        return None

    value = payload.get("run_id")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def boot_id(payload: dict[str, Any] | None) -> str | None:
    """Return boot_id from run metadata."""
    if not payload:
        return None

    value = payload.get("boot_id")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def wall_time(payload: dict[str, Any] | None) -> float | None:
    """Return wall_time from run metadata."""
    if not payload:
        return None

    value = payload.get("wall_time")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def monotonic_time(payload: dict[str, Any] | None) -> float | None:
    """Return monotonic_time from run metadata."""
    if not payload:
        return None

    value = payload.get("monotonic_time")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def updated_wall_time(payload: dict[str, Any] | None) -> float | None:
    """Return updated_wall_time from run metadata."""
    if not payload:
        return None

    value = payload.get("updated_wall_time")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def updated_monotonic_time(payload: dict[str, Any] | None) -> float | None:
    """Return updated_monotonic_time from run metadata."""
    if not payload:
        return None

    value = payload.get("updated_monotonic_time")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def run_status(payload: dict[str, Any] | None) -> str | None:
    """Return status from run metadata."""
    if not payload:
        return None

    value = payload.get("status")
    if not isinstance(value, str):
        return None

    value = value.strip().lower()
    return value or None


# Canonical coordination only: these lock files carry no runtime truth.
# Order: startup reservation -> brief prestart lifecycle lease -> mutation ->
# StopGate transition. The normal supervisor retains only its lifetime lease.
import threading as _threading
_mutation_local = _threading.local()
_mutation_threads = _threading.RLock()
_mutation_process = os.getpid()
_mutation_fd = None


@contextmanager
def runtime_mutation(*, blocking=True):
    """Short cross-process writer exclusion; never the supervisor lifetime lock."""
    global _mutation_local, _mutation_threads, _mutation_process, _mutation_fd
    if _mutation_process != os.getpid():
        if _mutation_fd is not None:
            os.close(_mutation_fd)  # close child copy, never unlock parent's lease
        _mutation_fd = None
        _mutation_local = _threading.local()
        _mutation_threads = _threading.RLock()
        _mutation_process = os.getpid()
    if not _mutation_threads.acquire(blocking=blocking):
        raise BlockingIOError("runtime mutation thread already active")
    try:
        if getattr(_mutation_local, "depth", 0):
            _mutation_local.depth += 1
            try:
                yield
            finally:
                _mutation_local.depth -= 1
            return
        RUNTIME_STATE_DIR.mkdir(parents=True, exist_ok=True)
        path = RUNTIME_STATE_DIR / "runtime_mutation.lock"
        fd = _coordination_fd(path)
        _mutation_fd = fd
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
            _mutation_local.depth = 1
            try:
                yield
            finally:
                _mutation_local.depth = 0
        finally:
            _mutation_fd = None
            os.close(fd)
    finally:
        _mutation_threads.release()


@contextmanager
def startup_reservation():
    """Serialize WORK/ctl startup, borrowing only a verified inherited lock FD."""
    RUNTIME_STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNTIME_STATE_DIR / "startup_reservation.lock"
    inherited = os.environ.get("MAKSIMAR_STARTUP_FD")
    borrowed = inherited is not None
    if borrowed:
        fd = int(inherited)
        if fd < 3:
            raise RuntimeError("invalid startup reservation descriptor")
        identity = os.fstat(fd)
        current = os.stat(path, follow_symlinks=False)
        if (identity.st_dev, identity.st_ino) != (current.st_dev, current.st_ino):
            raise RuntimeError("startup reservation descriptor does not match canonical inode")
    else:
        fd = _coordination_fd(path)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        # A borrowed descriptor belongs to the outer WORK shell; never unlock it.
        if not borrowed:
            os.close(fd)


@contextmanager
def prestart_mutation():
    """Non-writer prestart scope; never assigns run identity or writer authority."""
    if _writer_pid is not None:
        raise RuntimeError("prestart reconciliation cannot run inside a supervisor writer")
    with startup_reservation():
        lease_path = RUNTIME_STATE_DIR / "run_lifecycle.lock"
        fd = _coordination_fd(lease_path)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with runtime_mutation(blocking=False):
                yield
        finally:
            os.close(fd)


def _coordination_fd(path):
    import stat
    parent = path.parent.lstat()
    if not stat.S_ISDIR(parent.st_mode) or parent.st_uid != os.getuid() or parent.st_mode & 0o022:
        raise RuntimeError("canonical coordination directory is unsafe")
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600)
    try:
        opened, current = os.fstat(fd), os.stat(path, follow_symlinks=False)
        if (not stat.S_ISREG(opened.st_mode) or opened.st_uid != os.getuid()
                or (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino)):
            raise RuntimeError("canonical coordination inode is unsafe or replaced")
        return fd
    except BaseException:
        os.close(fd)
        raise
