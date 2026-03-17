#!/usr/bin/env python3
"""Canonical runtime paths for MAKSIMAR foundation services."""

from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "MAKSIMAR_PLATFORM"

CORE_ROOT_DIR = ROOT / "CORE_ROOT"
SUPERVISOR_DIR = ROOT / "SUPERVISOR"
CONTROL_PLANE_DIR = ROOT / "CONTROL_PLANE"

RUNTIME_DIR = ROOT / "RUNTIME"
RUNTIME_STATE_DIR = RUNTIME_DIR / "state"
RUNTIME_PIDS_DIR = RUNTIME_DIR / "pids"

LOGS_DIR = ROOT / "logs"

RUNTIME_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "heartbeat_state.json"
GUARD_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "guard_heartbeat_state.json"
CORE_GUARD_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "core_guard_heartbeat_state.json"
KERNEL_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "kernel_heartbeat_state.json"

RUN_METADATA_FILE = RUNTIME_STATE_DIR / "run_metadata.json"
INCIDENT_SNAPSHOT_FILE = RUNTIME_STATE_DIR / "last_incident_snapshot.json"
INCIDENT_HISTORY_FILE = RUNTIME_STATE_DIR / "incident_history.jsonl"
DIAGNOSTICS_DB_FILE = RUNTIME_STATE_DIR / "diagnostics_db.json"

SYSTEM_LOG_FILE = LOGS_DIR / "system.log"
RUNTIME_LOG_FILE = LOGS_DIR / "runtime.log"
GUARD_LOG_FILE = LOGS_DIR / "guard.log"
CORE_GUARD_LOG_FILE = LOGS_DIR / "core_guard.log"
KERNEL_GUARD_LOG_FILE = LOGS_DIR / "kernel_guard.log"

STOP_GATE_SCRIPT = CORE_ROOT_DIR / "stop_gate.py"
STOP_GATE_WATCHER_SCRIPT = CORE_ROOT_DIR / "stop_gate_watcher.py"
CORE_GUARD_SCRIPT = CORE_ROOT_DIR / "core_guard.py"
KERNEL_WATCHDOG_SCRIPT = CORE_ROOT_DIR / "kernel_watchdog.py"
PROCESS_SUPERVISOR_SCRIPT = SUPERVISOR_DIR / "process_supervisor.py"

RUNTIME_SESSION_NAME = "maksimar"
GUARD_SESSION_NAME = "maksimar_guard"
CORE_GUARD_SESSION_NAME = "maksimar_core_guard"
KERNEL_GUARD_SESSION_NAME = "maksimar_kernel_guard"

CONTROL_PLANE_HOST = "127.0.0.1"
CONTROL_PLANE_PORT = 8000

VENV_PYTHON = ROOT / "venv" / "bin" / "python"


def ensure_runtime_layout() -> None:
    """Ensure runtime directories exist."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_STATE_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_PIDS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
