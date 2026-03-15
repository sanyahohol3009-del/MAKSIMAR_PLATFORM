#!/usr/bin/env python3
"""Incident history log for MAKSIMAR safety foundation."""

from __future__ import annotations

import json
import time
from typing import Any

from CORE_ROOT.runtime_paths import (
    INCIDENT_HISTORY_FILE,
    ensure_runtime_layout,
)

from CORE_ROOT.run_context import read_run_metadata


def write_incident_record(
    reason: str,
    status: str = "crashed",
) -> dict[str, Any]:
    """
    Append incident record to history log.
    """

    ensure_runtime_layout()

    meta = read_run_metadata()

    wall = time.time()
    mono = time.monotonic()

    payload: dict[str, Any] = {
        "timestamp_wall": wall,
        "timestamp_monotonic": mono,
        "reason": reason,
        "status": status,
    }

    if meta:
        payload["run_id"] = meta.get("run_id")
        payload["boot_id"] = meta.get("boot_id")

    with open(INCIDENT_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

    return payload


def read_incident_history() -> list[dict[str, Any]]:
    """
    Read full incident history.
    """

    ensure_runtime_layout()

    if not INCIDENT_HISTORY_FILE.exists():
        return []

    history: list[dict[str, Any]] = []

    with open(INCIDENT_HISTORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                history.append(json.loads(line))
            except Exception:
                continue

    return history
