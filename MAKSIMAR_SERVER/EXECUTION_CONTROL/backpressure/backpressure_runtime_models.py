from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_pressure import (
    AdmissionDecision,
    PressureDecisionAction,
    PressureLevel,
    PressureSignalKind,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class ServerBackpressureRuntimeEntry:
    """Server-side backpressure runtime entry."""

    node_id: CanonicalNodeId
    pressure_level: PressureLevel
    primary_signal_kind: PressureSignalKind
    primary_signal_value: int
    primary_action: PressureDecisionAction
    admission_decision: AdmissionDecision
    throttling_active: bool
    degraded_mode_required: bool
    remote_reroute_preferred: bool
    overload_protection_active: bool
    reason: str

    def __post_init__(self) -> None:
        """Validate backpressure runtime invariants."""
        if self.primary_signal_value < 0:
            raise ValueError(
                f"primary_signal_value must be non-negative for {self.node_id}"
            )

        if not self.reason.strip():
            raise ValueError(f"reason must not be empty for {self.node_id}")

        if self.pressure_level == "normal":
            if self.primary_action != "allow":
                raise ValueError("normal pressure must use primary_action='allow'")
            if self.admission_decision != "accept":
                raise ValueError("normal pressure must use admission_decision='accept'")
            if self.throttling_active:
                raise ValueError("normal pressure must not enable throttling")
            if self.degraded_mode_required:
                raise ValueError("normal pressure must not require degraded mode")
            if self.remote_reroute_preferred:
                raise ValueError("normal pressure must not prefer remote reroute")
            if self.overload_protection_active:
                raise ValueError(
                    "normal pressure must not enable overload protection"
                )

        if self.pressure_level == "elevated":
            if self.admission_decision != "accept_with_throttle":
                raise ValueError(
                    "elevated pressure must use admission_decision='accept_with_throttle'"
                )
            if not self.throttling_active:
                raise ValueError("elevated pressure must enable throttling")
            if self.degraded_mode_required:
                raise ValueError("elevated pressure must not require degraded mode")
            if self.overload_protection_active:
                raise ValueError(
                    "elevated pressure must not enable overload protection"
                )

        if self.pressure_level == "high":
            if self.admission_decision != "delay_new_work":
                raise ValueError(
                    "high pressure must use admission_decision='delay_new_work'"
                )
            if not self.throttling_active:
                raise ValueError("high pressure must enable throttling")
            if not self.degraded_mode_required:
                raise ValueError("high pressure must require degraded mode")
            if not self.remote_reroute_preferred:
                raise ValueError("high pressure must prefer remote reroute")
            if not self.overload_protection_active:
                raise ValueError("high pressure must enable overload protection")

        if self.pressure_level == "critical":
            if self.admission_decision != "reject_new_work":
                raise ValueError(
                    "critical pressure must use admission_decision='reject_new_work'"
                )
            if not self.throttling_active:
                raise ValueError("critical pressure must enable throttling")
            if not self.degraded_mode_required:
                raise ValueError("critical pressure must require degraded mode")
            if not self.remote_reroute_preferred:
                raise ValueError("critical pressure must prefer remote reroute")
            if not self.overload_protection_active:
                raise ValueError("critical pressure must enable overload protection")


@dataclass(frozen=True, slots=True)
class ServerBackpressureRuntimeContract:
    """Unified server-side backpressure runtime contract."""

    total_entries: int
    entries: tuple[ServerBackpressureRuntimeEntry, ...]
