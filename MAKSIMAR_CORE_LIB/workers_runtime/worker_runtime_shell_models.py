from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkerRuntimeShellContract:
    """Final shell contract for workers runtime / health layer."""

    shell_id: str
    total_health_entries: int
    total_load_entries: int
