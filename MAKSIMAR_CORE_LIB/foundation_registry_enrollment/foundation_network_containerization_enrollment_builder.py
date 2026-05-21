from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    FoundationDashboardVisibilityModel,
    build_foundation_dashboard_visibility_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    FoundationDomainEnrollmentModel,
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FoundationLayerManifestModel,
    build_foundation_layer_manifest_model,
)


NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES: tuple[str, ...] = (
    "NETWORK_SEGMENTATION/layer_manifest.yaml",
    "NETWORK_SEGMENTATION/container_network_rules.yaml",
    "NETWORK_SEGMENTATION/network_segments.yaml",
    "NETWORK_SEGMENTATION/existing_bindings/network_trust_boundaries_binding.yaml",
    "CONTAINER_DEPLOYMENT/layer_manifest.yaml",
    "CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml",
    "CONTAINER_DEPLOYMENT/container_contract.schema.yaml",
    "CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml",
    "CONTAINER_DEPLOYMENT/no_production_deploy_until_foundation_green.yaml",
    "MAKSIMAR_CORE_LIB/network_containerization/network_segment_models.py",
    "MAKSIMAR_CORE_LIB/network_containerization/network_topology_builder.py",
    "MAKSIMAR_CORE_LIB/network_containerization/network_trust_boundary_binding_models.py",
    "MAKSIMAR_CORE_LIB/network_containerization/container_contract_models.py",
    "MAKSIMAR_CORE_LIB/network_containerization/container_deployment_read_model.py",
    "MAKSIMAR_CORE_LIB/network_containerization/network_containerization_acceptance_read_model.py",
    "docs/architecture/foundation/network_containerization_foundation_acceptance_v1.md",
    "docs/architecture/foundation/network_containerization_phase_4_final_closure_v1.md",
    "docs/architecture/foundation/network_containerization_container_boundary_v1.md",
    "docs/architecture/foundation/network_containerization_existing_binding_review_v1.md",
    "tests/network_containerization",
    "tests/network_trust_boundaries",
)


@dataclass(frozen=True, slots=True)
class NetworkContainerizationFoundationEnrollmentReadModel:
    read_model_id: str
    layer_manifest: FoundationLayerManifestModel
    domain_enrollment: FoundationDomainEnrollmentModel
    dashboard_visibility: FoundationDashboardVisibilityModel
    existing_network_containerization_surfaces: tuple[str, ...]
    network_containerization_registry_visible: bool
    existing_network_containerization_accounted: bool
    replaces_network_containerization: bool
    migrates_network_containerization: bool
    duplicates_network_containerization_logic: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_control_allowed: bool
    active_docker_deployment_allowed: bool
    active_compose_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.layer_manifest, FoundationLayerManifestModel):
            raise TypeError("layer_manifest must be FoundationLayerManifestModel")
        if not isinstance(self.domain_enrollment, FoundationDomainEnrollmentModel):
            raise TypeError("domain_enrollment must be FoundationDomainEnrollmentModel")
        if not isinstance(self.dashboard_visibility, FoundationDashboardVisibilityModel):
            raise TypeError("dashboard_visibility must be FoundationDashboardVisibilityModel")

        if self.layer_manifest.layer_id != "network_containerization":
            raise ValueError("layer_manifest must describe network_containerization")
        if self.domain_enrollment.registry_domain_id != "network_containerization":
            raise ValueError("domain_enrollment must describe network_containerization")
        if self.dashboard_visibility.domain_enrollment.registry_domain_id != "network_containerization":
            raise ValueError("dashboard_visibility must describe network_containerization")

        _validate_non_empty_tuple(
            "existing_network_containerization_surfaces",
            self.existing_network_containerization_surfaces,
        )
        _validate_true("network_containerization_registry_visible", self.network_containerization_registry_visible)
        _validate_true("existing_network_containerization_accounted", self.existing_network_containerization_accounted)
        _validate_false("replaces_network_containerization", self.replaces_network_containerization)
        _validate_false("migrates_network_containerization", self.migrates_network_containerization)
        _validate_false("duplicates_network_containerization_logic", self.duplicates_network_containerization_logic)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("active_docker_deployment_allowed", self.active_docker_deployment_allowed)
        _validate_false("active_compose_deployment_allowed", self.active_compose_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_manifest": self.layer_manifest.to_dict(),
            "domain_enrollment": self.domain_enrollment.to_dict(),
            "dashboard_visibility": self.dashboard_visibility.to_dict(),
            "existing_network_containerization_surfaces": self.existing_network_containerization_surfaces,
            "network_containerization_registry_visible": self.network_containerization_registry_visible,
            "existing_network_containerization_accounted": self.existing_network_containerization_accounted,
            "replaces_network_containerization": self.replaces_network_containerization,
            "migrates_network_containerization": self.migrates_network_containerization,
            "duplicates_network_containerization_logic": self.duplicates_network_containerization_logic,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "active_docker_deployment_allowed": self.active_docker_deployment_allowed,
            "active_compose_deployment_allowed": self.active_compose_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_network_containerization_foundation_enrollment_read_model() -> NetworkContainerizationFoundationEnrollmentReadModel:
    return NetworkContainerizationFoundationEnrollmentReadModel(
        read_model_id="network_containerization_foundation_enrollment_read_model_v1",
        layer_manifest=build_foundation_layer_manifest_model("network_containerization"),
        domain_enrollment=build_foundation_domain_enrollment_model("network_containerization"),
        dashboard_visibility=build_foundation_dashboard_visibility_model("network_containerization"),
        existing_network_containerization_surfaces=NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES,
        network_containerization_registry_visible=True,
        existing_network_containerization_accounted=True,
        replaces_network_containerization=False,
        migrates_network_containerization=False,
        duplicates_network_containerization_logic=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_control_allowed=False,
        active_docker_deployment_allowed=False,
        active_compose_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "network_containerization_foundation_registry_visible",
            "existing_network_containerization_accounted",
            "network_containerization_not_replaced",
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
