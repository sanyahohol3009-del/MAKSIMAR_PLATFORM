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
from CORE_ROOT.runtime_paths import ensure_runtime_layout


HEARTBEAT_SCHEMA_VERSION = 1


def atomic_write_json(path: os.PathLike[str] | str, payload: dict[str, Any]) -> None:
    """Atomically write JSON payload to disk.

    Args:
        path: Destination file path.
        payload: JSON-serializable payload.
    """
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
