from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ValidationTier = Literal[
    "L1_HEADER",
    "L2_SCHEMA",
    "L3_DEEP",
]


@dataclass(frozen=True, slots=True)
class ValidationTierEntry:
    """Canonical validation tier description entry."""

    tier_id: ValidationTier
    tier_order: int
    header_validation_required: bool
    schema_validation_required: bool
    deep_validation_required: bool
    payload_reference_enforcement_required: bool
    description: str

    def __post_init__(self) -> None:
        """Validate validation tier invariants."""
        if self.tier_order < 0:
            raise ValueError(f"tier_order must be non-negative for {self.tier_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.tier_id}")

        if self.tier_id == "L1_HEADER":
            if self.tier_order != 0:
                raise ValueError("L1_HEADER must use tier_order=0")
            if not self.header_validation_required:
                raise ValueError("L1_HEADER must require header validation")
            if self.schema_validation_required:
                raise ValueError("L1_HEADER must not require schema validation")
            if self.deep_validation_required:
                raise ValueError("L1_HEADER must not require deep validation")
            if self.payload_reference_enforcement_required:
                raise ValueError(
                    "L1_HEADER must not require payload reference enforcement"
                )

        if self.tier_id == "L2_SCHEMA":
            if self.tier_order != 1:
                raise ValueError("L2_SCHEMA must use tier_order=1")
            if not self.header_validation_required:
                raise ValueError("L2_SCHEMA must require header validation")
            if not self.schema_validation_required:
                raise ValueError("L2_SCHEMA must require schema validation")
            if self.deep_validation_required:
                raise ValueError("L2_SCHEMA must not require deep validation")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "L2_SCHEMA must require payload reference enforcement"
                )

        if self.tier_id == "L3_DEEP":
            if self.tier_order != 2:
                raise ValueError("L3_DEEP must use tier_order=2")
            if not self.header_validation_required:
                raise ValueError("L3_DEEP must require header validation")
            if not self.schema_validation_required:
                raise ValueError("L3_DEEP must require schema validation")
            if not self.deep_validation_required:
                raise ValueError("L3_DEEP must require deep validation")
            if not self.payload_reference_enforcement_required:
                raise ValueError(
                    "L3_DEEP must require payload reference enforcement"
                )


@dataclass(frozen=True, slots=True)
class ValidationTierContract:
    """Unified canonical validation tier contract."""

    total_tiers: int
    tiers: tuple[ValidationTierEntry, ...]


def build_validation_tier_contract() -> ValidationTierContract:
    """Build canonical validation tier contract."""
    tiers = (
        ValidationTierEntry(
            tier_id="L1_HEADER",
            tier_order=0,
            header_validation_required=True,
            schema_validation_required=False,
            deep_validation_required=False,
            payload_reference_enforcement_required=False,
            description="Header-only validation for fast structural admission checks.",
        ),
        ValidationTierEntry(
            tier_id="L2_SCHEMA",
            tier_order=1,
            header_validation_required=True,
            schema_validation_required=True,
            deep_validation_required=False,
            payload_reference_enforcement_required=True,
            description="Schema/type validation with payload reference enforcement.",
        ),
        ValidationTierEntry(
            tier_id="L3_DEEP",
            tier_order=2,
            header_validation_required=True,
            schema_validation_required=True,
            deep_validation_required=True,
            payload_reference_enforcement_required=True,
            description="Deep/domain validation for high-risk or execution-critical paths.",
        ),
    )

    tier_ids = tuple(entry.tier_id for entry in tiers)
    tier_orders = tuple(entry.tier_order for entry in tiers)

    if tier_ids != ("L1_HEADER", "L2_SCHEMA", "L3_DEEP"):
        raise ValueError("Validation tier order is invalid")

    if tier_orders != (0, 1, 2):
        raise ValueError("Validation tier numeric order is invalid")

    if len(set(tier_ids)) != len(tier_ids):
        raise ValueError("Duplicate validation tiers detected")

    if len(set(tier_orders)) != len(tier_orders):
        raise ValueError("Duplicate validation tier orders detected")

    return ValidationTierContract(
        total_tiers=len(tiers),
        tiers=tiers,
    )
