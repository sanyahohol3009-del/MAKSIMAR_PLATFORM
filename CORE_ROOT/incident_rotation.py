#!/usr/bin/env python3
"""Incident rotation helpers for MAKSIMAR safety foundation."""

from __future__ import annotations

import json
from typing import Any

from CORE_ROOT.runtime_paths import INCIDENT_HISTORY_FILE, ensure_runtime_layout


INCIDENT_HISTORY_MAX_RECORDS = 200


def read_incident_history_lines() -> list[str]:
    """Read non-empty incident history lines."""
    ensure_runtime_layout()

    if not INCIDENT_HISTORY_FILE.exists():
        return []

    with INCIDENT_HISTORY_FILE.open("r", encoding="utf-8") as file_obj:
        return [line.rstrip("\n") for line in file_obj if line.strip()]


def read_incident_history_records() -> list[dict[str, Any]]:
    """Read and parse incident history records."""
    records: list[dict[str, Any]] = []

    for line in read_incident_history_lines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue

        if isinstance(payload, dict):
            records.append(payload)

    return records


def write_incident_history_records(records: list[dict[str, Any]]) -> None:
    """Rewrite incident history file from canonical records."""
    ensure_runtime_layout()

    normalized_lines: list[str] = []

    for payload in records:
        if not isinstance(payload, dict):
            continue
        normalized_lines.append(json.dumps(payload, ensure_ascii=False))

    content = "\n".join(normalized_lines)
    if content:
        content += "\n"

    with INCIDENT_HISTORY_FILE.open("w", encoding="utf-8") as file_obj:
        file_obj.write(content)


def rotate_incident_history(
    max_records: int = INCIDENT_HISTORY_MAX_RECORDS,
) -> list[dict[str, Any]]:
    """Trim incident history to the newest max_records entries."""
    if not isinstance(max_records, int):
        raise ValueError("max_records must be an int")

    if max_records <= 0:
        raise ValueError("max_records must be greater than zero")

    records = read_incident_history_records()

    if len(records) <= max_records:
        return records

    trimmed = records[-max_records:]
    write_incident_history_records(trimmed)
    return trimmed


def incident_history_count() -> int:
    """Return parsed incident history record count."""
    return len(read_incident_history_records())
