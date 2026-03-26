from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.payload_builders import (
    build_payload_envelope,
)
from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
    ValidationTaskClass,
    ValidationTier,
    build_validation_plan,
)


@dataclass(frozen=True, slots=True)
class L2SchemaValidationInput:
    """Server-side L2 schema validation input."""

    task_class: ValidationTaskClass
    payload_class: PayloadClass
    payload_size_kb: int
    artifact_ref: str
    owner_task_id: str


@dataclass(frozen=True, slots=True)
class L2SchemaValidationResult:
    """Server-side L2 schema validation result."""

    passed: bool
    resolved_validation_tier: ValidationTier | str
    deep_validation_required: bool
    execution_side_effects_possible: bool
    error_code: ValidationErrorCode | str
    reason: str

    def __post_init__(self) -> None:
        """Validate L2 result invariants."""
        if not self.reason.strip():
            raise ValueError("L2 reason must not be empty")

        if self.passed:
            if self.error_code != "":
                raise ValueError("Passed L2 validation must not set error_code")
            if self.resolved_validation_tier == "":
                raise ValueError(
                    "Passed L2 validation must set resolved_validation_tier"
                )

        if not self.passed:
            if self.error_code == "":
                raise ValueError("Failed L2 validation must set error_code")


def _map_payload_validation_reason_to_error_code(
    *,
    reason: str,
) -> ValidationErrorCode:
    """Map payload validation reason to canonical validation error code."""
    if reason == "artifact_reference_required":
        return "missing_payload_reference"
    if reason == "owner_task_id_required":
        return "missing_payload_reference"
    if reason == "payload_exceeds_inline_limit":
        return "forbidden_payload_embedding"
    return "invalid_schema"


def validate_l2_schema(
    *,
    request: L2SchemaValidationInput,
) -> L2SchemaValidationResult:
    """Validate schema/payload policy and resolve validation tier."""
    try:
        plan = build_validation_plan(
            task_class=request.task_class,
            payload_class=request.payload_class,
        )
    except ValueError:
        return L2SchemaValidationResult(
            passed=False,
            resolved_validation_tier="",
            deep_validation_required=False,
            execution_side_effects_possible=False,
            error_code="policy_rule_not_found",
            reason="validation_policy_rule_missing",
        )

    payload_envelope = build_payload_envelope(
        payload_class=request.payload_class,
        payload_size_kb=request.payload_size_kb,
        artifact_ref=request.artifact_ref,
        owner_task_id=request.owner_task_id,
    )

    if not payload_envelope.valid:
        return L2SchemaValidationResult(
            passed=False,
            resolved_validation_tier=plan.required_validation_tier,
            deep_validation_required=plan.deep_validation_required,
            execution_side_effects_possible=plan.execution_side_effects_possible,
            error_code=_map_payload_validation_reason_to_error_code(
                reason=payload_envelope.validation_reason,
            ),
            reason=payload_envelope.validation_reason,
        )

    if (
        plan.payload_reference_enforcement_required
        and request.payload_class == "heavy_artifact"
        and not request.artifact_ref.strip()
    ):
        return L2SchemaValidationResult(
            passed=False,
            resolved_validation_tier=plan.required_validation_tier,
            deep_validation_required=plan.deep_validation_required,
            execution_side_effects_possible=plan.execution_side_effects_possible,
            error_code="missing_payload_reference",
            reason="payload_reference_missing_after_plan_resolution",
        )

    return L2SchemaValidationResult(
        passed=True,
        resolved_validation_tier=plan.required_validation_tier,
        deep_validation_required=plan.deep_validation_required,
        execution_side_effects_possible=plan.execution_side_effects_possible,
        error_code="",
        reason="l2_schema_valid",
    )
