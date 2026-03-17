#!/usr/bin/env python3
"""Run context helpers for MAKSIMAR foundation services."""

from _future_ import annotations

import time
import uuid
from typing import Any

from CORE_ROOT.runtime_paths import RUN_METADATA_FILE, ensure_runtime_layout

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

    ensure_runtime_layout()
    atomic_write_json(RUN_METADATA_FILE, payload)
    return payload


def read_run_metadata() -> dict[str, Any] | None:
    """Read run metadata from disk."""
    from CORE_ROOT.heartbeat_io import safe_read_json

    ensure_runtime_layout()
    payload = safe_read_json(RUN_METADATA_FILE)

    if not isinstance(payload, dict):
        return None

    return payload


def initialize_run_metadata(status: str = RUN_STATUS_BOOTING) -> dict[str, Any]:
    """Create and persist fresh run metadata."""
    payload = build_run_metadata(status=status)
    return write_run_metadata(payload)


def set_run_status(status: str) -> dict[str, Any]:
    """Update lifecycle status on existing run metadata."""
    normalized = validate_run_status(status)

    payload = read_run_metadata()
    if payload is None:
        raise RuntimeError("run metadata file is missing")

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
