from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.validation_policy.validation_tier_models import (
    ValidationTier,
)


ValidationTaskClass = Literal[
    "chat_request",
    "simulation_request",
    "robotics_action",
    "media_job",
    "evaluation_job",
    "automation_job",
]

ValidationRiskLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


@dataclass(frozen=True, slots=True)
class ValidationTaskClassEntry:
    """Canonical validation task class description entry."""

    task_class: ValidationTaskClass
    tier_order: int
    default_validation_tier: ValidationTier
    risk_level: ValidationRiskLevel
    payload_reference_enforcement_required: bool
    deep_validation_default_required: bool
    execution_side_effects_possible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate task class invariants."""
        if self.tier_order < 0:
            raise ValueError(f"tier_order must be non-negative for {self.task_class}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.task_class}")

        if self.task_class == "chat_request":
            if self.tier_order != 0:
                raise ValueError("chat_request must use tier_order=0")
            if self.default_validation_tier != "L1_HEADER":
                raise ValueError(
                    "chat_request must default to validation tier 'L1_HEADER'"
                )
            if self.risk_level != "low":
                raise ValueError("chat_request must use risk_level='low'")
            if self.payload_reference_enforcement_required:
                raise ValueError(
                    "chat_request must not require payload reference enforcement"
                )
            if self.deep_validation_default_required:
                raise ValueError(
                    "chat_request must not require deep validation by default"
                )
            if self.execution_side_effects_possible:
                raise ValueError(
                    "chat_request must not declare execution side effects"
                )

        if self.task_class == "simulation_request":
            if self.tier_order != 1:
                raise ValueError("simulation_request must use tier_order=1")
            if self.default_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    "simulation_request must default to validation tier 'L2_SCHEMA'"
                )
            if self.risk_level != "medium":
                raise ValueError("simulation_request must use risk_level='medium'")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "simulation_request must require payload reference enforcement"
                )
            if self.deep_validation_default_required:
                raise ValueError(
                    "simulation_request must not require deep validation by default"
                )

        if self.task_class == "robotics_action":
            if self.tier_order != 2:
                raise ValueError("robotics_action must use tier_order=2")
            if self.default_validation_tier != "L3_DEEP":
                raise ValueError(
                    "robotics_action must default to validation tier 'L3_DEEP'"
                )
            if self.risk_level != "critical":
                raise ValueError("robotics_action must use risk_level='critical'")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "robotics_action must require payload reference enforcement"
                )
            if not self.deep_validation_default_required:
                raise ValueError(
                    "robotics_action must require deep validation by default"
                )
            if not self.execution_side_effects_possible:
                raise ValueError(
                    "robotics_action must declare execution side effects"
                )

        if self.task_class == "media_job":
            if self.tier_order != 3:
                raise ValueError("media_job must use tier_order=3")
            if self.default_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    "media_job must default to validation tier 'L2_SCHEMA'"
                )
            if self.risk_level != "medium":
                raise ValueError("media_job must use risk_level='medium'")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "media_job must require payload reference enforcement"
                )
            if self.deep_validation_default_required:
                raise ValueError(
                    "media_job must not require deep validation by default"
                )

        if self.task_class == "evaluation_job":
            if self.tier_order != 4:
                raise ValueError("evaluation_job must use tier_order=4")
            if self.default_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    "evaluation_job must default to validation tier 'L2_SCHEMA'"
                )
            if self.risk_level != "medium":
                raise ValueError("evaluation_job must use risk_level='medium'")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "evaluation_job must require payload reference enforcement"
                )
            if self.deep_validation_default_required:
                raise ValueError(
                    "evaluation_job must not require deep validation by default"
                )

        if self.task_class == "automation_job":
            if self.tier_order != 5:
                raise ValueError("automation_job must use tier_order=5")
            if self.default_validation_tier != "L3_DEEP":
                raise ValueError(
                    "automation_job must default to validation tier 'L3_DEEP'"
                )
            if self.risk_level != "high":
                raise ValueError("automation_job must use risk_level='high'")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "automation_job must require payload reference enforcement"
                )
            if not self.deep_validation_default_required:
                raise ValueError(
                    "automation_job must require deep validation by default"
                )
            if not self.execution_side_effects_possible:
                raise ValueError(
                    "automation_job must declare execution side effects"
                )


@dataclass(frozen=True, slots=True)
class ValidationTaskClassContract:
    """Unified canonical validation task class contract."""

    total_task_classes: int
    task_classes: tuple[ValidationTaskClassEntry, ...]


def build_validation_task_class_contract() -> ValidationTaskClassContract:
    """Build canonical validation task class contract."""
    task_classes = (
        ValidationTaskClassEntry(
            task_class="chat_request",
            tier_order=0,
            default_validation_tier="L1_HEADER",
            risk_level="low",
            payload_reference_enforcement_required=False,
            deep_validation_default_required=False,
            execution_side_effects_possible=False,
            description="Interactive chat request with fast header validation path.",
        ),
        ValidationTaskClassEntry(
            task_class="simulation_request",
            tier_order=1,
            default_validation_tier="L2_SCHEMA",
            risk_level="medium",
            payload_reference_enforcement_required=True,
            deep_validation_default_required=False,
            execution_side_effects_possible=False,
            description="Simulation request that requires schema validation and payload reference enforcement.",
        ),
        ValidationTaskClassEntry(
            task_class="robotics_action",
            tier_order=2,
            default_validation_tier="L3_DEEP",
            risk_level="critical",
            payload_reference_enforcement_required=True,
            deep_validation_default_required=True,
            execution_side_effects_possible=True,
            description="Robotics action requiring deep validation before execution-side effects.",
        ),
        ValidationTaskClassEntry(
            task_class="media_job",
            tier_order=3,
            default_validation_tier="L2_SCHEMA",
            risk_level="medium",
            payload_reference_enforcement_required=True,
            deep_validation_default_required=False,
            execution_side_effects_possible=False,
            description="Media job requiring structured validation and artifact-safe routing.",
        ),
        ValidationTaskClassEntry(
            task_class="evaluation_job",
            tier_order=4,
            default_validation_tier="L2_SCHEMA",
            risk_level="medium",
            payload_reference_enforcement_required=True,
            deep_validation_default_required=False,
            execution_side_effects_possible=False,
            description="Evaluation job requiring schema validation and controlled payload flow.",
        ),
        ValidationTaskClassEntry(
            task_class="automation_job",
            tier_order=5,
            default_validation_tier="L3_DEEP",
            risk_level="high",
            payload_reference_enforcement_required=True,
            deep_validation_default_required=True,
            execution_side_effects_possible=True,
            description="Automation job requiring deep validation before execution-side effects.",
        ),
    )

    task_class_ids = tuple(entry.task_class for entry in task_classes)
    tier_orders = tuple(entry.tier_order for entry in task_classes)

    expected_order = (
        "chat_request",
        "simulation_request",
        "robotics_action",
        "media_job",
        "evaluation_job",
        "automation_job",
    )

    if task_class_ids != expected_order:
        raise ValueError("Validation task class order is invalid")

    if tier_orders != (0, 1, 2, 3, 4, 5):
        raise ValueError("Validation task class numeric order is invalid")

    if len(set(task_class_ids)) != len(task_class_ids):
        raise ValueError("Duplicate validation task classes detected")

    if len(set(tier_orders)) != len(tier_orders):
        raise ValueError("Duplicate validation task class orders detected")

    return ValidationTaskClassContract(
        total_task_classes=len(task_classes),
        task_classes=task_classes,
    )
