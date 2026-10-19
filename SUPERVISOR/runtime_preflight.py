#!/usr/bin/env python3
"""Runtime preflight validation before supervisor startup."""

from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from CORE_ROOT.heartbeat_io import (
    HEARTBEAT_SCHEMA_VERSION, _process_start_ticks, heartbeat_process_alive,
    heartbeat_source, heartbeat_status, safe_read_json,
)
from CORE_ROOT.run_context import RUN_METADATA_SCHEMA_VERSION, RUN_STATUS_RUNNING
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
    RUN_METADATA_FILE,
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
    already_running_healthy: bool
    details: dict[str, Any] = field(default_factory=dict)


RUNTIME_PID_FILE = ROOT / "RUNTIME" / "runtime.pid"
EXPECTED_SESSIONS = frozenset({
    RUNTIME_SESSION_NAME,
    GUARD_SESSION_NAME,
    CORE_GUARD_SESSION_NAME,
    KERNEL_GUARD_SESSION_NAME,
})
HEARTBEAT_MAX_AGE_SECONDS = 15.0
# Existing heartbeat writers; this observation table owns no lifecycle state.
EXPECTED_HEARTBEATS = {
    "runtime": ("process_supervisor", "SUPERVISOR.process_supervisor"),
    "guard": ("stop_gate_watcher", "CORE_ROOT.stop_gate_watcher"),
    "core_guard": ("core_guard", "CORE_ROOT.core_guard"),
    "kernel_guard": ("kernel_watchdog", "CORE_ROOT.kernel_watchdog"),
}


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


def _finite_number(value: Any) -> bool:
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _heartbeat_status(path: Path, *, now: float | None = None,
                      monotonic_now: float | None = None,
                      expected_module: str | None = None,
                      proc_root: Path = Path("/proc")) -> dict[str, Any]:
    """Retain writer facts and read-only process proof, never freshness alone."""
    exists = path.exists()
    try:
        payload = safe_read_json(path)
    except (OSError, UnicodeError):
        payload = None
    if payload is None:
        return {"exists": exists, "fresh": False, "age_seconds": None,
                "error": "invalid heartbeat object" if exists else "missing"}
    wall = time.time() if now is None else now
    mono = time.monotonic() if monotonic_now is None else monotonic_now
    timestamps = (payload.get("ts"), payload.get("monotonic_ts"))
    valid_times = all(_finite_number(v) for v in (*timestamps, wall, mono))
    ages = (wall - timestamps[0], mono - timestamps[1]) if valid_times else ()
    fresh = bool(ages) and all(0 <= age <= HEARTBEAT_MAX_AGE_SECONDS for age in ages)
    identity = _process_identity(payload.get("pid"), proc_root=proc_root)
    try:
        process_verified = bool(expected_module) and heartbeat_process_alive(
            payload, expected_module, proc_root=proc_root)
    except (OSError, UnicodeError):
        process_verified = False
    return {
        **{key: payload.get(key) for key in (
            "schema_version", "source", "status", "ts", "monotonic_ts", "pid",
            "process_start_ticks", "run_id", "boot_id", "run_monotonic_time")},
        "exists": exists, "fresh": fresh,
        "age_seconds": max(ages) if ages else None,
        "identity": identity, "process_verified": process_verified,
        "error": "" if valid_times else "invalid heartbeat timestamps",
    }


def _read_pid_file(path: Path = RUNTIME_PID_FILE) -> tuple[bool, int | None]:
    if not path.exists():
        return False, None
    try:
        value = int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return True, None
    return True, value if value > 0 else None


def _process_identity(pid: int | None, *, proc_root: Path = Path("/proc")) -> dict[str, Any]:
    result = {"pid": pid, "alive": None, "cmdline": "", "argv": [], "cwd": "",
              "process_start_ticks": None, "project_process": False}
    if type(pid) is not int or pid <= 0:
        return {**result, "alive": False}
    proc = proc_root / str(pid)
    if not proc.exists():
        return {**result, "alive": False}
    try:
        start_ticks = _process_start_ticks(proc)
        argv = [v.decode("utf-8", errors="strict") for v in
                proc.joinpath("cmdline").read_bytes().split(b"\0") if v]
        cwd = str(proc.joinpath("cwd").resolve(strict=True))
    except (OSError, UnicodeError):
        return result
    # Use the existing exact module/cwd/start-tick verifier, including a second
    # stat read to reject PID replacement during observation.
    module = argv[2] if len(argv) >= 3 and argv[1] == "-m" else ""
    try:
        verified = bool(start_ticks) and heartbeat_process_alive(
            {"pid": pid, "process_start_ticks": start_ticks}, module, proc_root=proc_root)
    except (OSError, UnicodeError):
        verified = False
    return {**result, "alive": True, "process_verified": verified, "argv": argv, "cmdline": " ".join(argv),
            "cwd": cwd, "process_start_ticks": start_ticks,
            "project_process": verified and (module == "SUPERVISOR.process_supervisor"
                or (module == "uvicorn" and argv[3:4] == ["CONTROL_PLANE.api_server:app"]))}


