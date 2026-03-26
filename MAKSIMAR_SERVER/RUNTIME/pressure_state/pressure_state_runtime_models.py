from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.execution_pressure import (
    AdmissionDecision,
    PressureLevel,
    PressureSignalKind,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


PressureRuntimeState = Literal[
    "open",
    "throttled",
    "degraded",
    "protected",
]

NodeHealthState = Literal[
    "healthy",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class PressureStateRuntimeEntry:
    """Server-side pressure state runtime entry."""

    node_id: CanonicalNodeId
    pressure_level: PressureLevel
    runtime_state: PressureRuntimeState
    primary_signal_kind: PressureSignalKind
    primary_signal_value: int
    admission_decision: AdmissionDecision
    throttling_active: bool
    degraded_mode_active: bool
    overload_protection_active: bool
    health_state: NodeHealthState
    queue_depth: int
    reason: str

    def __post_init__(self) -> None:
        """Validate pressure state runtime invariants."""
        if self.primary_signal_value < 0:
            raise ValueError(
                f"primary_signal_value must be non-negative for {self.node_id}"
            )

        if self.queue_depth < 0:
            raise ValueError(f"queue_depth must be non-negative for {self.node_id}")

        if not self.reason.strip():
            raise ValueError(f"reason must not be empty for {self.node_id}")

        if self.pressure_level == "normal":
            if self.runtime_state != "open":
                raise ValueError("normal pressure must use runtime_state='open'")
            if self.admission_decision != "accept":
                raise ValueError("normal pressure must use admission_decision='accept'")
            if self.throttling_active:
                raise ValueError("normal pressure must not enable throttling")
            if self.degraded_mode_active:
                raise ValueError("normal pressure must not enable degraded mode")
            if self.overload_protection_active:
                raise ValueError(
                    "normal pressure must not enable overload protection"
                )

        if self.pressure_level == "elevated":
            if self.runtime_state != "throttled":
                raise ValueError(
                    "elevated pressure must use runtime_state='throttled'"
                )
            if self.admission_decision != "accept_with_throttle":
                raise ValueError(
                    "elevated pressure must use admission_decision='accept_with_throttle'"
                )
            if not self.throttling_active:
                raise ValueError("elevated pressure must enable throttling")
            if self.degraded_mode_active:
                raise ValueError("elevated pressure must not enable degraded mode")
            if self.overload_protection_active:
                raise ValueError(
                    "elevated pressure must not enable overload protection"
                )

        if self.pressure_level == "high":
            if self.runtime_state != "degraded":
                raise ValueError("high pressure must use runtime_state='degraded'")
            if self.admission_decision != "delay_new_work":
                raise ValueError(
                    "high pressure must use admission_decision='delay_new_work'"
                )
            if not self.throttling_active:
                raise ValueError("high pressure must enable throttling")
            if not self.degraded_mode_active:
                raise ValueError("high pressure must enable degraded mode")
            if not self.overload_protection_active:
                raise ValueError("high pressure must enable overload protection")

        if self.pressure_level == "critical":
            if self.runtime_state != "protected":
                raise ValueError(
                    "critical pressure must use runtime_state='protected'"
                )
            if self.admission_decision != "reject_new_work":
                raise ValueError(
                    "critical pressure must use admission_decision='reject_new_work'"
                )
            if not self.throttling_active:
                raise ValueError("critical pressure must enable throttling")
            if not self.degraded_mode_active:
                raise ValueError("critical pressure must enable degraded mode")
            if not self.overload_protection_active:
                raise ValueError("critical pressure must enable overload protection")


@dataclass(frozen=True, slots=True)
class PressureStateRuntimeContract:
    """Unified server-side pressure state runtime contract."""

    total_entries: int
    elevated_or_higher_entries: int
    degraded_active_entries: int
    entries: tuple[PressureStateRuntimeEntry, ...]
