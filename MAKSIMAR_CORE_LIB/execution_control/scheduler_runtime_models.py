from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class SchedulerRuntimeState:
    """Canonical scheduler runtime state entry."""

    scheduler_id: str
    active_node_id: CanonicalNodeId
    queued_tasks: int
    degraded_mode_active: bool


@dataclass(frozen=True, slots=True)
class SchedulerRuntimeContract:
    """Unified scheduler runtime state contract."""

    total_schedulers: int
    schedulers: tuple[SchedulerRuntimeState, ...]
