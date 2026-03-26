from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_control.queue_identity_models import (
    CanonicalQueueName,
)


@dataclass(frozen=True, slots=True)
class QueueRuntimeState:
    """Canonical queue runtime state entry."""

    queue_name: CanonicalQueueName
    queued_tasks: int
    running_tasks: int
    overloaded: bool


@dataclass(frozen=True, slots=True)
class QueueRuntimeContract:
    """Unified queue runtime state contract."""

    total_queues: int
    queues: tuple[QueueRuntimeState, ...]
