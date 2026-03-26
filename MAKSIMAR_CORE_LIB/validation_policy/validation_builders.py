from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.validation_policy.validation_error_models import (
    ValidationErrorCode,
    ValidationErrorEntry,
    build_validation_error_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_policy_contract import (
    ValidationPolicyRuleEntry,
    build_validation_policy_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_task_class_models import (
    ValidationRiskLevel,
    ValidationTaskClass,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_tier_models import (
    ValidationTier,
    build_validation_tier_contract,
)


@dataclass(frozen=True, slots=True)
class BuiltValidationPlan:
    """Resolved validation plan derived from canonical validation policy."""

    rule_id: str
    task_class: ValidationTaskClass
    payload_class: PayloadClass
    required_validation_tier: ValidationTier
    effective_risk_level: ValidationRiskLevel
    header_validation_required: bool
    schema_validation_required: bool
    deep_validation_required: bool
    payload_reference_enforcement_required: bool
    execution_side_effects_possible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate built validation plan invariants."""
        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.rule_id}")

        if self.required_validation_tier == "L1_HEADER":
            if not self.header_validation_required:
                raise ValueError(
                    "L1_HEADER plan must require header validation"
                )
            if self.schema_validation_required:
                raise ValueError(
                    "L1_HEADER plan must not require schema validation"
                )
            if self.deep_validation_required:
                raise ValueError(
                    "L1_HEADER plan must not require deep validation"
                )

        if self.required_validation_tier == "L2_SCHEMA":
            if not self.header_validation_required:
                raise ValueError(
                    "L2_SCHEMA plan must require header validation"
                )
            if not self.schema_validation_required:
                raise ValueError(
                    "L2_SCHEMA plan must require schema validation"
                )
            if self.deep_validation_required and self.task_class not in (
                "simulation_request",
                "robotics_action",
                "automation_job",
            ):
                raise ValueError(
                    f"Unexpected deep validation requirement for {self.rule_id}"
                )

        if self.required_validation_tier == "L3_DEEP":
            if not self.header_validation_required:
                raise ValueError(
                    "L3_DEEP plan must require header validation"
                )
            if not self.schema_validation_required:
                raise ValueError(
                    "L3_DEEP plan must require schema validation"
                )
            if not self.deep_validation_required:
                raise ValueError(
                    "L3_DEEP plan must require deep validation"
                )

        if self.payload_class == "heavy_artifact":
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "heavy_artifact plan must require payload reference enforcement"
                )

        if self.task_class in ("robotics_action", "automation_job"):
            if not self.execution_side_effects_possible:
                raise ValueError(
                    f"{self.task_class} plan must declare execution side effects"
                )


def _find_policy_rule(
    *,
    task_class: ValidationTaskClass,
    payload_class: PayloadClass,
) -> ValidationPolicyRuleEntry:
    """Find canonical validation policy rule."""
    contract = build_validation_policy_contract()

    for rule in contract.rules:
        if rule.task_class == task_class and rule.payload_class == payload_class:
            return rule

    raise ValueError(
        f"No validation policy rule found for task_class={task_class}, payload_class={payload_class}"
    )


def _find_validation_error(
    *,
    error_code: ValidationErrorCode,
) -> ValidationErrorEntry:
    """Find canonical validation error entry."""
    contract = build_validation_error_contract()

    for error in contract.errors:
        if error.error_code == error_code:
            return error

    raise ValueError(f"Unknown validation error code: {error_code}")


def build_validation_plan(
    *,
    task_class: ValidationTaskClass,
    payload_class: PayloadClass,
) -> BuiltValidationPlan:
    """Build resolved validation plan from canonical validation policy."""
    policy_rule = _find_policy_rule(
        task_class=task_class,
        payload_class=payload_class,
    )

    tier_contract = build_validation_tier_contract()
    tier_entry = next(
        entry
        for entry in tier_contract.tiers
        if entry.tier_id == policy_rule.required_validation_tier
    )

    return BuiltValidationPlan(
        rule_id=policy_rule.rule_id,
        task_class=policy_rule.task_class,
        payload_class=policy_rule.payload_class,
        required_validation_tier=policy_rule.required_validation_tier,
        effective_risk_level=policy_rule.effective_risk_level,
        header_validation_required=tier_entry.header_validation_required,
        schema_validation_required=tier_entry.schema_validation_required,
        deep_validation_required=policy_rule.deep_validation_required,
        payload_reference_enforcement_required=policy_rule.payload_reference_enforcement_required,
        execution_side_effects_possible=policy_rule.execution_side_effects_possible,
        description=policy_rule.description,
    )


def build_validation_error_entry(
    *,
    error_code: ValidationErrorCode,
) -> ValidationErrorEntry:
    """Build canonical validation error entry by code."""
    return _find_validation_error(error_code=error_code)
