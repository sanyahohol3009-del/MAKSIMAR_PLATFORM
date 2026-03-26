from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.workers_registry.worker_identity_models import (
    CanonicalWorkerId,
)


@dataclass(frozen=True, slots=True)
class LeaseMetricEntry:
    """Canonical deep lease metric entry."""

    lease_id: str
    owner_worker_id: CanonicalWorkerId
    active: bool


@dataclass(frozen=True, slots=True)
class LeaseMetricsContract:
    """Unified deep lease metrics contract."""

    total_leases: int
    leases: tuple[LeaseMetricEntry, ...]
