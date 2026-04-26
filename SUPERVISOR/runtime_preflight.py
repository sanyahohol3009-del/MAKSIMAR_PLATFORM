#!/usr/bin/env python3
"""Runtime preflight validation before supervisor startup."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import socket
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from CORE_ROOT.runtime_paths import (
    CONTROL_PLANE_HOST,
    CONTROL_PLANE_PORT,
    CORE_GUARD_HEARTBEAT_FILE,
    CORE_GUARD_SESSION_NAME,
    GUARD_HEARTBEAT_FILE,
    GUARD_SESSION_NAME,
    KERNEL_HEARTBEAT_FILE,
    KERNEL_GUARD_SESSION_NAME,
    LOGS_DIR,
    PREFLIGHT_LOG_FILE,
    PREFLIGHT_RESULT_FILE,
    REQUIRED_RUNTIME_IMPORTS,
    ROOT,
    RUNTIME_HEARTBEAT_FILE,
    RUNTIME_PIDS_DIR,
    RUNTIME_SESSION_NAME,
    RUNTIME_STATE_DIR,
    ensure_runtime_layout,
    resolve_canonical_python,
)


@dataclass(slots=True)
class PreflightReport:
    """Structured preflight result."""

    preflight_id: str
    checked_at: str
    ok: bool
    stale_tmux_found: bool
    stale_pid_found: bool
    stale_heartbeat_found: bool
    port_conflict_found: bool
    previous_crash_found: bool
    details: dict[str, Any] = field(default_factory=dict)


def utc_now_iso() -> str:
    """Return canonical UTC timestamp."""
    return datetime.now(tz=UTC).isoformat(timespec="seconds")


def build_preflight_id() -> str:
    """Build stable preflight identifier."""
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"preflight-{timestamp}"


def log(message: str) -> None:
    """Append a message to preflight log and stdout."""
    ensure_runtime_layout()
    timestamp = utc_now_iso()
    line = f"[PREFLIGHT] {timestamp} {message}"
    print(line, flush=True)
    with PREFLIGHT_LOG_FILE.open("a", encoding="utf-8") as file_obj:
        file_obj.write(line + "\n")


def write_report(report: PreflightReport) -> None:
    """Write preflight report to JSON."""
    ensure_runtime_layout()
    temp_path = PREFLIGHT_RESULT_FILE.with_suffix(".json.tmp")
    payload = asdict(report)
    with temp_path.open("w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False, indent=2, sort_keys=True)
        file_obj.flush()
        os.fsync(file_obj.fileno())
    temp_path.replace(PREFLIGHT_RESULT_FILE)


def check_python(details: dict[str, Any]) -> bool:
    """Validate canonical python interpreter."""
    try:
        python_path = resolve_canonical_python()
    except FileNotFoundError as exc:
        details["python"] = {"ok": False, "error": str(exc)}
        return False

    details["python"] = {
        "ok": True,
        "path": str(python_path),
    }
    return True


def check_runtime_directories(details: dict[str, Any]) -> bool:
    """Validate required runtime directories."""
    ensure_runtime_layout()
    checks = {
        "root_exists": ROOT.exists(),
        "logs_dir_exists": LOGS_DIR.exists(),
        "runtime_state_dir_exists": RUNTIME_STATE_DIR.exists(),
        "runtime_pids_dir_exists": RUNTIME_PIDS_DIR.exists(),
    }
    ok = all(checks.values())
    details["directories"] = {"ok": ok, **checks}
    return ok


def check_imports(details: dict[str, Any]) -> bool:
    """Validate required runtime imports."""
    failed: list[str] = []
    imported: list[str] = []

    for module_name in REQUIRED_RUNTIME_IMPORTS:
        try:
            importlib.import_module(module_name)
            imported.append(module_name)
        except Exception:
            failed.append(module_name)

    ok = not failed
    details["imports"] = {
        "ok": ok,
        "imported": imported,
        "failed": failed,
    }
    return ok


def check_tmux(details: dict[str, Any]) -> tuple[bool, bool]:
    """Validate tmux and detect stale sessions."""
    try:
        result = subprocess.run(
            ["tmux", "ls"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2.0,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        details["tmux"] = {
            "ok": False,
            "error": "tmux not available",
            "stale_sessions": [],
        }
        return False, False

    stale_sessions: list[str] = []
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    known_sessions = (
        RUNTIME_SESSION_NAME,
        GUARD_SESSION_NAME,
        CORE_GUARD_SESSION_NAME,
        KERNEL_GUARD_SESSION_NAME,
    )
    for line in output_lines:
        session_name = line.split(":", 1)[0]
        if session_name in known_sessions:
            stale_sessions.append(session_name)

    ok = result.returncode in (0, 1)
    details["tmux"] = {
        "ok": ok,
        "sessions": output_lines,
        "stale_sessions": stale_sessions,
    }
    return ok, bool(stale_sessions)


def check_stale_heartbeats(details: dict[str, Any]) -> bool:
    """Detect stale heartbeat artifacts."""
    stale_files: list[str] = []
    for path in (
        RUNTIME_HEARTBEAT_FILE,
        GUARD_HEARTBEAT_FILE,
        CORE_GUARD_HEARTBEAT_FILE,
        KERNEL_HEARTBEAT_FILE,
    ):
        if path.exists():
            stale_files.append(str(path))

    details["heartbeat"] = {
        "ok": True,
        "stale_files": stale_files,
    }
    return bool(stale_files)


def check_stale_pids(details: dict[str, Any]) -> bool:
    """Detect stale PID files."""
    stale_pid_files: list[str] = []
    if RUNTIME_PIDS_DIR.exists():
        for path in sorted(RUNTIME_PIDS_DIR.glob("*.pid")):
            stale_pid_files.append(str(path))

    details["pids"] = {
        "ok": True,
        "stale_pid_files": stale_pid_files,
    }
    return bool(stale_pid_files)


def check_port_conflict(details: dict[str, Any]) -> bool:
    """Check whether runtime port is already occupied."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        result = sock.connect_ex((CONTROL_PLANE_HOST, CONTROL_PLANE_PORT))
    finally:
        sock.close()

    conflict = result == 0
    details["port"] = {
        "ok": not conflict,
        "host": CONTROL_PLANE_HOST,
        "port": CONTROL_PLANE_PORT,
        "port_conflict_found": conflict,
    }
    return conflict


