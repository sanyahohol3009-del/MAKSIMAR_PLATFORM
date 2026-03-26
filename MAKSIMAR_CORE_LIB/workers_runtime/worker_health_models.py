from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
)


WorkerHealthStatus = Literal[
    "ok",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class WorkerHealthEntry:
    """Canonical worker health entry."""

    worker_id: CanonicalWorkerId
    status: WorkerHealthStatus
    active_tasks: int
    heartbeat_ok: bool


@dataclass(frozen=True, slots=True)
class WorkerHealthContract:
    """Unified worker health contract."""

    total_workers: int
    workers: tuple[WorkerHealthEntry, ...]
