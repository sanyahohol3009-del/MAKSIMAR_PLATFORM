from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionState:
    """Canonical execution control runtime state."""

    total_tasks: int
    queued_tasks: int
    running_tasks: int
    node_health: str
    degraded_mode_active: bool


@dataclass(frozen=True, slots=True)
class ExecutionStateContract:
    """Unified execution state contract."""

    state: ExecutionState