def _identity_matches(identity: Any, pid: Any, module: str, ticks: Any = None) -> bool:
    if not isinstance(identity, dict) or type(pid) is not int or pid <= 0:
        return False
    argv = identity.get("argv")
    start = identity.get("process_start_ticks")
    return (identity.get("alive") is True and identity.get("process_verified") is True
            and identity.get("pid") == pid
            and identity.get("cwd") == str(ROOT)
            and isinstance(argv, list) and len(argv) >= 3
            and argv[1:3] == ["-m", module]
            and isinstance(start, str) and start.isdecimal()
            and (ticks is None or start == ticks)
            and (module != "uvicorn" or argv[3:4] == ["CONTROL_PLANE.api_server:app"]))


def _runtime_pid_identity(pid: int | None) -> dict[str, Any]:
    identity = _process_identity(pid)
    return {**identity, "matches": _identity_matches(identity, pid, "SUPERVISOR.process_supervisor")}


def _tmux_snapshot() -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            capture_output=True, text=True, check=False, timeout=2.0,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "sessions": [], "error": str(exc)}
    sessions = sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})
    return {"available": result.returncode in (0, 1), "sessions": sessions, "error": "" if result.returncode in (0, 1) else result.stderr.strip(),
            "stderr": result.stderr.strip()}


def _port_snapshot() -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["ss", "-H", "-ltnp", f"sport = :{CONTROL_PLANE_PORT}"],
            capture_output=True, text=True, check=False, timeout=2.0,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"listening": False, "owner_pids": [], "owned_by_project": False,
                "owner_identities": [], "ss_output": "", "error": str(exc)}
    output = result.stdout.strip()
    owner_pids = sorted({int(value) for value in re.findall(r"pid=(\d+)", output)})
    identities = [_process_identity(pid) for pid in owner_pids]
    owned = (result.returncode == 0 and len(identities) == 1
             and _identity_matches(identities[0], owner_pids[0], "uvicorn"))
    return {"listening": bool(output), "owner_pids": owner_pids,
            "owner_identities": identities, "owned_by_project": owned,
            "ss_output": output, "error": "" if result.returncode == 0 else result.stderr or "ss failed"}


def _health_snapshot() -> dict[str, Any]:
    url = f"http://{CONTROL_PLANE_HOST}:{CONTROL_PLANE_PORT}/health"
    try:
        with urllib.request.urlopen(url, timeout=2.0) as response:
            status = int(response.status)
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {"ok": False, "status": None, "url": url, "error": str(exc)}
    return {
        "ok": status == 200 and isinstance(payload, dict) and payload.get("ok") is True,
        "status": status,
        "url": url,
        "error": "",
    }


