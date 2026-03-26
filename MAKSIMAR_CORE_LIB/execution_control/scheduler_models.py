from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SchedulerState:
    """Canonical scheduler state."""

    scheduler_id: str
    active_node: str
    running_tasks: int
    degraded_mode_active: bool


@dataclass(frozen=True, slots=True)
class SchedulerContract:
    """Unified scheduler contract."""

    total_schedulers: int
    schedulers: tuple[SchedulerState, ...]
