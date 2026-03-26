from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
    ValidationTaskClass,
)


_ALLOWED_TASK_CLASSES: set[str] = {
    "chat_request",
    "simulation_request",
    "robotics_action",
    "media_job",
    "evaluation_job",
    "automation_job",
}

_ALLOWED_PAYLOAD_CLASSES: set[str] = {
    "small_control",
    "medium_contract",
    "heavy_artifact",
}


@dataclass(frozen=True, slots=True)
class L1HeaderValidationInput:
    """Server-side L1 header validation input."""

    request_id: str
    task_class: ValidationTaskClass | str
    payload_class: PayloadClass | str


@dataclass(frozen=True, slots=True)
class L1HeaderValidationResult:
    """Server-side L1 header validation result."""

    passed: bool
    error_code: ValidationErrorCode | str
    reason: str

    def __post_init__(self) -> None:
        """Validate L1 result invariants."""
        if not self.reason.strip():
            raise ValueError("L1 reason must not be empty")

        if self.passed and self.error_code != "":
            raise ValueError("Passed L1 validation must not set error_code")

        if not self.passed and self.error_code == "":
            raise ValueError("Failed L1 validation must set error_code")


def validate_l1_header(
    *,
    request: L1HeaderValidationInput,
) -> L1HeaderValidationResult:
    """Validate header-level request metadata."""
    if not request.request_id.strip():
        return L1HeaderValidationResult(
            passed=False,
            error_code="invalid_header",
            reason="request_id_missing",
        )

    if str(request.task_class) not in _ALLOWED_TASK_CLASSES:
        return L1HeaderValidationResult(
            passed=False,
            error_code="invalid_header",
            reason="task_class_invalid",
        )

    if str(request.payload_class) not in _ALLOWED_PAYLOAD_CLASSES:
        return L1HeaderValidationResult(
            passed=False,
            error_code="invalid_header",
            reason="payload_class_invalid",
        )

    return L1HeaderValidationResult(
        passed=True,
        error_code="",
        reason="l1_header_valid",
    )
