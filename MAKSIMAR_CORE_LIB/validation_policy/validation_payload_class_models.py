from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
)
from MAKSIMAR_CORE_LIB.validation_policy.validation_tier_models import (
    ValidationTier,
)


ValidationPayloadRiskLevel = Literal[
    "low",
    "medium",
    "high",
]


@dataclass(frozen=True, slots=True)
class ValidationPayloadClassEntry:
    """Canonical validation payload class description entry."""

    payload_class: PayloadClass
    validation_order: int
    minimum_validation_tier: ValidationTier
    risk_level: ValidationPayloadRiskLevel
    inline_payload_allowed: bool
    payload_reference_required: bool
    deep_validation_required_for_default_flow: bool
    description: str

    def __post_init__(self) -> None:
        """Validate validation payload class invariants."""
        if self.validation_order < 0:
            raise ValueError(
                f"validation_order must be non-negative for {self.payload_class}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.payload_class}"
            )

        if self.payload_class == "small_control":
            if self.validation_order != 0:
                raise ValueError("small_control must use validation_order=0")
            if self.minimum_validation_tier != "L1_HEADER":
                raise ValueError(
                    "small_control must use minimum_validation_tier='L1_HEADER'"
                )
            if self.risk_level != "low":
                raise ValueError("small_control must use risk_level='low'")
            if not self.inline_payload_allowed:
                raise ValueError("small_control must allow inline payload")
            if self.payload_reference_required:
                raise ValueError(
                    "small_control must not require payload reference"
                )
            if self.deep_validation_required_for_default_flow:
                raise ValueError(
                    "small_control must not require deep validation by default"
                )

        if self.payload_class == "medium_contract":
            if self.validation_order != 1:
                raise ValueError("medium_contract must use validation_order=1")
            if self.minimum_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    "medium_contract must use minimum_validation_tier='L2_SCHEMA'"
                )
            if self.risk_level != "medium":
                raise ValueError("medium_contract must use risk_level='medium'")
            if not self.inline_payload_allowed:
                raise ValueError("medium_contract must allow inline payload")
            if self.payload_reference_required:
                raise ValueError(
                    "medium_contract must not require payload reference"
                )
            if self.deep_validation_required_for_default_flow:
                raise ValueError(
                    "medium_contract must not require deep validation by default"
                )

        if self.payload_class == "heavy_artifact":
            if self.validation_order != 2:
                raise ValueError("heavy_artifact must use validation_order=2")
            if self.minimum_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    "heavy_artifact must use minimum_validation_tier='L2_SCHEMA'"
                )
            if self.risk_level != "high":
                raise ValueError("heavy_artifact must use risk_level='high'")
            if self.inline_payload_allowed:
                raise ValueError("heavy_artifact must not allow inline payload")
            if not self.payload_reference_required:
                raise ValueError(
                    "heavy_artifact must require payload reference"
                )
            if not self.deep_validation_required_for_default_flow:
                raise ValueError(
                    "heavy_artifact must require deep validation by default"
                )


@dataclass(frozen=True, slots=True)
class ValidationPayloadClassContract:
    """Unified canonical validation payload class contract."""

    total_payload_classes: int
    payload_classes: tuple[ValidationPayloadClassEntry, ...]


def build_validation_payload_class_contract() -> ValidationPayloadClassContract:
    """Build canonical validation payload class contract."""
    payload_classes = (
        ValidationPayloadClassEntry(
            payload_class="small_control",
            validation_order=0,
            minimum_validation_tier="L1_HEADER",
            risk_level="low",
            inline_payload_allowed=True,
            payload_reference_required=False,
            deep_validation_required_for_default_flow=False,
            description="Small control payload validated through fast header-level policy.",
        ),
        ValidationPayloadClassEntry(
            payload_class="medium_contract",
            validation_order=1,
            minimum_validation_tier="L2_SCHEMA",
            risk_level="medium",
            inline_payload_allowed=True,
            payload_reference_required=False,
            deep_validation_required_for_default_flow=False,
            description="Medium structured payload requiring schema validation before execution.",
        ),
        ValidationPayloadClassEntry(
            payload_class="heavy_artifact",
            validation_order=2,
            minimum_validation_tier="L2_SCHEMA",
            risk_level="high",
            inline_payload_allowed=False,
            payload_reference_required=True,
            deep_validation_required_for_default_flow=True,
            description="Heavy artifact payload requiring reference-safe routing and deep validation by default.",
        ),
    )

    payload_ids = tuple(entry.payload_class for entry in payload_classes)
    validation_orders = tuple(entry.validation_order for entry in payload_classes)

    if payload_ids != ("small_control", "medium_contract", "heavy_artifact"):
        raise ValueError("Validation payload class order is invalid")

    if validation_orders != (0, 1, 2):
        raise ValueError("Validation payload class numeric order is invalid")

    if len(set(payload_ids)) != len(payload_ids):
        raise ValueError("Duplicate validation payload classes detected")

    if len(set(validation_orders)) != len(validation_orders):
        raise ValueError("Duplicate validation payload class orders detected")

    return ValidationPayloadClassContract(
        total_payload_classes=len(payload_classes),
        payload_classes=payload_classes,
    )
