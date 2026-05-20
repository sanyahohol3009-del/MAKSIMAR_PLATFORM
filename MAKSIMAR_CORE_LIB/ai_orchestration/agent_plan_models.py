from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.tool_call_boundary_models import (
    ToolCallBoundaryModel,
    build_default_tool_call_boundary_model,
)


@dataclass(frozen=True, slots=True)
class AgentPlanModel:
    plan_id: str
    request_id: str
    plan_steps: tuple[str, ...]
    proposal_only: bool
    tool_call_boundary: ToolCallBoundaryModel
    execution_allowed: bool
    action_library_execution_allowed: bool
    workflow_engine_execution_allowed: bool
    direct_autonomous_execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("plan_id", self.plan_id)
        _validate_non_empty("request_id", self.request_id)
        _validate_non_empty_tuple("plan_steps", self.plan_steps)
        _validate_true("proposal_only", self.proposal_only)
        if not isinstance(self.tool_call_boundary, ToolCallBoundaryModel):
            raise TypeError("tool_call_boundary must be ToolCallBoundaryModel")
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
            "plan_id": self.plan_id,
            "request_id": self.request_id,
            "plan_steps": self.plan_steps,
            "proposal_only": self.proposal_only,
            "tool_call_boundary": self.tool_call_boundary.to_dict(),
            "execution_allowed": self.execution_allowed,
            "action_library_execution_allowed": self.action_library_execution_allowed,
            "workflow_engine_execution_allowed": self.workflow_engine_execution_allowed,
            "direct_autonomous_execution_allowed": self.direct_autonomous_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_agent_plan_model() -> AgentPlanModel:
    return AgentPlanModel(
        plan_id="agent_plan_v1",
        request_id="model_request_v1",
        plan_steps=("inspect_request", "select_existing_model_route", "return_read_model"),
        proposal_only=True,
        tool_call_boundary=build_default_tool_call_boundary_model(),
        execution_allowed=False,
        action_library_execution_allowed=False,
        workflow_engine_execution_allowed=False,
        direct_autonomous_execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "agent_plan_proposal_only",
            "execution_blocked_by_default",
            "runtime_mutation_blocked",
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
