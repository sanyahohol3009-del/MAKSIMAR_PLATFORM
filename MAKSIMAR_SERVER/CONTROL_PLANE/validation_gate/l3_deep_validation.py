from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
)


@dataclass(frozen=True, slots=True)
class L3DeepValidationInput:
    """Server-side L3 deep validation input."""

    deep_validation_required: bool
    execution_side_effects_possible: bool
    domain_policy_ack: bool
    safety_context_present: bool


@dataclass(frozen=True, slots=True)
class L3DeepValidationResult:
    """Server-side L3 deep validation result."""

    executed: bool
    passed: bool
    error_code: ValidationErrorCode | str
    reason: str

    def __post_init__(self) -> None:
        """Validate L3 result invariants."""
        if not self.reason.strip():
            raise ValueError("L3 reason must not be empty")

        if not self.executed:
            if self.passed:
                raise ValueError("Non-executed L3 validation must not pass")
            if self.error_code != "":
                raise ValueError("Non-executed L3 validation must not set error_code")

        if self.executed and self.passed and self.error_code != "":
            raise ValueError("Passed L3 validation must not set error_code")

        if self.executed and not self.passed and self.error_code == "":
            raise ValueError("Failed L3 validation must set error_code")


def validate_l3_deep(
    *,
    request: L3DeepValidationInput,
) -> L3DeepValidationResult:
    """Validate deep/domain requirements for execution-critical paths."""
    if not request.deep_validation_required:
        return L3DeepValidationResult(
            executed=False,
            passed=False,
            error_code="",
            reason="l3_not_required",
        )

    if request.execution_side_effects_possible:
        if not request.domain_policy_ack:
            return L3DeepValidationResult(
                executed=True,
                passed=False,
                error_code="deep_validation_failed",
                reason="domain_policy_ack_missing",
            )
        if not request.safety_context_present:
            return L3DeepValidationResult(
                executed=True,
                passed=False,
                error_code="deep_validation_failed",
                reason="safety_context_missing",
            )

    return L3DeepValidationResult(
        executed=True,
        passed=True,
        error_code="",
        reason="l3_deep_valid",
    )