def check_previous_crash(details: dict[str, Any]) -> bool:
    """Infer previous abnormal stop from leftovers."""
    evidence: list[str] = []

    if PREFLIGHT_RESULT_FILE.exists():
        evidence.append(str(PREFLIGHT_RESULT_FILE))
    if any(path.exists() for path in (
        RUNTIME_HEARTBEAT_FILE,
        GUARD_HEARTBEAT_FILE,
        CORE_GUARD_HEARTBEAT_FILE,
        KERNEL_HEARTBEAT_FILE,
    )):
        evidence.append("leftover_heartbeat_state")

    previous_crash_found = bool(evidence)
    details["previous_crash"] = {
        "ok": True,
        "evidence": evidence,
    }
    return previous_crash_found


def run_preflight() -> PreflightReport:
    """Run all preflight checks."""
    details: dict[str, Any] = {}

    python_ok = check_python(details)
    dirs_ok = check_runtime_directories(details)
    imports_ok = check_imports(details)
    tmux_ok, stale_tmux_found = check_tmux(details)

    stale_heartbeat_found = check_stale_heartbeats(details)
    stale_pid_found = check_stale_pids(details)
    port_conflict_found = check_port_conflict(details)
    previous_crash_found = check_previous_crash(details)

    ok = all((python_ok, dirs_ok, imports_ok, tmux_ok)) and not port_conflict_found

    return PreflightReport(
        preflight_id=build_preflight_id(),
        checked_at=utc_now_iso(),
        ok=ok,
        stale_tmux_found=stale_tmux_found,
        stale_pid_found=stale_pid_found,
        stale_heartbeat_found=stale_heartbeat_found,
        port_conflict_found=port_conflict_found,
        previous_crash_found=previous_crash_found,
        details=details,
    )


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run runtime preflight validation.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if stale runtime artifacts are present.",
    )
    args = parser.parse_args()

    ensure_runtime_layout()
    report = run_preflight()
    write_report(report)

    log(f"preflight ok={report.ok}")
    log(
        "flags: "
        f"stale_tmux={report.stale_tmux_found}, "
        f"stale_pid={report.stale_pid_found}, "
        f"stale_heartbeat={report.stale_heartbeat_found}, "
        f"port_conflict={report.port_conflict_found}, "
        f"previous_crash={report.previous_crash_found}"
    )

    if not report.ok:
        sys.exit(1)

    if args.strict and (
        report.stale_tmux_found
        or report.stale_pid_found
        or report.stale_heartbeat_found
    ):
        sys.exit(2)


if __name__ == "__main__":
    main()
