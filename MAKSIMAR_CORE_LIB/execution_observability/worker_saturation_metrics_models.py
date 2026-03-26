from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
)


@dataclass(frozen=True, slots=True)
class WorkerSaturationMetricEntry:
    """Canonical worker saturation metric entry."""

    worker_id: CanonicalWorkerId
    active_tasks: int
    max_concurrency: int
    saturation_level: str


@dataclass(frozen=True, slots=True)
class WorkerSaturationMetricsContract:
    """Unified worker saturation metrics contract."""

    total_workers: int
    workers: tuple[WorkerSaturationMetricEntry, ...]
