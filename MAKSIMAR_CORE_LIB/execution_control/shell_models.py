from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionControlShellContract:
    """Final shell contract for execution control layer."""

    shell_id: str
    total_tasks: int
    total_queues: int
    total_leases: int
    total_schedulers: int
    total_admission_decisions: int
    total_routes: int
    degraded_mode_active: bool
