from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ValidationErrorCode = Literal[
    "invalid_header",
    "invalid_schema",
    "forbidden_payload_embedding",
    "missing_payload_reference",
    "deep_validation_failed",
    "policy_rule_not_found",
]

ValidationErrorCategory = Literal[
    "header",
    "schema",
    "payload",
    "deep_validation",
    "policy",
]

ValidationErrorSeverity = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


@dataclass(frozen=True, slots=True)
class ValidationErrorEntry:
    """Canonical validation error description entry."""

    error_code: ValidationErrorCode
    category: ValidationErrorCategory
    severity: ValidationErrorSeverity
    retryable: bool
    terminal: bool
    description: str

    def __post_init__(self) -> None:
        """Validate validation error invariants."""
        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.error_code}")

        if self.terminal and self.retryable:
            raise ValueError(
                f"terminal validation error must not be retryable: {self.error_code}"
            )

        if self.error_code == "invalid_header":
            if self.category != "header":
                raise ValueError("invalid_header must use category='header'")
            if self.severity != "medium":
                raise ValueError("invalid_header must use severity='medium'")
            if self.retryable:
                raise ValueError("invalid_header must not be retryable")
            if not self.terminal:
                raise ValueError("invalid_header must be terminal")

        if self.error_code == "invalid_schema":
            if self.category != "schema":
                raise ValueError("invalid_schema must use category='schema'")
            if self.severity != "high":
                raise ValueError("invalid_schema must use severity='high'")
            if self.retryable:
                raise ValueError("invalid_schema must not be retryable")
            if not self.terminal:
                raise ValueError("invalid_schema must be terminal")

        if self.error_code == "forbidden_payload_embedding":
            if self.category != "payload":
                raise ValueError(
                    "forbidden_payload_embedding must use category='payload'"
                )
            if self.severity != "high":
                raise ValueError(
                    "forbidden_payload_embedding must use severity='high'"
                )
            if self.retryable:
                raise ValueError(
                    "forbidden_payload_embedding must not be retryable"
                )
            if not self.terminal:
                raise ValueError("forbidden_payload_embedding must be terminal")

        if self.error_code == "missing_payload_reference":
            if self.category != "payload":
                raise ValueError("missing_payload_reference must use category='payload'")
            if self.severity != "high":
                raise ValueError("missing_payload_reference must use severity='high'")
            if self.retryable:
                raise ValueError("missing_payload_reference must not be retryable")
            if not self.terminal:
                raise ValueError("missing_payload_reference must be terminal")

        if self.error_code == "deep_validation_failed":
            if self.category != "deep_validation":
                raise ValueError(
                    "deep_validation_failed must use category='deep_validation'"
                )
            if self.severity != "critical":
                raise ValueError("deep_validation_failed must use severity='critical'")
            if self.retryable:
                raise ValueError("deep_validation_failed must not be retryable")
            if not self.terminal:
                raise ValueError("deep_validation_failed must be terminal")

        if self.error_code == "policy_rule_not_found":
            if self.category != "policy":
                raise ValueError("policy_rule_not_found must use category='policy'")
            if self.severity != "critical":
                raise ValueError("policy_rule_not_found must use severity='critical'")
            if self.retryable:
                raise ValueError("policy_rule_not_found must not be retryable")
            if not self.terminal:
                raise ValueError("policy_rule_not_found must be terminal")


@dataclass(frozen=True, slots=True)
class ValidationErrorContract:
    """Unified canonical validation error contract."""

    total_errors: int
    errors: tuple[ValidationErrorEntry, ...]


def build_validation_error_contract() -> ValidationErrorContract:
    """Build canonical validation error contract."""
    errors = (
        ValidationErrorEntry(
            error_code="invalid_header",
            category="header",
            severity="medium",
            retryable=False,
            terminal=True,
            description="Header validation failed and request must be rejected.",
        ),
        ValidationErrorEntry(
            error_code="invalid_schema",
            category="schema",
            severity="high",
            retryable=False,
            terminal=True,
            description="Schema or type validation failed and request must be rejected.",
        ),
        ValidationErrorEntry(
            error_code="forbidden_payload_embedding",
            category="payload",
            severity="high",
            retryable=False,
            terminal=True,
            description="Payload embedding violated routing rules and must be rejected.",
        ),
        ValidationErrorEntry(
            error_code="missing_payload_reference",
            category="payload",
            severity="high",
            retryable=False,
            terminal=True,
            description="Required payload reference is missing for referenced validation flow.",
        ),
        ValidationErrorEntry(
            error_code="deep_validation_failed",
            category="deep_validation",
            severity="critical",
            retryable=False,
            terminal=True,
            description="Deep/domain validation failed and execution must be blocked.",
        ),
        ValidationErrorEntry(
            error_code="policy_rule_not_found",
            category="policy",
            severity="critical",
            retryable=False,
            terminal=True,
            description="Validation policy rule could not be resolved for request.",
        ),
    )

    error_codes = tuple(entry.error_code for entry in errors)

    if len(set(error_codes)) != len(error_codes):
        raise ValueError("Duplicate validation error codes detected")

    expected_order = (
        "invalid_header",
        "invalid_schema",
        "forbidden_payload_embedding",
        "missing_payload_reference",
        "deep_validation_failed",
        "policy_rule_not_found",
    )
    if error_codes != expected_order:
        raise ValueError("Validation error code order is invalid")

    return ValidationErrorContract(
        total_errors=len(errors),
        errors=errors,
    )
