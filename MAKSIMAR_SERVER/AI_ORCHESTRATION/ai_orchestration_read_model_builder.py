from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    AIOrchestrationReadModel,
    build_default_ai_orchestration_read_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.adapters import (
    AIServicesAdapterReadModel,
    ControlPlaneAIRouterAdapterReadModel,
    WorkersAdapterReadModel,
    build_ai_services_adapter_read_model,
    build_control_plane_ai_router_adapter_read_model,
    build_workers_adapter_read_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ai_orchestration_health import (
    AIOrchestrationHealthReadModel,
    build_ai_orchestration_health_read_model,
)


@dataclass(frozen=True, slots=True)
class AIOrchestrationRuntimeReadModel:
    read_model_id: str
    core_read_model: AIOrchestrationReadModel
    ai_services_adapter: AIServicesAdapterReadModel
    workers_adapter: WorkersAdapterReadModel
    control_plane_router_adapter: ControlPlaneAIRouterAdapterReadModel
    health: AIOrchestrationHealthReadModel
    proposal_only: bool
    runtime_mutation_allowed: bool
    deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.core_read_model, AIOrchestrationReadModel):
            raise TypeError("core_read_model must be AIOrchestrationReadModel")
        if not isinstance(self.ai_services_adapter, AIServicesAdapterReadModel):
            raise TypeError("ai_services_adapter must be AIServicesAdapterReadModel")
        if not isinstance(self.workers_adapter, WorkersAdapterReadModel):
            raise TypeError("workers_adapter must be WorkersAdapterReadModel")
        if not isinstance(self.control_plane_router_adapter, ControlPlaneAIRouterAdapterReadModel):
            raise TypeError("control_plane_router_adapter must be ControlPlaneAIRouterAdapterReadModel")
        if not isinstance(self.health, AIOrchestrationHealthReadModel):
            raise TypeError("health must be AIOrchestrationHealthReadModel")
        _validate_true("proposal_only", self.proposal_only)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("deployment_allowed", self.deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "core_read_model": self.core_read_model.to_dict(),
            "ai_services_adapter": self.ai_services_adapter.to_dict(),
            "workers_adapter": self.workers_adapter.to_dict(),
            "control_plane_router_adapter": self.control_plane_router_adapter.to_dict(),
            "health": self.health.to_dict(),
            "proposal_only": self.proposal_only,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_orchestration_runtime_read_model() -> AIOrchestrationRuntimeReadModel:
    return AIOrchestrationRuntimeReadModel(
        read_model_id="ai_orchestration_runtime_read_model_v1",
        core_read_model=build_default_ai_orchestration_read_model(),
        ai_services_adapter=build_ai_services_adapter_read_model(),
        workers_adapter=build_workers_adapter_read_model(),
        control_plane_router_adapter=build_control_plane_ai_router_adapter_read_model(),
        health=build_ai_orchestration_health_read_model(),
        proposal_only=True,
        runtime_mutation_allowed=False,
        deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_orchestration_runtime_read_model_dashboard_safe",
            "adapters_point_to_existing_services",
            "proposal_only",
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