def classify_runtime_observation(observation: dict[str, Any]) -> dict[str, Any]:
    """Require the complete current-run/process chain before authorizing health."""
    observation = observation if isinstance(observation, dict) else {}
    tmux = observation.get("tmux", {})
    heartbeats = observation.get("heartbeats", {})
    port = observation.get("port", {})
    health = observation.get("health", {})
    identity = observation.get("runtime_pid_identity", {})
    shape_ok = (all(isinstance(v, dict) for v in (tmux, heartbeats, port, health, identity))
                and isinstance(tmux.get("sessions"), list)
                and all(isinstance(v, str) for v in tmux["sessions"])
                and type(tmux.get("available")) is bool
                and type(observation.get("pid_file_exists")) is bool
                and type(port.get("listening")) is bool
                and type(port.get("owned_by_project")) is bool
                and type(health.get("ok")) is bool)
    if not shape_ok:
        return {"classification": "stale_runtime_state", "healthy": False, "clean": False,
                "reasons": ["malformed_runtime_observation"], "expected_sessions_present": False,
                "all_heartbeats_fresh": False, "heartbeat_chain_valid": False,
                "port_owned_by_project": False}
    sessions = set(tmux["sessions"])
    expected_sessions_present = (tmux["available"] is True and not tmux.get("error")
                                 and EXPECTED_SESSIONS.issubset(sessions))
    any_expected_session = bool(EXPECTED_SESSIONS.intersection(sessions))
    pid_file_exists = observation["pid_file_exists"]
    runtime_pid = observation.get("runtime_pid")
    pid_ok = (pid_file_exists and identity.get("matches") is True
              and _identity_matches(identity, runtime_pid, "SUPERVISOR.process_supervisor"))
    complete_peers = set(heartbeats) == set(EXPECTED_HEARTBEATS)
    peers_well_formed = complete_peers and all(
        isinstance(v, dict) and type(v.get("exists")) is bool and type(v.get("fresh")) is bool
        for v in heartbeats.values())
    any_heartbeat = any(not isinstance(v, dict) or v.get("exists") is not False
                        for v in heartbeats.values())
    wall, mono = observation.get("observed_wall_time"), observation.get("observed_monotonic_time")
    clocks_ok = _finite_number(wall) and _finite_number(mono)
    all_heartbeats_fresh = peers_well_formed and clocks_ok and all(
        v["exists"] is True and v["fresh"] is True and not v.get("error")
        and all(_finite_number(v.get(key)) and 0 <= now - v[key] <= HEARTBEAT_MAX_AGE_SECONDS
                for key, now in (("ts", wall), ("monotonic_ts", mono)))
        for v in heartbeats.values())
    meta = observation.get("run_metadata")
    run_ok = (isinstance(meta, dict) and type(meta.get("schema_version")) is int
              and meta["schema_version"] == RUN_METADATA_SCHEMA_VERSION
              and meta.get("status") == RUN_STATUS_RUNNING
              and all(isinstance(meta.get(key), str) and bool(meta[key].strip())
                      for key in ("run_id", "boot_id"))
              and clocks_ok and _finite_number(meta.get("monotonic_time"))
              and 0 <= meta["monotonic_time"] <= mono
              and _finite_number(meta.get("wall_time")) and 0 <= meta["wall_time"] <= wall)
    heartbeat_chain_valid = bool(all_heartbeats_fresh and run_ok and all(
        type(v.get("schema_version")) is int and v["schema_version"] == HEARTBEAT_SCHEMA_VERSION
        and heartbeat_source(v) == source and v.get("source") == source
        and heartbeat_status(v) == "alive" and v.get("status") == "alive"
        and v.get("run_id") == meta["run_id"] and v.get("boot_id") == meta["boot_id"]
        and _finite_number(v.get("run_monotonic_time"))
        and v["run_monotonic_time"] == meta["monotonic_time"]
        and v["monotonic_ts"] >= meta["monotonic_time"]
        and v.get("process_verified") is True
        and _identity_matches(v.get("identity"), v.get("pid"), module, v.get("process_start_ticks"))
        and isinstance(v.get("process_start_ticks"), str)
        and v["process_start_ticks"].isdecimal()
        for scope, (source, module) in EXPECTED_HEARTBEATS.items()
        for v in [heartbeats[scope]])
        and len({v["pid"] for v in heartbeats.values()}) == len(EXPECTED_HEARTBEATS)
        and heartbeats["runtime"]["pid"] == runtime_pid
        and heartbeats["runtime"]["process_start_ticks"] == identity.get("process_start_ticks"))
    port_listening = port["listening"]
    owners, owner_identities = port.get("owner_pids"), port.get("owner_identities")
    port_owned_by_project = bool(port["owned_by_project"] is True and not port.get("error")
        and isinstance(owners, list) and len(owners) == 1
        and isinstance(owner_identities, list) and len(owner_identities) == 1
        and _identity_matches(owner_identities[0], owners[0], "uvicorn"))
    health_ok = health["ok"] is True and health.get("status") == 200 and not health.get("error")
    healthy = bool(all((expected_sessions_present, pid_ok, heartbeat_chain_valid,
                        port_listening, port_owned_by_project, health_ok)))
    evidence_present = any((any_expected_session, pid_file_exists, any_heartbeat,
                            port_listening, health["ok"], identity.get("alive") is True))
    # Old STOP receipts need no live identity; they can prove clean STOP only.
    observation_errors = bool(tmux.get("error") or port.get("error")
        or (not pid_file_exists and (runtime_pid is not None or identity.get("alive") is True))
        or (not port_listening and (port.get("owner_pids") or port.get("owner_identities"))))
    orderly_stopped = bool(peers_well_formed and tmux["available"] and not observation_errors
        and not any_expected_session and not port_listening and not health["ok"]
        and (not pid_file_exists or (type(runtime_pid) is int and runtime_pid > 0
                                    and identity.get("alive") is False))
        and all(heartbeats[scope].get("exists") is True
                and heartbeats[scope].get("status") == "stopped"
                and heartbeats[scope].get("source") == source
                and not heartbeats[scope].get("error")
                for scope, (source, _) in EXPECTED_HEARTBEATS.items()))
    clean = bool(peers_well_formed and tmux["available"] and not observation_errors
                 and (not evidence_present or orderly_stopped))
    reasons: list[str] = []
    if healthy:
        classification = "already_running_healthy"
    elif clean:
        classification = "orderly_stopped" if orderly_stopped else "clean_start"
    else:
        if port_listening and not port_owned_by_project:
            reasons.append("foreign_process_on_control_plane_port")
        if any_expected_session and not pid_ok:
            reasons.append("tmux_present_runtime_process_missing_or_mismatched")
        if pid_file_exists and not pid_ok:
            reasons.append("stale_or_mismatched_runtime_pid")
        if (pid_ok or any_expected_session or port_listening) and not expected_sessions_present:
            reasons.append("expected_tmux_sessions_missing")
        if (pid_ok or any_expected_session) and not port_listening:
            reasons.append("control_plane_port_unavailable")
        if not heartbeat_chain_valid:
            reasons.append("heartbeat_missing_invalid_or_stale")
        if not run_ok:
            reasons.append("current_run_identity_unverified")
        if (pid_ok or any_expected_session or port_listening) and not health_ok:
            reasons.append("health_unavailable")
        if port_listening and port_owned_by_project and not pid_ok:
            reasons.append("control_plane_without_expected_supervisor")
        if observation_errors:
            reasons.append("runtime_observation_unavailable")
        classification = ("port_conflict_foreign_process" if reasons and
                          reasons[0] == "foreign_process_on_control_plane_port" else "stale_runtime_state")
    return {"classification": classification, "healthy": healthy, "clean": clean,
            "reasons": reasons, "expected_sessions_present": expected_sessions_present,
            "all_heartbeats_fresh": bool(all_heartbeats_fresh),
            "heartbeat_chain_valid": heartbeat_chain_valid,
            "port_owned_by_project": port_owned_by_project}


