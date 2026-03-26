from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_pressure.degraded_trigger_models import (
    build_degraded_trigger_contract,
)
from MAKSIMAR_CORE_LIB.execution_pressure.pressure_decision_contract import (
    AdmissionDecision,
    PressureDecisionAction,
    build_pressure_decision_contract,
)
from MAKSIMAR_CORE_LIB.execution_pressure.pressure_level_models import (
    PressureLevel,
    build_pressure_level_contract,
)


@dataclass(frozen=True, slots=True)
class AdmissionPressureRuleEntry:
    """Canonical admission rule aligned with pressure decision and degraded trigger policy."""

    pressure_level: PressureLevel
    admission_decision: AdmissionDecision
    primary_action: PressureDecisionAction
    new_task_admission_allowed: bool
    throttling_required: bool
    delay_required: bool
    rejection_required: bool
    degraded_mode_required: bool
    remote_reroute_preferred: bool
    description: str

    def __post_init__(self) -> None:
        """Validate admission rule invariants."""
        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.pressure_level}"
            )

        if self.pressure_level == "normal":
            if self.admission_decision != "accept":
                raise ValueError("normal pressure must use admission_decision='accept'")
            if self.primary_action != "allow":
                raise ValueError("normal pressure must use primary_action='allow'")
            if not self.new_task_admission_allowed:
                raise ValueError("normal pressure must allow new task admission")
            if self.throttling_required:
                raise ValueError("normal pressure must not require throttling")
            if self.delay_required:
                raise ValueError("normal pressure must not require delay")
            if self.rejection_required:
                raise ValueError("normal pressure must not require rejection")
            if self.degraded_mode_required:
                raise ValueError("normal pressure must not require degraded mode")

        if self.pressure_level == "elevated":
            if self.admission_decision != "accept_with_throttle":
                raise ValueError(
                    "elevated pressure must use admission_decision='accept_with_throttle'"
                )
            if not self.new_task_admission_allowed:
                raise ValueError("elevated pressure must allow new task admission")
            if not self.throttling_required:
                raise ValueError("elevated pressure must require throttling")
            if self.delay_required:
                raise ValueError("elevated pressure must not require delay")
            if self.rejection_required:
                raise ValueError("elevated pressure must not require rejection")

        if self.pressure_level == "high":
            if self.admission_decision != "delay_new_work":
                raise ValueError(
                    "high pressure must use admission_decision='delay_new_work'"
                )
            if not self.new_task_admission_allowed:
                raise ValueError(
                    "high pressure must keep admission logically available for delayed work"
                )
            if not self.throttling_required:
                raise ValueError("high pressure must require throttling")
            if not self.delay_required:
                raise ValueError("high pressure must require delayed admission")
            if self.rejection_required:
                raise ValueError("high pressure must not require outright rejection")
            if not self.degraded_mode_required:
                raise ValueError("high pressure must require degraded mode")

        if self.pressure_level == "critical":
            if self.admission_decision != "reject_new_work":
                raise ValueError(
                    "critical pressure must use admission_decision='reject_new_work'"
                )
            if self.new_task_admission_allowed:
                raise ValueError("critical pressure must not allow new task admission")
            if not self.throttling_required:
                raise ValueError("critical pressure must require throttling")
            if self.delay_required:
                raise ValueError("critical pressure must not use delayed admission")
            if not self.rejection_required:
                raise ValueError("critical pressure must require rejection")
            if not self.degraded_mode_required:
                raise ValueError("critical pressure must require degraded mode")
            if not self.remote_reroute_preferred:
                raise ValueError("critical pressure must prefer remote reroute")


@dataclass(frozen=True, slots=True)
class AdmissionPressureRulesContract:
    """Unified canonical admission pressure rules contract."""

    total_rules: int
    rules: tuple[AdmissionPressureRuleEntry, ...]


def build_admission_pressure_rules_contract() -> AdmissionPressureRulesContract:
    """Build canonical admission pressure rules contract."""
    pressure_levels = build_pressure_level_contract()
    pressure_decisions = build_pressure_decision_contract()
    degraded_triggers = build_degraded_trigger_contract()

    decision_by_level = {
        entry.pressure_level: entry for entry in pressure_decisions.rules
    }
    trigger_by_level = {
        entry.pressure_level: entry for entry in degraded_triggers.triggers
    }

    rules = (
        AdmissionPressureRuleEntry(
            pressure_level="normal",
            admission_decision="accept",
            primary_action="allow",
            new_task_admission_allowed=True,
            throttling_required=False,
            delay_required=False,
            rejection_required=False,
            degraded_mode_required=False,
            remote_reroute_preferred=False,
            description="Normal pressure admits work without extra protection.",
        ),
        AdmissionPressureRuleEntry(
            pressure_level="elevated",
            admission_decision="accept_with_throttle",
            primary_action="allow",
            new_task_admission_allowed=True,
            throttling_required=True,
            delay_required=False,
            rejection_required=False,
            degraded_mode_required=False,
            remote_reroute_preferred=False,
            description="Elevated pressure admits work with mild throttling.",
        ),
        AdmissionPressureRuleEntry(
            pressure_level="high",
            admission_decision="delay_new_work",
            primary_action="degrade",
            new_task_admission_allowed=True,
            throttling_required=True,
            delay_required=True,
            rejection_required=False,
            degraded_mode_required=True,
            remote_reroute_preferred=True,
            description="High pressure delays new work and prefers degraded/rerouted execution.",
        ),
        AdmissionPressureRuleEntry(
            pressure_level="critical",
            admission_decision="reject_new_work",
            primary_action="reject",
            new_task_admission_allowed=False,
            throttling_required=True,
            delay_required=False,
            rejection_required=True,
            degraded_mode_required=True,
            remote_reroute_preferred=True,
            description="Critical pressure rejects new work and maximizes protection.",
        ),
    )

    level_order = tuple(entry.pressure_level for entry in pressure_levels.levels)
    rule_order = tuple(entry.pressure_level for entry in rules)
    if rule_order != level_order:
        raise ValueError("Admission pressure rule order must match canonical level order")

    if len(set(rule_order)) != len(rule_order):
        raise ValueError("Duplicate admission pressure rules detected")

    for rule in rules:
        decision = decision_by_level[rule.pressure_level]
        trigger = trigger_by_level[rule.pressure_level]

        if rule.admission_decision != decision.admission_decision:
            raise ValueError(
                f"Admission decision mismatch for {rule.pressure_level}"
            )
        if rule.primary_action != decision.primary_action:
            raise ValueError(
                f"Primary action mismatch for {rule.pressure_level}"
            )
        if rule.new_task_admission_allowed != decision.new_task_admission_allowed:
            raise ValueError(
                f"Admission allowance mismatch for {rule.pressure_level}"
            )
        if rule.degraded_mode_required != decision.degraded_mode_required:
            raise ValueError(
                f"Degraded mode requirement mismatch for {rule.pressure_level}"
            )
        if rule.remote_reroute_preferred != decision.remote_reroute_preferred:
            raise ValueError(
                f"Remote reroute preference mismatch for {rule.pressure_level}"
            )
        if rule.degraded_mode_required != trigger.trigger_enabled:
            raise ValueError(
                f"Trigger alignment mismatch for {rule.pressure_level}"
            )

    return AdmissionPressureRulesContract(
        total_rules=len(rules),
        rules=rules,
    )
