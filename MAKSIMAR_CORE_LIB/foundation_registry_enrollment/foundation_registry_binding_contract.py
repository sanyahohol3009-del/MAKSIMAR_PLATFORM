from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    FoundationDashboardVisibilityModel,
    build_dashboard_visibility_from_enrollments,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    FoundationDomainEnrollmentModel,
    build_default_foundation_domain_enrollments,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    FoundationLayerManifestModel,
    build_default_foundation_layer_manifests,
)


@dataclass(frozen=True, slots=True)
class FoundationRegistryEnrollmentReadModel:
    read_model_id: str
    layer_manifests: tuple[FoundationLayerManifestModel, ...]
    domain_enrollments: tuple[FoundationDomainEnrollmentModel, ...]
    dashboard_visibility: tuple[FoundationDashboardVisibilityModel, ...]
    foundation_visibility_formalized: bool
    existing_registry_surfaces_accounted: bool
    replaces_existing_registry: bool
    migrates_existing_registry: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    acceptance_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_manifest_tuple(self.layer_manifests)
        _validate_enrollment_tuple(self.domain_enrollments)
        _validate_visibility_tuple(self.dashboard_visibility)
        _validate_matching_layer_coverage(
            self.layer_manifests,
            self.domain_enrollments,
            self.dashboard_visibility,
        )

        _validate_true("foundation_visibility_formalized", self.foundation_visibility_formalized)
        _validate_true("existing_registry_surfaces_accounted", self.existing_registry_surfaces_accounted)
        _validate_false("replaces_existing_registry", self.replaces_existing_registry)
        _validate_false("migrates_existing_registry", self.migrates_existing_registry)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
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
            "layer_manifests": tuple(item.to_dict() for item in self.layer_manifests),
            "domain_enrollments": tuple(item.to_dict() for item in self.domain_enrollments),
            "dashboard_visibility": tuple(item.to_dict() for item in self.dashboard_visibility),
            "foundation_visibility_formalized": self.foundation_visibility_formalized,
            "existing_registry_surfaces_accounted": self.existing_registry_surfaces_accounted,
            "replaces_existing_registry": self.replaces_existing_registry,
            "migrates_existing_registry": self.migrates_existing_registry,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "acceptance_ready": self.acceptance_ready,
            "reason_codes": self.reason_codes,
        }


def build_foundation_registry_enrollment_read_model() -> FoundationRegistryEnrollmentReadModel:
    layer_manifests = build_default_foundation_layer_manifests()
    domain_enrollments = build_default_foundation_domain_enrollments()
    dashboard_visibility = build_dashboard_visibility_from_enrollments(domain_enrollments)

    return FoundationRegistryEnrollmentReadModel(
        read_model_id="foundation_registry_enrollment_read_model_v1",
        layer_manifests=layer_manifests,
        domain_enrollments=domain_enrollments,
        dashboard_visibility=dashboard_visibility,
        foundation_visibility_formalized=True,
        existing_registry_surfaces_accounted=True,
        replaces_existing_registry=False,
        migrates_existing_registry=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        acceptance_ready=True,
        reason_codes=(
            "foundation_registry_enrollment_ready",
            "foundation_visibility_formalized",
            "existing_registry_surfaces_accounted",
            "registry_write_blocked",
        ),
    )


def _validate_manifest_tuple(value: tuple[FoundationLayerManifestModel, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError("layer_manifests must be a tuple")
    if not value:
        raise ValueError("layer_manifests must not be empty")
    for item in value:
        if not isinstance(item, FoundationLayerManifestModel):
            raise TypeError("layer_manifests must contain FoundationLayerManifestModel values")


def _validate_enrollment_tuple(value: tuple[FoundationDomainEnrollmentModel, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError("domain_enrollments must be a tuple")
    if not value:
        raise ValueError("domain_enrollments must not be empty")
    for item in value:
        if not isinstance(item, FoundationDomainEnrollmentModel):
            raise TypeError("domain_enrollments must contain FoundationDomainEnrollmentModel values")


def _validate_visibility_tuple(value: tuple[FoundationDashboardVisibilityModel, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError("dashboard_visibility must be a tuple")
    if not value:
        raise ValueError("dashboard_visibility must not be empty")
    for item in value:
        if not isinstance(item, FoundationDashboardVisibilityModel):
            raise TypeError("dashboard_visibility must contain FoundationDashboardVisibilityModel values")


def _validate_matching_layer_coverage(
    manifests: tuple[FoundationLayerManifestModel, ...],
    enrollments: tuple[FoundationDomainEnrollmentModel, ...],
    visibility: tuple[FoundationDashboardVisibilityModel, ...],
) -> None:
    manifest_ids = tuple(item.layer_id for item in manifests)
    enrollment_ids = tuple(item.registry_domain_id for item in enrollments)
    visibility_ids = tuple(item.domain_enrollment.registry_domain_id for item in visibility)

    expected = tuple(FOUNDATION_LAYER_IDS)
    if manifest_ids != expected:
        raise ValueError("layer_manifests must cover all foundation layers in canonical order")
    if enrollment_ids != expected:
        raise ValueError("domain_enrollments must cover all foundation layers in canonical order")
    if visibility_ids != expected:
        raise ValueError("dashboard_visibility must cover all foundation layers in canonical order")


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