def inspect_runtime_state() -> dict[str, Any]:
    pid_file_exists, runtime_pid = _read_pid_file()
    wall, mono = time.time(), time.monotonic()
    paths = {"runtime": RUNTIME_HEARTBEAT_FILE, "guard": GUARD_HEARTBEAT_FILE,
             "core_guard": CORE_GUARD_HEARTBEAT_FILE, "kernel_guard": KERNEL_HEARTBEAT_FILE}
    try:
        meta = safe_read_json(RUN_METADATA_FILE)
    except (OSError, UnicodeError):
        meta = None
    observation = {
        "observed_wall_time": wall, "observed_monotonic_time": mono,
        "run_metadata": meta,
        "tmux": _tmux_snapshot(), "pid_file_exists": pid_file_exists,
        "runtime_pid": runtime_pid, "runtime_pid_identity": _runtime_pid_identity(runtime_pid),
        "heartbeats": {scope: _heartbeat_status(path, expected_module=EXPECTED_HEARTBEATS[scope][1])
                       for scope, path in paths.items()},
        "port": _port_snapshot(), "health": _health_snapshot(),
    }
    # A lifecycle transition during inspection cannot authorize recovery.
    try:
        metadata_unchanged = safe_read_json(RUN_METADATA_FILE) == meta
    except (OSError, UnicodeError):
        metadata_unchanged = False
    if not metadata_unchanged:
        observation["run_metadata"] = None
    observation["observed_wall_time"] = time.time()
    observation["observed_monotonic_time"] = time.monotonic()
    observation["decision"] = classify_runtime_observation(observation)
    return observation


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
    """Validate tmux; session presence alone is never stale evidence."""
    snapshot = _tmux_snapshot()
    ok = bool(snapshot["available"])
    details["tmux"] = {
        "ok": ok,
        "sessions": snapshot["sessions"],
        "stale_sessions": [],
        "error": snapshot["error"],
    }
    return ok, False


def check_stale_heartbeats(details: dict[str, Any]) -> bool:
    """Detect stale heartbeat artifacts."""
    stale_files: list[str] = []
    for path in (
        RUNTIME_HEARTBEAT_FILE,
        GUARD_HEARTBEAT_FILE,
        CORE_GUARD_HEARTBEAT_FILE,
        KERNEL_HEARTBEAT_FILE,
    ):
        if path.exists() and not _heartbeat_status(path)["fresh"]:
            stale_files.append(str(path))

    details["heartbeat"] = {
        "ok": True,
        "stale_files": stale_files,
    }
    return bool(stale_files)


