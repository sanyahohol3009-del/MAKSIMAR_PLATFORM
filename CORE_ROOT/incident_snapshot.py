#!/usr/bin/env python3
"""
Incident snapshot writer for MAKSIMAR safety foundation.
Creates immutable diagnostic snapshots on failures.
"""

from __future__ import annotations

import time
from typing import Any

from CORE_ROOT.runtime_paths import (
    INCIDENT_SNAPSHOT_FILE,
    ensure_runtime_layout,
)

from CORE_ROOT.heartbeat_io import atomic_write_json
from CORE_ROOT.run_context import read_run_metadata


SNAPSHOT_SCHEMA_VERSION = 1


def build_incident_snapshot(
    reason: str,
    status: str = "crashed",
) -> dict[str, Any]:
    """
    Build a diagnostic snapshot payload.
    """

    meta = read_run_metadata()

    wall = time.time()
    mono = time.monotonic()

    payload: dict[str, Any] = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "timestamp_wall": wall,
        "timestamp_monotonic": mono,
        "reason": reason,
        "status": status,
    }

    if meta:
        payload["run_id"] = meta.get("run_id")
        payload["boot_id"] = meta.get("boot_id")

    return payload


def write_incident_snapshot(
    reason: str,
    status: str = "crashed",
) -> dict[str, Any]:
    """
    Persist snapshot atomically.
    """

    ensure_runtime_layout()

    payload = build_incident_snapshot(
        reason=reason,
        status=status,
    )

    atomic_write_json(INCIDENT_SNAPSHOT_FILE, payload)

    return payload
