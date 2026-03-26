from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_control.queue_identity_models import (
    CanonicalQueueName,
)


@dataclass(frozen=True, slots=True)
class QueueMetricEntry:
    """Canonical deep queue metric entry."""

    queue_name: CanonicalQueueName
    queued_tasks: int
    running_tasks: int
    overloaded: bool


@dataclass(frozen=True, slots=True)
class QueueMetricsContract:
    """Unified deep queue metrics contract."""

    total_queues: int
    queues: tuple[QueueMetricEntry, ...]
