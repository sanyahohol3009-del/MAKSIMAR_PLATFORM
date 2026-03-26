from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.validation_policy.validation_payload_class_models import (
    ValidationPayloadRiskLevel,
    build_validation_payload_class_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_task_class_models import (
    ValidationRiskLevel,
    ValidationTaskClass,
    build_validation_task_class_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_tier_models import (
    ValidationTier,
    build_validation_tier_contract,
)


_RISK_RANK = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}

_TIER_RANK = {
    "L1_HEADER": 0,
    "L2_SCHEMA": 1,
    "L3_DEEP": 2,
}


def _resolve_stricter_tier(
    task_tier: ValidationTier,
    payload_tier: ValidationTier,
) -> ValidationTier:
    """Resolve stricter validation tier."""
    if _TIER_RANK[task_tier] >= _TIER_RANK[payload_tier]:
        return task_tier
    return payload_tier


def _resolve_higher_risk(
    task_risk: ValidationRiskLevel,
    payload_risk: ValidationPayloadRiskLevel,
) -> ValidationRiskLevel:
    """Resolve higher validation risk level."""
    if _RISK_RANK[task_risk] >= _RISK_RANK[payload_risk]:
        return task_risk
    return payload_risk  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class ValidationPolicyRuleEntry:
    """Canonical validation policy rule entry."""

    rule_id: str
    task_class: ValidationTaskClass
    payload_class: PayloadClass
    required_validation_tier: ValidationTier
    effective_risk_level: ValidationRiskLevel
    payload_reference_enforcement_required: bool
    deep_validation_required: bool
    execution_side_effects_possible: bool
    policy_order: int
    description: str

    def __post_init__(self) -> None:
        """Validate validation policy invariants."""
        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")

        if self.policy_order < 0:
            raise ValueError(f"policy_order must be non-negative for {self.rule_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.rule_id}")

        if self.payload_class == "heavy_artifact":
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "heavy_artifact rules must require payload reference enforcement"
                )

        if self.required_validation_tier == "L1_HEADER":
            if self.deep_validation_required:
                raise ValueError(
                    f"L1_HEADER rule must not require deep validation: {self.rule_id}"
                )

        if self.required_validation_tier == "L3_DEEP":
            if not self.deep_validation_required:
                raise ValueError(
                    f"L3_DEEP rule must require deep validation: {self.rule_id}"
                )

        if self.task_class in ("robotics_action", "automation_job"):
            if not self.execution_side_effects_possible:
                raise ValueError(
                    f"{self.task_class} must declare execution side effects: {self.rule_id}"
                )

        if self.task_class == "chat_request":
            if self.payload_class == "heavy_artifact":
                raise ValueError(
                    "chat_request must not pair with heavy_artifact in default validation policy"
                )


@dataclass(frozen=True, slots=True)
class ValidationPolicyContract:
    """Unified canonical validation policy contract."""

    total_rules: int
    rules: tuple[ValidationPolicyRuleEntry, ...]


def build_validation_policy_contract() -> ValidationPolicyContract:
    """Build canonical validation policy contract."""
    tier_contract = build_validation_tier_contract()
    task_contract = build_validation_task_class_contract()
    payload_contract = build_validation_payload_class_contract()

    allowed_payloads_by_task: dict[ValidationTaskClass, tuple[PayloadClass, ...]] = {
        "chat_request": ("small_control", "medium_contract"),
        "simulation_request": ("medium_contract", "heavy_artifact"),
        "robotics_action": ("medium_contract", "heavy_artifact"),
        "media_job": ("medium_contract", "heavy_artifact"),
        "evaluation_job": ("medium_contract", "heavy_artifact"),
        "automation_job": ("medium_contract", "heavy_artifact"),
    }

    tier_ids = tuple(entry.tier_id for entry in tier_contract.tiers)
    if tier_ids != ("L1_HEADER", "L2_SCHEMA", "L3_DEEP"):
        raise ValueError("Validation tier contract must be canonical before policy build")

    payload_by_id = {
        entry.payload_class: entry for entry in payload_contract.payload_classes
    }

    rules: list[ValidationPolicyRuleEntry] = []
    policy_order = 0

    for task_entry in task_contract.task_classes:
        allowed_payloads = allowed_payloads_by_task[task_entry.task_class]

        for payload_class in allowed_payloads:
            payload_entry = payload_by_id[payload_class]

            required_validation_tier = _resolve_stricter_tier(
                task_entry.default_validation_tier,
                payload_entry.minimum_validation_tier,
            )
            effective_risk_level = _resolve_higher_risk(
                task_entry.risk_level,
                payload_entry.risk_level,
            )
            payload_reference_enforcement_required = (
                task_entry.payload_reference_enforcement_required
                or payload_entry.payload_reference_required
            )
            deep_validation_required = (
                task_entry.deep_validation_default_required
                or payload_entry.deep_validation_required_for_default_flow
                or required_validation_tier == "L3_DEEP"
            )

            rule_id = f"policy_{task_entry.task_class}_{payload_class}"

            rules.append(
                ValidationPolicyRuleEntry(
                    rule_id=rule_id,
                    task_class=task_entry.task_class,
                    payload_class=payload_class,
                    required_validation_tier=required_validation_tier,
                    effective_risk_level=effective_risk_level,
                    payload_reference_enforcement_required=payload_reference_enforcement_required,
                    deep_validation_required=deep_validation_required,
                    execution_side_effects_possible=task_entry.execution_side_effects_possible,
                    policy_order=policy_order,
                    description=(
                        f"Validation policy for task_class={task_entry.task_class} "
                        f"with payload_class={payload_class}."
                    ),
                )
            )
            policy_order += 1

    rule_ids = tuple(entry.rule_id for entry in rules)
    rule_orders = tuple(entry.policy_order for entry in rules)

    if len(set(rule_ids)) != len(rule_ids):
        raise ValueError("Duplicate validation policy rule ids detected")

    if len(set(rule_orders)) != len(rule_orders):
        raise ValueError("Duplicate validation policy rule orders detected")

    expected_total_rules = sum(
        len(allowed_payloads)
        for allowed_payloads in allowed_payloads_by_task.values()
    )
    if len(rules) != expected_total_rules:
        raise ValueError("Validation policy rule count is invalid")

    return ValidationPolicyContract(
        total_rules=len(rules),
        rules=tuple(rules),
    )
