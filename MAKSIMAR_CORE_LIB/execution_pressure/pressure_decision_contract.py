from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.execution_pressure.pressure_level_models import (
    PressureLevel,
    build_pressure_level_contract,
)


PressureDecisionAction = Literal[
    "allow",
    "delay",
    "requeue",
    "reject",
    "degrade",
]

AdmissionDecision = Literal[
    "accept",
    "accept_with_throttle",
    "delay_new_work",
    "reject_new_work",
]


@dataclass(frozen=True, slots=True)
class PressureDecisionEntry:
    """Canonical decision rule for a pressure level."""

    pressure_level: PressureLevel
    primary_action: PressureDecisionAction
    admission_decision: AdmissionDecision
    degraded_mode_required: bool
    remote_reroute_preferred: bool
    new_task_admission_allowed: bool
    description: str

    def __post_init__(self) -> None:
        """Validate pressure decision invariants."""
        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.pressure_level}"
            )

        if self.pressure_level == "normal":
            if self.primary_action != "allow":
                raise ValueError("normal pressure must use primary_action='allow'")
            if self.admission_decision != "accept":
                raise ValueError("normal pressure must use admission_decision='accept'")
            if self.degraded_mode_required:
                raise ValueError("normal pressure must not require degraded mode")
            if not self.new_task_admission_allowed:
                raise ValueError("normal pressure must allow new task admission")

        if self.pressure_level == "elevated":
            if self.primary_action not in ("allow", "delay"):
                raise ValueError(
                    "elevated pressure must use primary_action in {'allow', 'delay'}"
                )
            if self.admission_decision not in ("accept", "accept_with_throttle"):
                raise ValueError(
                    "elevated pressure must use admission_decision in "
                    "{'accept', 'accept_with_throttle'}"
                )

        if self.pressure_level == "high":
            if self.primary_action not in ("delay", "degrade", "requeue"):
                raise ValueError(
                    "high pressure must use primary_action in "
                    "{'delay', 'degrade', 'requeue'}"
                )
            if not self.degraded_mode_required:
                raise ValueError("high pressure must require degraded mode")
            if self.admission_decision not in ("accept_with_throttle", "delay_new_work"):
                raise ValueError(
                    "high pressure must use admission_decision in "
                    "{'accept_with_throttle', 'delay_new_work'}"
                )

        if self.pressure_level == "critical":
            if self.primary_action not in ("reject", "degrade", "requeue"):
                raise ValueError(
                    "critical pressure must use primary_action in "
                    "{'reject', 'degrade', 'requeue'}"
                )
            if not self.degraded_mode_required:
                raise ValueError("critical pressure must require degraded mode")
            if self.admission_decision != "reject_new_work":
                raise ValueError(
                    "critical pressure must use admission_decision='reject_new_work'"
                )
            if self.new_task_admission_allowed:
                raise ValueError("critical pressure must not allow new task admission")


@dataclass(frozen=True, slots=True)
class PressureDecisionContract:
    """Unified canonical pressure decision contract."""

    total_rules: int
    rules: tuple[PressureDecisionEntry, ...]


def build_pressure_decision_contract() -> PressureDecisionContract:
    """Build canonical pressure decision contract."""
    pressure_levels = build_pressure_level_contract()
    level_order = tuple(entry.pressure_level for entry in pressure_levels.levels)

    rules = (
        PressureDecisionEntry(
            pressure_level="normal",
            primary_action="allow",
            admission_decision="accept",
            degraded_mode_required=False,
            remote_reroute_preferred=False,
            new_task_admission_allowed=True,
            description="Normal pressure accepts work without pressure-based intervention.",
        ),
        PressureDecisionEntry(
            pressure_level="elevated",
            primary_action="allow",
            admission_decision="accept_with_throttle",
            degraded_mode_required=False,
            remote_reroute_preferred=False,
            new_task_admission_allowed=True,
            description="Elevated pressure keeps work flowing with mild throttling.",
        ),
        PressureDecisionEntry(
            pressure_level="high",
            primary_action="degrade",
            admission_decision="delay_new_work",
            degraded_mode_required=True,
            remote_reroute_preferred=True,
            new_task_admission_allowed=True,
            description="High pressure prefers degraded execution and delayed admission.",
        ),
        PressureDecisionEntry(
            pressure_level="critical",
            primary_action="reject",
            admission_decision="reject_new_work",
            degraded_mode_required=True,
            remote_reroute_preferred=True,
            new_task_admission_allowed=False,
            description="Critical pressure blocks new work and protects runtime integrity.",
        ),
    )

    rule_order = tuple(entry.pressure_level for entry in rules)
    if rule_order != level_order:
        raise ValueError("Pressure decision rule order must match pressure level order")

    if len(set(rule_order)) != len(rule_order):
        raise ValueError("Duplicate pressure decision rules detected")

    return PressureDecisionContract(
        total_rules=len(rules),
        rules=rules,
    )
