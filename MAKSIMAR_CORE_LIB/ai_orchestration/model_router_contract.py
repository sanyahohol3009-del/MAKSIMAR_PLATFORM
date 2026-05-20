from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.agent_plan_models import (
    AgentPlanModel,
    build_default_agent_plan_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_request_models import (
    ModelRequestModel,
    build_default_model_request_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_response_models import (
    ModelResponseModel,
    build_default_model_response_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.tool_call_boundary_models import (
    ToolCallBoundaryModel,
    build_default_tool_call_boundary_model,
)


@dataclass(frozen=True, slots=True)
class ModelRouterReadModel:
    request_id: str
    requested_capability: str
    selected_model: str
    model_route_reason: str
    tool_call_requested: bool
    tool_call_allowed: bool
    execution_allowed: bool
    direct_action_execution_allowed: bool
    workflow_engine_execution_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("request_id", self.request_id)
        _validate_non_empty("requested_capability", self.requested_capability)
        _validate_non_empty("selected_model", self.selected_model)
        _validate_non_empty("model_route_reason", self.model_route_reason)
        _validate_false("tool_call_allowed", self.tool_call_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("direct_action_execution_allowed", self.direct_action_execution_allowed)
        _validate_false("workflow_engine_execution_allowed", self.workflow_engine_execution_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "requested_capability": self.requested_capability,
            "selected_model": self.selected_model,
            "model_route_reason": self.model_route_reason,
            "tool_call_requested": self.tool_call_requested,
            "tool_call_allowed": self.tool_call_allowed,
            "execution_allowed": self.execution_allowed,
            "direct_action_execution_allowed": self.direct_action_execution_allowed,
            "workflow_engine_execution_allowed": self.workflow_engine_execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class ModelRouterContract:
    contract_id: str
    request: ModelRequestModel
    response: ModelResponseModel
    agent_plan: AgentPlanModel
    tool_call_boundary: ToolCallBoundaryModel
    read_model: ModelRouterReadModel
    contract_only: bool
    execution_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("contract_id", self.contract_id)
        if not isinstance(self.request, ModelRequestModel):
            raise TypeError("request must be ModelRequestModel")
        if not isinstance(self.response, ModelResponseModel):
            raise TypeError("response must be ModelResponseModel")
        if not isinstance(self.agent_plan, AgentPlanModel):
            raise TypeError("agent_plan must be AgentPlanModel")
        if not isinstance(self.tool_call_boundary, ToolCallBoundaryModel):
            raise TypeError("tool_call_boundary must be ToolCallBoundaryModel")
        if not isinstance(self.read_model, ModelRouterReadModel):
            raise TypeError("read_model must be ModelRouterReadModel")
        _validate_true("contract_only", self.contract_only)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "request": self.request.to_dict(),
            "response": self.response.to_dict(),
            "agent_plan": self.agent_plan.to_dict(),
            "tool_call_boundary": self.tool_call_boundary.to_dict(),
            "read_model": self.read_model.to_dict(),
            "contract_only": self.contract_only,
            "execution_allowed": self.execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_model_router_read_model(
    request: ModelRequestModel | None = None,
) -> ModelRouterReadModel:
    resolved_request = build_default_model_request_model() if request is None else request
    if not isinstance(resolved_request, ModelRequestModel):
        raise TypeError("request must be ModelRequestModel")

    return ModelRouterReadModel(
        request_id=resolved_request.request_id,
        requested_capability=resolved_request.requested_capability,
        selected_model="existing_ai_router_selected_model",
        model_route_reason="existing_ai_router_binding_reference",
        tool_call_requested=resolved_request.tool_call_requested,
        tool_call_allowed=False,
        execution_allowed=False,
        direct_action_execution_allowed=False,
        workflow_engine_execution_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_router_contract_read_model_only",
            "tool_call_blocked_by_default",
            "execution_blocked_by_default",
        ),
    )


def build_model_router_contract() -> ModelRouterContract:
    request = build_default_model_request_model()
    return ModelRouterContract(
        contract_id="model_router_contract_v1",
        request=request,
        response=build_default_model_response_model(),
        agent_plan=build_default_agent_plan_model(),
        tool_call_boundary=build_default_tool_call_boundary_model(
            tool_call_requested=request.tool_call_requested,
        ),
        read_model=build_model_router_read_model(request),
        contract_only=True,
        execution_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_router_contract_only",
            "no_direct_action_execution",
            "no_workflow_engine_execution",
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
