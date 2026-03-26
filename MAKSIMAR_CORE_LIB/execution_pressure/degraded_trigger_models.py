from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.execution_pressure.pressure_decision_contract import (
    build_pressure_decision_contract,
)
from MAKSIMAR_CORE_LIB.execution_pressure.pressure_level_models import (
    PressureLevel,
    build_pressure_level_contract,
)


DegradedTriggerScope = Literal[
    "none",
    "selective_reduction",
    "broad_protection",
]

DegradedRoutingPolicy = Literal[
    "no_reroute",
    "prefer_remote_reroute",
    "force_remote_reroute_when_available",
]


@dataclass(frozen=True, slots=True)
class DegradedTriggerEntry:
    """Canonical degraded trigger entry aligned with pressure policy."""

    pressure_level: PressureLevel
    trigger_enabled: bool
    trigger_scope: DegradedTriggerScope
    feature_reduction_required: bool
    routing_policy: DegradedRoutingPolicy
    observability_alert_required: bool
    description: str

    def __post_init__(self) -> None:
        """Validate degraded trigger invariants."""
        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.pressure_level}"
            )

        if not self.trigger_enabled:
            if self.trigger_scope != "none":
                raise ValueError(
                    f"trigger_scope must be 'none' when trigger is disabled for {self.pressure_level}"
                )
            if self.feature_reduction_required:
                raise ValueError(
                    f"feature_reduction_required must be False when trigger is disabled for {self.pressure_level}"
                )
            if self.routing_policy != "no_reroute":
                raise ValueError(
                    f"routing_policy must be 'no_reroute' when trigger is disabled for {self.pressure_level}"
                )

        if self.trigger_enabled:
            if self.trigger_scope == "none":
                raise ValueError(
                    f"trigger_scope must not be 'none' when trigger is enabled for {self.pressure_level}"
                )
            if not self.observability_alert_required:
                raise ValueError(
                    f"observability_alert_required must be True when trigger is enabled for {self.pressure_level}"
                )

        if self.pressure_level == "high":
            if not self.trigger_enabled:
                raise ValueError("high pressure must enable degraded trigger")
            if self.trigger_scope != "selective_reduction":
                raise ValueError(
                    "high pressure must use trigger_scope='selective_reduction'"
                )
            if self.routing_policy not in (
                "prefer_remote_reroute",
                "force_remote_reroute_when_available",
            ):
                raise ValueError(
                    "high pressure must prefer remote reroute"
                )

        if self.pressure_level == "critical":
            if not self.trigger_enabled:
                raise ValueError("critical pressure must enable degraded trigger")
            if self.trigger_scope != "broad_protection":
                raise ValueError(
                    "critical pressure must use trigger_scope='broad_protection'"
                )
            if self.routing_policy != "force_remote_reroute_when_available":
                raise ValueError(
                    "critical pressure must force remote reroute when available"
                )


@dataclass(frozen=True, slots=True)
class DegradedTriggerContract:
    """Unified canonical degraded trigger contract."""

    total_triggers: int
    triggers: tuple[DegradedTriggerEntry, ...]


def build_degraded_trigger_contract() -> DegradedTriggerContract:
    """Build canonical degraded trigger contract."""
    pressure_levels = build_pressure_level_contract()
    pressure_decisions = build_pressure_decision_contract()

    decision_by_level = {
        entry.pressure_level: entry for entry in pressure_decisions.rules
    }

    triggers = (
        DegradedTriggerEntry(
            pressure_level="normal",
            trigger_enabled=False,
            trigger_scope="none",
            feature_reduction_required=False,
            routing_policy="no_reroute",
            observability_alert_required=False,
            description="Normal pressure does not trigger degraded execution.",
        ),
        DegradedTriggerEntry(
            pressure_level="elevated",
            trigger_enabled=False,
            trigger_scope="none",
            feature_reduction_required=False,
            routing_policy="no_reroute",
            observability_alert_required=False,
            description="Elevated pressure remains observable without degraded trigger activation.",
        ),
        DegradedTriggerEntry(
            pressure_level="high",
            trigger_enabled=True,
            trigger_scope="selective_reduction",
            feature_reduction_required=True,
            routing_policy="prefer_remote_reroute",
            observability_alert_required=True,
            description="High pressure activates selective feature reduction and prefers reroute.",
        ),
        DegradedTriggerEntry(
            pressure_level="critical",
            trigger_enabled=True,
            trigger_scope="broad_protection",
            feature_reduction_required=True,
            routing_policy="force_remote_reroute_when_available",
            observability_alert_required=True,
            description="Critical pressure activates broad protection and aggressive rerouting.",
        ),
    )

    level_order = tuple(entry.pressure_level for entry in pressure_levels.levels)
    trigger_order = tuple(entry.pressure_level for entry in triggers)
    if trigger_order != level_order:
        raise ValueError(
            "Degraded trigger order must match canonical pressure level order"
        )

    if len(set(trigger_order)) != len(trigger_order):
        raise ValueError("Duplicate degraded trigger levels detected")

    for trigger in triggers:
        decision = decision_by_level[trigger.pressure_level]
        if decision.degraded_mode_required != trigger.trigger_enabled:
            raise ValueError(
                f"Degraded trigger mismatch for {trigger.pressure_level}"
            )

    return DegradedTriggerContract(
        total_triggers=len(triggers),
        triggers=triggers,
    )
