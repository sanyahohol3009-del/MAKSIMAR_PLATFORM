from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
)


@dataclass(frozen=True, slots=True)
class LeaseRuntimeState:
    """Canonical lease runtime state entry."""

    lease_id: str
    owner_task_id: str
    owner_worker_id: CanonicalWorkerId
    active: bool


@dataclass(frozen=True, slots=True)
class LeaseRuntimeContract:
    """Unified lease runtime state contract."""

    total_leases: int
    leases: tuple[LeaseRuntimeState, ...]
