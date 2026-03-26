from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkerIOEntry:
    """Canonical worker input/output contract entry."""

    worker_id: str
    input_contract: str
    output_contract: str
    artifact_output_supported: bool


@dataclass(frozen=True, slots=True)
class WorkerIOContract:
    """Unified worker input/output contract."""

    total_entries: int
    entries: tuple[WorkerIOEntry, ...]
