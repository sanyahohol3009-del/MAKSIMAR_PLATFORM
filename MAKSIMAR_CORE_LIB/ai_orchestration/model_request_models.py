from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelRequestModel:
    request_id: str
    requested_capability: str
    requester_id: str
    input_reference: str
    tool_call_requested: bool
    direct_action_requested: bool
    workflow_execution_requested: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("request_id", self.request_id)
        _validate_non_empty("requested_capability", self.requested_capability)
        _validate_non_empty("requester_id", self.requester_id)
        _validate_non_empty("input_reference", self.input_reference)
        _validate_false("direct_action_requested", self.direct_action_requested)
        _validate_false("workflow_execution_requested", self.workflow_execution_requested)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "requested_capability": self.requested_capability,
            "requester_id": self.requester_id,
            "input_reference": self.input_reference,
            "tool_call_requested": self.tool_call_requested,
            "direct_action_requested": self.direct_action_requested,
            "workflow_execution_requested": self.workflow_execution_requested,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_model_request_model() -> ModelRequestModel:
    return ModelRequestModel(
        request_id="model_request_v1",
        requested_capability="general_reasoning",
        requester_id="ai_orchestration_surface",
        input_reference="request_payload_ref",
        tool_call_requested=False,
        direct_action_requested=False,
        workflow_execution_requested=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_request_dashboard_safe",
            "direct_action_not_requested",
            "workflow_execution_not_requested",
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
