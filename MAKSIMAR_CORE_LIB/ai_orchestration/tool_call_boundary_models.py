from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolCallBoundaryModel:
    boundary_id: str
    proposal_boundary_only: bool
    tool_call_requested: bool
    tool_call_allowed: bool
    execution_allowed: bool
    action_library_execution_allowed: bool
    workflow_engine_execution_allowed: bool
    direct_autonomous_execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("boundary_id", self.boundary_id)
        _validate_true("proposal_boundary_only", self.proposal_boundary_only)
        _validate_false("tool_call_allowed", self.tool_call_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("action_library_execution_allowed", self.action_library_execution_allowed)
        _validate_false("workflow_engine_execution_allowed", self.workflow_engine_execution_allowed)
        _validate_false("direct_autonomous_execution_allowed", self.direct_autonomous_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "proposal_boundary_only": self.proposal_boundary_only,
            "tool_call_requested": self.tool_call_requested,
            "tool_call_allowed": self.tool_call_allowed,
            "execution_allowed": self.execution_allowed,
            "action_library_execution_allowed": self.action_library_execution_allowed,
            "workflow_engine_execution_allowed": self.workflow_engine_execution_allowed,
            "direct_autonomous_execution_allowed": self.direct_autonomous_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_tool_call_boundary_model(
    *,
    tool_call_requested: bool = False,
) -> ToolCallBoundaryModel:
    return ToolCallBoundaryModel(
        boundary_id="tool_call_boundary_v1",
        proposal_boundary_only=True,
        tool_call_requested=tool_call_requested,
        tool_call_allowed=False,
        execution_allowed=False,
        action_library_execution_allowed=False,
        workflow_engine_execution_allowed=False,
        direct_autonomous_execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "tool_call_boundary_proposal_only",
            "tool_call_blocked_by_default",
            "action_library_execution_blocked",
            "workflow_engine_execution_blocked",
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
