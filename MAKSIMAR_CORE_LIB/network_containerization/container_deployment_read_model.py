from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_containerization.network_topology_builder import (
    NetworkTopologyReadModel,
    build_network_topology_read_model,
)


@dataclass(frozen=True, slots=True)
class ContainerDeploymentReadModel:
    read_model_id: str
    topology: NetworkTopologyReadModel
    container_deployment_blueprint_path: str
    container_contract_schema_path: str
    security_required_gate_path: str
    foundation_green_gate_path: str
    deployment_allowed_now: bool
    active_docker_deployment_allowed: bool
    active_compose_deployment_allowed: bool
    public_exposure_allowed: bool
    runtime_network_mutation_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.topology, NetworkTopologyReadModel):
            raise TypeError("topology must be NetworkTopologyReadModel")
        _validate_non_empty("container_deployment_blueprint_path", self.container_deployment_blueprint_path)
        _validate_non_empty("container_contract_schema_path", self.container_contract_schema_path)
        _validate_non_empty("security_required_gate_path", self.security_required_gate_path)
        _validate_non_empty("foundation_green_gate_path", self.foundation_green_gate_path)
        _validate_false("deployment_allowed_now", self.deployment_allowed_now)
        _validate_false("active_docker_deployment_allowed", self.active_docker_deployment_allowed)
        _validate_false("active_compose_deployment_allowed", self.active_compose_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "topology": self.topology.to_dict(),
            "container_deployment_blueprint_path": self.container_deployment_blueprint_path,
            "container_contract_schema_path": self.container_contract_schema_path,
            "security_required_gate_path": self.security_required_gate_path,
            "foundation_green_gate_path": self.foundation_green_gate_path,
            "deployment_allowed_now": self.deployment_allowed_now,
            "active_docker_deployment_allowed": self.active_docker_deployment_allowed,
            "active_compose_deployment_allowed": self.active_compose_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_container_deployment_read_model() -> ContainerDeploymentReadModel:
    return ContainerDeploymentReadModel(
        read_model_id="container_deployment_read_model_v1",
        topology=build_network_topology_read_model(),
        container_deployment_blueprint_path="CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml",
        container_contract_schema_path="CONTAINER_DEPLOYMENT/container_contract.schema.yaml",
        security_required_gate_path="CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml",
        foundation_green_gate_path="CONTAINER_DEPLOYMENT/no_production_deploy_until_foundation_green.yaml",
        deployment_allowed_now=False,
        active_docker_deployment_allowed=False,
        active_compose_deployment_allowed=False,
        public_exposure_allowed=False,
        runtime_network_mutation_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "container_deployment_read_model_dashboard_safe",
            "no_public_exposure_by_default",
            "deployment_not_allowed_now",
            "read_model_only",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if not value:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value:
        raise ValueError(f"{field_name} must remain false")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)
