from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_pressure import (
    DegradedRoutingPolicy,
    DegradedTriggerScope,
    PressureLevel,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId


@dataclass(frozen=True, slots=True)
class DegradedModeRuntimeEntry:
    """Server-side degraded mode runtime entry."""

    node_id: CanonicalNodeId
    pressure_level: PressureLevel
    degraded_mode_active: bool
    trigger_scope: DegradedTriggerScope
    feature_reduction_active: bool
    routing_policy: DegradedRoutingPolicy
    observability_alert_active: bool
    reason: str

    def __post_init__(self) -> None:
        """Validate degraded mode runtime invariants."""
        if not self.reason.strip():
            raise ValueError(f"reason must not be empty for {self.node_id}")

        if not self.degraded_mode_active:
            if self.trigger_scope != "none":
                raise ValueError(
                    f"trigger_scope must be 'none' when degraded mode is inactive for {self.node_id}"
                )
            if self.feature_reduction_active:
                raise ValueError(
                    f"feature_reduction_active must be False when degraded mode is inactive for {self.node_id}"
                )
            if self.routing_policy != "no_reroute":
                raise ValueError(
                    f"routing_policy must be 'no_reroute' when degraded mode is inactive for {self.node_id}"
                )
            if self.observability_alert_active:
                raise ValueError(
                    f"observability_alert_active must be False when degraded mode is inactive for {self.node_id}"
                )

        if self.degraded_mode_active:
            if self.trigger_scope == "none":
                raise ValueError(
                    f"trigger_scope must not be 'none' when degraded mode is active for {self.node_id}"
                )
            if not self.observability_alert_active:
                raise ValueError(
                    f"observability_alert_active must be True when degraded mode is active for {self.node_id}"
                )

        if self.pressure_level == "normal":
            if self.degraded_mode_active:
                raise ValueError(
                    "normal pressure must not activate degraded mode"
                )

        if self.pressure_level == "elevated":
            if self.degraded_mode_active:
                raise ValueError(
                    "elevated pressure must not activate degraded mode"
                )

        if self.pressure_level == "high":
            if self.degraded_mode_active and self.trigger_scope != "selective_reduction":
                raise ValueError(
                    "high pressure must use trigger_scope='selective_reduction'"
                )

        if self.pressure_level == "critical":
            if self.degraded_mode_active and self.trigger_scope != "broad_protection":
                raise ValueError(
                    "critical pressure must use trigger_scope='broad_protection'"
                )


@dataclass(frozen=True, slots=True)
class DegradedModeRuntimeContract:
    """Unified server-side degraded mode runtime contract."""

    total_entries: int
    active_entries: int
    entries: tuple[DegradedModeRuntimeEntry, ...]
