from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionQueueState:
    """Canonical execution queue state."""

    queue_name: str
    queued_tasks: int
    max_tasks: int
    overloaded: bool


@dataclass(frozen=True, slots=True)
class ExecutionQueueContract:
    """Unified execution queue contract."""

    total_queues: int
    queues: tuple[ExecutionQueueState, ...]
