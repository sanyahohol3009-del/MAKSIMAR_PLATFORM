from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId
from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
    CanonicalWorkerType,
)


@dataclass(frozen=True, slots=True)
class WorkerEntry:
    """Canonical worker registry entry."""

    worker_id: CanonicalWorkerId
    worker_type: CanonicalWorkerType
    target_node: CanonicalNodeId
    active: bool


@dataclass(frozen=True, slots=True)
class WorkerRegistryContract:
    """Unified worker registry contract."""

    total_workers: int
    workers: tuple[WorkerEntry, ...]
