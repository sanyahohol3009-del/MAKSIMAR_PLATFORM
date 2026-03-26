from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionRuntimeShellContract:
    """Final shell contract for execution-control runtime layer."""

    shell_id: str
    total_queue_runtime_entries: int
    total_lease_runtime_entries: int
    total_scheduler_runtime_entries: int
    total_admission_runtime_entries: int
    total_degraded_runtime_entries: int
