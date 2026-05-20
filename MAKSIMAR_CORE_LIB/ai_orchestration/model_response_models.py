from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelResponseModel:
    response_id: str
    request_id: str
    selected_model: str
    response_summary: str
    response_ready: bool
    tool_call_allowed: bool
    execution_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("response_id", self.response_id)
        _validate_non_empty("request_id", self.request_id)
        _validate_non_empty("selected_model", self.selected_model)
        _validate_non_empty("response_summary", self.response_summary)
        _validate_true("response_ready", self.response_ready)
        _validate_false("tool_call_allowed", self.tool_call_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_id": self.response_id,
            "request_id": self.request_id,
            "selected_model": self.selected_model,
            "response_summary": self.response_summary,
            "response_ready": self.response_ready,
            "tool_call_allowed": self.tool_call_allowed,
            "execution_allowed": self.execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_model_response_model() -> ModelResponseModel:
    return ModelResponseModel(
        response_id="model_response_v1",
        request_id="model_request_v1",
        selected_model="existing_router_selected_model",
        response_summary="dashboard safe model response summary",
        response_ready=True,
        tool_call_allowed=False,
        execution_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_response_dashboard_safe",
            "tool_call_blocked_by_default",
            "execution_blocked_by_default",
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