def check_stale_pids(details: dict[str, Any]) -> bool:
    """Detect stale PID files."""
    stale_pid_files: list[str] = []
    exists, pid = _read_pid_file()
    if exists and not _runtime_pid_identity(pid)["matches"]:
        stale_pid_files.append(str(RUNTIME_PID_FILE))

    details["pids"] = {
        "ok": True,
        "stale_pid_files": stale_pid_files,
    }
    return bool(stale_pid_files)


def check_port_conflict(details: dict[str, Any]) -> bool:
    """Check whether runtime port is already occupied."""
    snapshot = _port_snapshot()
    conflict = bool(snapshot["listening"] and not snapshot["owned_by_project"])
    details["port"] = {
        "ok": not conflict,
        "host": CONTROL_PLANE_HOST,
        "port": CONTROL_PLANE_PORT,
        "port_conflict_found": conflict,
        **snapshot,
    }
    return conflict


def check_previous_crash(details: dict[str, Any]) -> bool:
    """Do not infer a crash from healthy runtime artifacts alone."""
    previous_crash_found = False
    details["previous_crash"] = {
        "ok": True,
        "evidence": [],
        "note": "crash classification requires contradictory runtime evidence",
    }
    return previous_crash_found


def run_preflight() -> PreflightReport:
    """Run all preflight checks."""
    details: dict[str, Any] = {}

    python_ok = check_python(details)
    dirs_ok = check_runtime_directories(details)
    imports_ok = check_imports(details)
    runtime_state = inspect_runtime_state()
    decision = runtime_state["decision"]
    reasons = set(decision["reasons"])
    tmux_ok = bool(runtime_state["tmux"]["available"])

    stale_tmux_found = bool(reasons.intersection({
        "tmux_present_runtime_process_missing_or_mismatched",
        "expected_tmux_sessions_missing",
    }))
    stale_pid_found = "stale_or_mismatched_runtime_pid" in reasons
    stale_heartbeat_found = "heartbeat_missing_invalid_or_stale" in reasons
    port_conflict_found = decision["classification"] == "port_conflict_foreign_process"
    previous_crash_found = decision["classification"] == "stale_runtime_state"
    already_running_healthy = bool(decision["healthy"])

    details["tmux"] = runtime_state["tmux"] | {
        "ok": tmux_ok,
        "expected_sessions": sorted(EXPECTED_SESSIONS),
        "expected_sessions_present": decision["expected_sessions_present"],
        "stale_sessions": sorted(EXPECTED_SESSIONS.intersection(runtime_state["tmux"]["sessions"]))
        if stale_tmux_found else [],
    }
    details["heartbeat"] = {
        "ok": decision["heartbeat_chain_valid"] or decision["clean"],
        "states": runtime_state["heartbeats"],
        "stale_files": [
            name for name, state in runtime_state["heartbeats"].items()
            if state["exists"] and not state["fresh"]
        ],
    }
    details["pids"] = {
        "ok": not stale_pid_found,
        "runtime_pid_file": str(RUNTIME_PID_FILE),
        "runtime_pid": runtime_state["runtime_pid"],
        "identity": runtime_state["runtime_pid_identity"],
        "stale_pid_files": [str(RUNTIME_PID_FILE)] if stale_pid_found else [],
    }
    details["port"] = {
        "ok": not port_conflict_found,
        "host": CONTROL_PLANE_HOST,
        "port": CONTROL_PLANE_PORT,
        "port_conflict_found": port_conflict_found,
        **runtime_state["port"],
    }
    details["health"] = runtime_state["health"]
    details["runtime_state"] = decision
    details["previous_crash"] = {
        "ok": not previous_crash_found,
        "evidence": list(decision["reasons"]) if previous_crash_found else [],
    }

    ok = all((python_ok, dirs_ok, imports_ok, tmux_ok)) and (
        decision["clean"] or already_running_healthy
    )

    return PreflightReport(
        preflight_id=build_preflight_id(),
        checked_at=utc_now_iso(),
        ok=ok,
        stale_tmux_found=stale_tmux_found,
        stale_pid_found=stale_pid_found,
        stale_heartbeat_found=stale_heartbeat_found,
        port_conflict_found=port_conflict_found,
        previous_crash_found=previous_crash_found,
        already_running_healthy=already_running_healthy,
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
    runtime_state = report.details.get("runtime_state", {})
    log(
        f"runtime_classification={runtime_state.get('classification', 'unknown')} "
        f"reasons={runtime_state.get('reasons', [])}"
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
