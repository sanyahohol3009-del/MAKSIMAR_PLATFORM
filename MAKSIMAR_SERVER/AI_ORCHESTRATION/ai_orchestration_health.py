from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AIOrchestrationHealthReadModel:
    health_id: str
    ai_services_adapter_ready: bool
    workers_adapter_ready: bool
    control_plane_router_adapter_ready: bool
    proposal_only: bool
    runtime_mutation_allowed: bool
    deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("health_id", self.health_id)
        _validate_true("ai_services_adapter_ready", self.ai_services_adapter_ready)
        _validate_true("workers_adapter_ready", self.workers_adapter_ready)
        _validate_true("control_plane_router_adapter_ready", self.control_plane_router_adapter_ready)
        _validate_true("proposal_only", self.proposal_only)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("deployment_allowed", self.deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    @property
    def healthy(self) -> bool:
        return (
            self.ai_services_adapter_ready
            and self.workers_adapter_ready
            and self.control_plane_router_adapter_ready
            and self.proposal_only
            and not self.runtime_mutation_allowed
            and not self.deployment_allowed
            and not self.public_exposure_allowed
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "health_id": self.health_id,
            "ai_services_adapter_ready": self.ai_services_adapter_ready,
            "workers_adapter_ready": self.workers_adapter_ready,
            "control_plane_router_adapter_ready": self.control_plane_router_adapter_ready,
            "proposal_only": self.proposal_only,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "healthy": self.healthy,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_orchestration_health_read_model() -> AIOrchestrationHealthReadModel:
    return AIOrchestrationHealthReadModel(
        health_id="ai_orchestration_health_v1",
        ai_services_adapter_ready=True,
        workers_adapter_ready=True,
        control_plane_router_adapter_ready=True,
        proposal_only=True,
        runtime_mutation_allowed=False,
        deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_services_adapter_ready",
            "workers_adapter_ready",
            "control_plane_router_adapter_ready",
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
