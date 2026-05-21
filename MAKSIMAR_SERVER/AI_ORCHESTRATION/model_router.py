from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    ModelRouterContract,
    ModelRouterReadModel,
    build_model_router_contract,
)


@dataclass(frozen=True, slots=True)
class AIOrchestrationModelRouterRuntimeReadModel:
    runtime_id: str
    router_contract: ModelRouterContract
    router_read_model: ModelRouterReadModel
    points_to_existing_router_binding: bool
    model_runtime_execution_allowed: bool
    route_execution_allowed: bool
    runtime_mutation_allowed: bool
    proposal_only: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("runtime_id", self.runtime_id)
        if not isinstance(self.router_contract, ModelRouterContract):
            raise TypeError("router_contract must be ModelRouterContract")
        if not isinstance(self.router_read_model, ModelRouterReadModel):
            raise TypeError("router_read_model must be ModelRouterReadModel")
        _validate_true("points_to_existing_router_binding", self.points_to_existing_router_binding)
        _validate_false("model_runtime_execution_allowed", self.model_runtime_execution_allowed)
        _validate_false("route_execution_allowed", self.route_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_id": self.runtime_id,
            "router_contract": self.router_contract.to_dict(),
            "router_read_model": self.router_read_model.to_dict(),
            "points_to_existing_router_binding": self.points_to_existing_router_binding,
            "model_runtime_execution_allowed": self.model_runtime_execution_allowed,
            "route_execution_allowed": self.route_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "proposal_only": self.proposal_only,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_orchestration_model_router_runtime_read_model() -> AIOrchestrationModelRouterRuntimeReadModel:
    contract = build_model_router_contract()
    return AIOrchestrationModelRouterRuntimeReadModel(
        runtime_id="ai_orchestration_model_router_runtime_v1",
        router_contract=contract,
        router_read_model=contract.read_model,
        points_to_existing_router_binding=True,
        model_runtime_execution_allowed=False,
        route_execution_allowed=False,
        runtime_mutation_allowed=False,
        proposal_only=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "runtime_facade_points_to_existing_router_binding",
            "model_runtime_execution_blocked",
            "proposal_only",
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
