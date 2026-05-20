from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_containerization.container_exposure_policy import (
    ContainerExposurePolicy,
    build_no_public_exposure_policy,
)
from MAKSIMAR_CORE_LIB.network_containerization.container_healthcheck_models import (
    ContainerHealthcheckModel,
    build_default_container_healthcheck_model,
)
from MAKSIMAR_CORE_LIB.network_containerization.network_segment_models import (
    NetworkSegmentId,
    REQUIRED_NETWORK_SEGMENTS,
)
from MAKSIMAR_CORE_LIB.network_containerization.restart_policy_models import (
    RestartPolicyModel,
    build_default_restart_policy_model,
)


@dataclass(frozen=True, slots=True)
class ContainerContractModel:
    service_id: str
    image_source: str
    network_segment: NetworkSegmentId
    healthcheck: ContainerHealthcheckModel
    restart_policy: RestartPolicyModel
    exposure_policy: ContainerExposurePolicy
    run_as_non_root_required: bool
    read_only_filesystem_required: bool
    drop_capabilities_required: bool
    no_new_privileges_required: bool
    active_deployment_allowed: bool
    production_deployment_allowed: bool
    runtime_network_mutation_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("service_id", self.service_id)
        _validate_non_empty("image_source", self.image_source)
        if self.network_segment not in REQUIRED_NETWORK_SEGMENTS:
            raise ValueError(f"unknown network segment: {self.network_segment}")
        if not isinstance(self.healthcheck, ContainerHealthcheckModel):
            raise TypeError("healthcheck must be ContainerHealthcheckModel")
        if not isinstance(self.restart_policy, RestartPolicyModel):
            raise TypeError("restart_policy must be RestartPolicyModel")
        if not isinstance(self.exposure_policy, ContainerExposurePolicy):
            raise TypeError("exposure_policy must be ContainerExposurePolicy")

        _validate_true("run_as_non_root_required", self.run_as_non_root_required)
        _validate_true("read_only_filesystem_required", self.read_only_filesystem_required)
        _validate_true("drop_capabilities_required", self.drop_capabilities_required)
        _validate_true("no_new_privileges_required", self.no_new_privileges_required)

        _validate_false("active_deployment_allowed", self.active_deployment_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("runtime_network_mutation_allowed", self.runtime_network_mutation_allowed)

        if self.exposure_policy.public_exposure_allowed:
            raise ValueError("container contract cannot allow public exposure")

        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "image_source": self.image_source,
            "network_segment": self.network_segment,
            "healthcheck": self.healthcheck.to_dict(),
            "restart_policy": self.restart_policy.to_dict(),
            "exposure_policy": self.exposure_policy.to_dict(),
            "run_as_non_root_required": self.run_as_non_root_required,
            "read_only_filesystem_required": self.read_only_filesystem_required,
            "drop_capabilities_required": self.drop_capabilities_required,
            "no_new_privileges_required": self.no_new_privileges_required,
            "active_deployment_allowed": self.active_deployment_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "runtime_network_mutation_allowed": self.runtime_network_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_default_container_contract_model(
    *,
    service_id: str = "maksimar_blueprint_service",
    image_source: str = "maksimar/service-name:blueprint",
    network_segment: NetworkSegmentId = "net_control",
) -> ContainerContractModel:
    return ContainerContractModel(
        service_id=service_id,
        image_source=image_source,
        network_segment=network_segment,
        healthcheck=build_default_container_healthcheck_model(),
        restart_policy=build_default_restart_policy_model(),
        exposure_policy=build_no_public_exposure_policy(),
        run_as_non_root_required=True,
        read_only_filesystem_required=True,
        drop_capabilities_required=True,
        no_new_privileges_required=True,
        active_deployment_allowed=False,
        production_deployment_allowed=False,
        runtime_network_mutation_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "container_contract_model_declared",
            "no_public_exposure_by_default",
            "no_active_deployment",
            "no_runtime_network_mutation",
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
