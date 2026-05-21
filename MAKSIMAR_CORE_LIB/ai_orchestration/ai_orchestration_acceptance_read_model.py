from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.ai_orchestration_read_model import (
    AIOrchestrationReadModel,
    build_default_ai_orchestration_read_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.ai_router_binding_contract import (
    AIRouterBindingContract,
    build_ai_router_binding_contract,
)


@dataclass(frozen=True, slots=True)
class AIOrchestrationAcceptanceReadModel:
    read_model_id: str
    ai_orchestration_read_model: AIOrchestrationReadModel
    ai_router_binding_contract: AIRouterBindingContract
    ai_services_accounted: bool
    workers_accounted: bool
    ai_router_binding_accounted: bool
    manifest_present: bool
    proposal_only: bool
    direct_execution_blocked: bool
    action_library_direct_execution_allowed: bool
    workflow_engine_direct_execution_allowed: bool
    runtime_mutation_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    acceptance_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.ai_orchestration_read_model, AIOrchestrationReadModel):
            raise TypeError("ai_orchestration_read_model must be AIOrchestrationReadModel")
        if not isinstance(self.ai_router_binding_contract, AIRouterBindingContract):
            raise TypeError("ai_router_binding_contract must be AIRouterBindingContract")

        _validate_true("ai_services_accounted", self.ai_services_accounted)
        _validate_true("workers_accounted", self.workers_accounted)
        _validate_true("ai_router_binding_accounted", self.ai_router_binding_accounted)
        _validate_true("manifest_present", self.manifest_present)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("direct_execution_blocked", self.direct_execution_blocked)

        _validate_false("action_library_direct_execution_allowed", self.action_library_direct_execution_allowed)
        _validate_false("workflow_engine_direct_execution_allowed", self.workflow_engine_direct_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)

        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_true("acceptance_ready", self.acceptance_ready)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "ai_orchestration_read_model": self.ai_orchestration_read_model.to_dict(),
            "ai_router_binding_contract": self.ai_router_binding_contract.to_dict(),
            "ai_services_accounted": self.ai_services_accounted,
            "workers_accounted": self.workers_accounted,
            "ai_router_binding_accounted": self.ai_router_binding_accounted,
            "manifest_present": self.manifest_present,
            "proposal_only": self.proposal_only,
            "direct_execution_blocked": self.direct_execution_blocked,
            "action_library_direct_execution_allowed": self.action_library_direct_execution_allowed,
            "workflow_engine_direct_execution_allowed": self.workflow_engine_direct_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "acceptance_ready": self.acceptance_ready,
            "reason_codes": self.reason_codes,
        }


def build_ai_orchestration_acceptance_read_model() -> AIOrchestrationAcceptanceReadModel:
    return AIOrchestrationAcceptanceReadModel(
        read_model_id="ai_orchestration_acceptance_read_model_v1",
        ai_orchestration_read_model=build_default_ai_orchestration_read_model(),
        ai_router_binding_contract=build_ai_router_binding_contract(),
        ai_services_accounted=True,
        workers_accounted=True,
        ai_router_binding_accounted=True,
        manifest_present=True,
        proposal_only=True,
        direct_execution_blocked=True,
        action_library_direct_execution_allowed=False,
        workflow_engine_direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        acceptance_ready=True,
        reason_codes=(
            "ai_orchestration_foundation_acceptance_ready",
            "ai_remains_proposal_only",
            "existing_ai_services_accounted",
            "existing_workers_accounted",
            "existing_ai_router_binding_accounted",
            "direct_execution_blocked",
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
