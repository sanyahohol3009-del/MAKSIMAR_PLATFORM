from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionLease:
    """Canonical execution lease state."""

    lease_id: str
    owner_task_id: str
    resource_type: str
    active: bool


@dataclass(frozen=True, slots=True)
class ExecutionLeaseContract:
    """Unified execution lease contract."""

    total_leases: int
    leases: tuple[ExecutionLease, ...]
