from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
)


WorkerSaturationLevel = Literal[
    "low",
    "medium",
    "high",
]


@dataclass(frozen=True, slots=True)
class WorkerLoadEntry:
    """Canonical worker load entry."""

    worker_id: CanonicalWorkerId
    active_tasks: int
    max_concurrency: int
    saturation_level: WorkerSaturationLevel


@dataclass(frozen=True, slots=True)
class WorkerLoadContract:
    """Unified worker load / saturation contract."""

    total_workers: int
    workers: tuple[WorkerLoadEntry, ...]
