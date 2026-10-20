#!/usr/bin/env python3
"""Heartbeat helpers for MAKSIMAR foundation services."""

from __future__ import annotations

import json
import os
import tempfile
import time
from typing import Any

from CORE_ROOT.run_context import boot_id as metadata_boot_id
from CORE_ROOT.run_context import monotonic_time as metadata_monotonic_time
from CORE_ROOT.run_context import read_run_metadata
from CORE_ROOT.run_context import run_id as metadata_run_id
from pathlib import Path
from CORE_ROOT.runtime_paths import ROOT, ensure_runtime_layout

HEARTBEAT_SCHEMA_VERSION = 1


def atomic_write_json(path: os.PathLike[str] | str, payload: dict[str, Any]) -> None:
    """Atomically write JSON payload to disk.

    Args:
        path: Destination file path.
        payload: JSON-serializable payload.
    """
    from CORE_ROOT.run_context import runtime_mutation
    with runtime_mutation():
        ensure_runtime_layout()

        path_str = os.fspath(path)
        target_dir = os.path.dirname(path_str) or "."

        fd, temp_path = tempfile.mkstemp(prefix=".tmp_", suffix=".json", dir=target_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file_obj:
                json.dump(payload, file_obj, ensure_ascii=False, separators=(",", ":"))
                file_obj.flush()
                os.fsync(file_obj.fileno())

            os.replace(temp_path, path_str)
        except Exception:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise


def safe_read_json(path: os.PathLike[str] | str) -> dict[str, Any] | None:
    """Safely read JSON payload from disk.

    Args:
        path: Source file path.

    Returns:
        Parsed dict or None if file is absent/invalid.
    """
    path_str = os.fspath(path)

    if not os.path.exists(path_str):
        return None

    try:
        with open(path_str, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    return payload


def build_heartbeat(source: str, status: str = "alive") -> dict[str, Any]:
    """Build canonical heartbeat payload.

    Args:
        source: Heartbeat source name.
        status: Heartbeat status value.

    Returns:
        Canonical heartbeat payload.
    """
    run_meta = read_run_metadata()

    payload: dict[str, Any] = {
        "schema_version": HEARTBEAT_SCHEMA_VERSION,
        "source": source,
        "status": status,
        "ts": time.time(),
        "monotonic_ts": time.monotonic(),
        "pid": os.getpid(),
        "process_start_ticks": _process_start_ticks(Path("/proc") / str(os.getpid())),
    }

    run_id_value = metadata_run_id(run_meta)
    if run_id_value is not None:
        payload["run_id"] = run_id_value

    boot_id_value = metadata_boot_id(run_meta)
    if boot_id_value is not None:
        payload["boot_id"] = boot_id_value

    run_monotonic_value = metadata_monotonic_time(run_meta)
    if run_monotonic_value is not None:
        payload["run_monotonic_time"] = run_monotonic_value

    return payload


def heartbeat_source(payload: dict[str, Any] | None) -> str | None:
    """Return heartbeat source."""
    if not payload:
        return None

    value = payload.get("source")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def heartbeat_status(payload: dict[str, Any] | None) -> str | None:
    """Return heartbeat status."""
    if not payload:
        return None

    value = payload.get("status")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def heartbeat_wall_time(payload: dict[str, Any] | None) -> float | None:
    """Return heartbeat wall timestamp."""
    if not payload:
        return None

    value = payload.get("ts")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def heartbeat_monotonic_time(payload: dict[str, Any] | None) -> float | None:
    """Return heartbeat monotonic timestamp."""
    if not payload:
        return None

    value = payload.get("monotonic_ts")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def heartbeat_age_seconds(payload: dict[str, Any] | None) -> float | None:
    """Return heartbeat age in seconds using monotonic time when available."""
    monotonic_value = heartbeat_monotonic_time(payload)
    if monotonic_value is not None:
        age = time.monotonic() - monotonic_value
        return max(age, 0.0)

    wall_value = heartbeat_wall_time(payload)
    if wall_value is None:
        return None

    age = time.time() - wall_value
    return max(age, 0.0)


def heartbeat_run_id(payload: dict[str, Any] | None) -> str | None:
    """Return heartbeat run_id."""
    if not payload:
        return None

    value = payload.get("run_id")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def heartbeat_boot_id(payload: dict[str, Any] | None) -> str | None:
    """Return heartbeat boot_id."""
    if not payload:
        return None

    value = payload.get("boot_id")
    if not isinstance(value, str):
        return None

    value = value.strip()
    return value or None


def heartbeat_run_monotonic_time(payload: dict[str, Any] | None) -> float | None:
    """Return run monotonic start time embedded into heartbeat."""
    if not payload:
        return None

    value = payload.get("run_monotonic_time")
    if not isinstance(value, (int, float)):
        return None

    return float(value)


def _process_start_ticks(proc: Path) -> str | None:
    try:
        # comm can contain spaces/parentheses; fields after the final ')' start
        # at stat field 3, so starttime (22) is offset 19.
        return proc.joinpath("stat").read_text().rsplit(")", 1)[1].split()[19]
    except (OSError, IndexError):
        return None


def heartbeat_process_alive(payload: dict[str, Any], expected_module: str,
                            *, proc_root: Path = Path("/proc")) -> bool:
    """Read-only identity check for bounded peer resynchronization, not authority."""
    pid = payload.get("pid")
    if type(pid) is not int or pid <= 0 or not payload.get("process_start_ticks"):
        return False
    proc = proc_root / str(pid)
    try:
        argv = proc.joinpath("cmdline").read_bytes().split(b"\0")
        module = expected_module.encode()
        return (len(argv) >= 3 and argv[1:3] == [b"-m", module]
            and str(proc.joinpath("cwd").resolve()) == str(ROOT)
            and _process_start_ticks(proc) == payload["process_start_ticks"])
    except OSError:
        return False


def find_owned_module_process_pids(expected_module: str, *, pidfile: Path | None = None,
                                   proc_root: Path = Path("/proc")) -> tuple[int, ...] | None:
    """Read-only owned candidates; None means inspection failed, never absence."""
    try:
        candidates = {int(p.name) for p in proc_root.iterdir() if p.name.isdecimal()}
    except OSError:
        return None
    if pidfile is not None:
        try:
            hinted_pid = int(pidfile.read_text(encoding="utf-8").strip())
            if hinted_pid > 0:
                candidates.add(hinted_pid)
        except (OSError, ValueError):
            pass
    owned = []
    for pid in sorted(candidates):
        proc = proc_root / str(pid)
        try:
            argv = proc.joinpath("cmdline").read_bytes().split(b"\0")
            if argv[1:3] != [b"-m", expected_module.encode()]:
                continue
            if str(proc.joinpath("cwd").resolve(strict=True)) != str(ROOT):
                continue
            start_ticks = _process_start_ticks(proc)
            if not start_ticks:
                if proc.exists():
                    return None
                continue
            if heartbeat_process_alive({"pid": pid, "process_start_ticks": start_ticks},
                                       expected_module, proc_root=proc_root):
                owned.append(pid)
            elif proc.exists():
                return None  # identity changed while collecting; not absence
        except (OSError, UnicodeError):
            if proc.exists():
                return None
    return tuple(owned)


def find_owned_module_process_pid(expected_module: str, *, pidfile: Path | None = None,
                                  proc_root: Path = Path("/proc")) -> int | None:
    """Preserve the existing exact-one PID discovery contract for CLI callers."""
    owned = find_owned_module_process_pids(expected_module, pidfile=pidfile, proc_root=proc_root)
    return owned[0] if owned is not None and len(owned) == 1 else None


def write_owned_pid_hint(path, module):
    """Publish a verified single owner hint without changing an identical hint."""
    from CORE_ROOT.run_context import runtime_mutation
    with runtime_mutation():
        pids = find_owned_module_process_pids(module)
        if pids is None or len(pids) > 1:
            raise RuntimeError("PID hint identity unknown or ambiguous")
        if not pids:
            return
        path = Path(path)
        if path.is_symlink():
            raise RuntimeError("PID hint symlink refused")
        text = str(pids[0]) + "\n"
        if path.is_file() and path.read_text().strip() == str(pids[0]):
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".pid_", dir=path.parent)
        try:
            with os.fdopen(fd, "w") as handle:
                handle.write(text); handle.flush(); os.fsync(handle.fileno())
            os.replace(temporary, path)
        except BaseException:
            if os.path.exists(temporary):
                os.unlink(temporary)
            raise


def remove_stopped_pid_hint(path, *, proc_root=Path("/proc")):
    """Remove only an absent process hint; unknown/live/foreign hints are retained."""
    from CORE_ROOT.run_context import runtime_mutation
    with runtime_mutation():
        path = Path(path)
        if not path.exists():
            return
        if path.is_symlink():
            raise RuntimeError("PID hint symlink refused")
        pid = int(path.read_text().strip())
        if pid <= 0 or (proc_root / str(pid)).exists():
            raise RuntimeError("PID hint process not proven absent")
        path.unlink()

def write_guard_heartbeat(path, source, status="alive", *, expected_run=None):
    """Use the existing atomic writer with a pinned guard run and terminal readback."""
    import math
    from CORE_ROOT import run_context
    with run_context.runtime_mutation():
        meta = run_context.read_run_metadata()
        if expected_run is not None and (
                not expected_run or not isinstance(meta, dict)
                or type(meta.get("schema_version")) is not int
                or meta["schema_version"] != run_context.RUN_METADATA_SCHEMA_VERSION
                or not all(isinstance(meta.get(k), str) and bool(meta[k].strip())
                           for k in ("run_id", "boot_id"))
                or not all(type(meta.get(k)) in (int, float) and math.isfinite(meta[k])
                           and meta[k] >= 0 for k in ("wall_time", "monotonic_time"))
                or run_context._identity(meta) != expected_run):
            raise RuntimeError("guard heartbeat run identity changed or missing")
        payload = build_heartbeat(source=source, status=status)
        previous = safe_read_json(path)
        if (status == "alive" and previous and previous.get("status") == "stopped"
                and all(previous.get(k) == payload.get(k) for k in
                        ("source", "pid", "process_start_ticks", "run_id", "boot_id", "run_monotonic_time"))):
            raise RuntimeError("guard terminal heartbeat cannot return to alive")
        atomic_write_json(path, payload)
        if safe_read_json(path) != payload:
            raise RuntimeError("guard heartbeat readback failed")
        if status == "stopped":
            directory = os.open(Path(path).parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)


def stop_owned_guard_process(module, source, pidfile, heartbeat_file, *, session_id=""):
    """Complete the existing guard stop contract; never manufacture a receipt.

    Same one-second grace as the existing controllers, pinned with pidfd.
    Startup reservation serializes duplicate stop/start requests. The mutation
    lock is deliberately not held while waiting for the guard's own writer.
    """
    import math
    import select
    import signal
    from CORE_ROOT import run_context
    pidfile, heartbeat_file = Path(pidfile), Path(heartbeat_file)

    def finite_number(value):
        return type(value) in (int, float) and math.isfinite(value) and value >= 0

    def receipt_matches(receipt, meta, *, pid=None, ticks=None):
        return bool(isinstance(receipt, dict) and isinstance(meta, dict)
            and type(meta.get("schema_version")) is int
            and meta["schema_version"] == run_context.RUN_METADATA_SCHEMA_VERSION
            and meta.get("status") in run_context.ALLOWED_RUN_STATUSES
            and finite_number(meta.get("monotonic_time"))
            and finite_number(meta.get("wall_time"))
            and finite_number(receipt.get("monotonic_ts"))
            and finite_number(receipt.get("ts"))
            and type(receipt.get("schema_version")) is int
            and receipt["schema_version"] == HEARTBEAT_SCHEMA_VERSION
            and receipt.get("source") == source
            and type(receipt.get("pid")) is int and receipt["pid"] > 0
            and isinstance(receipt.get("process_start_ticks"), str)
            and receipt["process_start_ticks"].isdecimal()
            and isinstance(meta.get("run_id"), str) and bool(meta["run_id"])
            and isinstance(meta.get("boot_id"), str) and bool(meta["boot_id"])
            and receipt.get("run_id") == meta["run_id"]
            and receipt.get("boot_id") == meta["boot_id"]
            and receipt.get("run_monotonic_time") == meta.get("monotonic_time")
            and (pid is None or receipt["pid"] == pid)
            and (ticks is None or receipt["process_start_ticks"] == ticks))

    with run_context.startup_reservation():
        if pidfile.is_symlink() or heartbeat_file.is_symlink():
            raise RuntimeError("guard stop refused: symlink state path")
        owned = find_owned_module_process_pids(module, pidfile=pidfile)
        if owned is None or len(owned) > 1:
            raise RuntimeError("guard stop refused: identity unknown or ambiguous")
        meta = run_context.read_run_metadata()
        before = safe_read_json(heartbeat_file)
        if not owned:
            if session_id:
                raise RuntimeError("guard stop refused: session has no proven process owner")
            if (not receipt_matches(before, meta) or before.get("status") != "stopped"
                    or (Path("/proc") / str(before["pid"])).exists()):
                raise RuntimeError("guard stop unproven: no verified owner or terminal receipt")
            if pidfile.exists():
                if pidfile.read_text().strip() != str(before["pid"]):
                    raise RuntimeError("guard PID hint mismatches terminal receipt")
                remove_stopped_pid_hint(pidfile)
            return

        pid = owned[0]
        ticks = _process_start_ticks(Path("/proc") / str(pid))
        if not receipt_matches(before, meta, pid=pid, ticks=ticks):
            raise RuntimeError("guard stop refused: heartbeat/run identity mismatch")
        fd = os.pidfd_open(pid)
        try:
            if not heartbeat_process_alive(before, module):
                raise RuntimeError("guard stop refused: identity changed before signal")
            started = time.monotonic()
            signal.pidfd_send_signal(fd, signal.SIGTERM)
            ready, _, _ = select.select([fd], [], [], 1.0)
            if not ready:
                signal.pidfd_send_signal(fd, signal.SIGKILL)
                raise RuntimeError("guard stop forced; terminal lifecycle not proven")
            # A dead but not yet reaped pipeline child must not be a live PID hint.
            while (Path("/proc") / str(pid)).exists() and time.monotonic() - started < 1.0:
                time.sleep(0.01)
            after = safe_read_json(heartbeat_file)
            if (run_context._identity(run_context.read_run_metadata() or {})
                    != run_context._identity(meta or {})
                    or not receipt_matches(after, meta, pid=pid, ticks=ticks)
                    or after.get("status") != "stopped"
                    or not isinstance(after.get("monotonic_ts"), (int, float))
                    or after["monotonic_ts"] < started
                    or (Path("/proc") / str(pid)).exists()):
                raise RuntimeError("guard stop incomplete: terminal receipt/exit not proven")
            if pidfile.exists():
                if pidfile.read_text().strip() != str(pid):
                    raise RuntimeError("guard PID hint changed during stop")
                remove_stopped_pid_hint(pidfile)
        finally:
            os.close(fd)
