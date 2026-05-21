from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AIOrchestrationFoundationReadinessModel:
    readiness_id: str
    security_layer_green: bool
    data_plane_green: bool
    update_recovery_green: bool
    network_containerization_green: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("readiness_id", self.readiness_id)
        _validate_true("security_layer_green", self.security_layer_green)
        _validate_true("data_plane_green", self.data_plane_green)
        _validate_true("update_recovery_green", self.update_recovery_green)
        _validate_true("network_containerization_green", self.network_containerization_green)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    @property
    def all_required_foundations_green(self) -> bool:
        return (
            self.security_layer_green
            and self.data_plane_green
            and self.update_recovery_green
            and self.network_containerization_green
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "readiness_id": self.readiness_id,
            "security_layer_green": self.security_layer_green,
            "data_plane_green": self.data_plane_green,
            "update_recovery_green": self.update_recovery_green,
            "network_containerization_green": self.network_containerization_green,
            "all_required_foundations_green": self.all_required_foundations_green,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class AIOrchestrationPolicy:
    policy_id: str
    foundation_readiness: AIOrchestrationFoundationReadinessModel
    may_propose: bool
    may_apply: bool
    direct_action_execution_allowed: bool
    workflow_engine_execution_allowed: bool
    direct_autonomous_execution_allowed: bool
    runtime_mutation_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("policy_id", self.policy_id)
        if not isinstance(self.foundation_readiness, AIOrchestrationFoundationReadinessModel):
            raise TypeError("foundation_readiness must be AIOrchestrationFoundationReadinessModel")
        if not self.foundation_readiness.all_required_foundations_green:
            raise ValueError("all required foundations must remain green")
        _validate_true("may_propose", self.may_propose)
        _validate_false("may_apply", self.may_apply)
        _validate_false("direct_action_execution_allowed", self.direct_action_execution_allowed)
        _validate_false("workflow_engine_execution_allowed", self.workflow_engine_execution_allowed)
        _validate_false("direct_autonomous_execution_allowed", self.direct_autonomous_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "foundation_readiness": self.foundation_readiness.to_dict(),
            "may_propose": self.may_propose,
            "may_apply": self.may_apply,
            "direct_action_execution_allowed": self.direct_action_execution_allowed,
            "workflow_engine_execution_allowed": self.workflow_engine_execution_allowed,
            "direct_autonomous_execution_allowed": self.direct_autonomous_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_ai_orchestration_foundation_readiness_model() -> AIOrchestrationFoundationReadinessModel:
    return AIOrchestrationFoundationReadinessModel(
        readiness_id="ai_orchestration_foundation_readiness_v1",
        security_layer_green=True,
        data_plane_green=True,
        update_recovery_green=True,
        network_containerization_green=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "security_layer_required",
            "data_plane_required",
            "update_recovery_required",
            "network_containerization_required",
        ),
    )


def build_default_ai_orchestration_policy() -> AIOrchestrationPolicy:
    return AIOrchestrationPolicy(
        policy_id="ai_orchestration_policy_v1",
        foundation_readiness=build_default_ai_orchestration_foundation_readiness_model(),
        may_propose=True,
        may_apply=False,
        direct_action_execution_allowed=False,
        workflow_engine_execution_allowed=False,
        direct_autonomous_execution_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_may_only_propose",
            "direct_execution_blocked",
            "runtime_mutation_blocked",
            "deployment_blocked",
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
