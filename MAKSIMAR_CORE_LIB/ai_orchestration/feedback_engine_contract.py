from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class FeedbackEngineContract:
    feedback_id: str
    feedback_source: str
    feedback_reference: str
    feedback_read_model_input_only: bool
    feedback_ready: bool
    autonomous_learning_mutation_allowed: bool
    runtime_model_update_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("feedback_id", self.feedback_id)
        _validate_non_empty("feedback_source", self.feedback_source)
        _validate_non_empty("feedback_reference", self.feedback_reference)
        _validate_true("feedback_read_model_input_only", self.feedback_read_model_input_only)
        _validate_true("feedback_ready", self.feedback_ready)
        _validate_false("autonomous_learning_mutation_allowed", self.autonomous_learning_mutation_allowed)
        _validate_false("runtime_model_update_allowed", self.runtime_model_update_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "feedback_id": self.feedback_id,
            "feedback_source": self.feedback_source,
            "feedback_reference": self.feedback_reference,
            "feedback_read_model_input_only": self.feedback_read_model_input_only,
            "feedback_ready": self.feedback_ready,
            "autonomous_learning_mutation_allowed": self.autonomous_learning_mutation_allowed,
            "runtime_model_update_allowed": self.runtime_model_update_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_feedback_engine_contract() -> FeedbackEngineContract:
    return FeedbackEngineContract(
        feedback_id="feedback_engine_contract_v1",
        feedback_source="operator_review_feedback",
        feedback_reference="feedback_payload_ref",
        feedback_read_model_input_only=True,
        feedback_ready=True,
        autonomous_learning_mutation_allowed=False,
        runtime_model_update_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "feedback_contract_only",
            "autonomous_learning_mutation_blocked",
            "runtime_model_update_blocked",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
