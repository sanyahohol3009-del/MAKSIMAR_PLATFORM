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


SECURITY_FOUNDATION_EXISTING_SURFACES: tuple[str, ...] = (
    "SECURITY_LAYER/layer_manifest.yaml",
    "SECURITY_LAYER/container_contract.yaml",
    "SECURITY_LAYER/existing_bindings/security_existing_sources.yaml",
    "MAKSIMAR_CORE_LIB/security_layer/security_read_model.py",
    "MAKSIMAR_CORE_LIB/security_layer/security_gate_contract.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_gate.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_telemetry_read_model_builder.py",
    "docs/architecture/foundation/security_layer_foundation_v1.md",
    "tests/security_layer",
)


@dataclass(frozen=True, slots=True)
class SecurityFoundationEnrollmentReadModel:
    read_model_id: str
    layer_manifest: FoundationLayerManifestModel
    domain_enrollment: FoundationDomainEnrollmentModel
    dashboard_visibility: FoundationDashboardVisibilityModel
    existing_security_surfaces: tuple[str, ...]
    security_registry_visible: bool
    existing_security_layer_accounted: bool
    replaces_security_layer: bool
    migrates_security_layer: bool
    duplicates_security_logic: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_control_allowed: bool
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

        if self.layer_manifest.layer_id != "security_layer":
            raise ValueError("layer_manifest must describe security_layer")
        if self.domain_enrollment.registry_domain_id != "security_layer":
            raise ValueError("domain_enrollment must describe security_layer")
        if self.dashboard_visibility.domain_enrollment.registry_domain_id != "security_layer":
            raise ValueError("dashboard_visibility must describe security_layer")

        _validate_non_empty_tuple("existing_security_surfaces", self.existing_security_surfaces)
        _validate_true("security_registry_visible", self.security_registry_visible)
        _validate_true("existing_security_layer_accounted", self.existing_security_layer_accounted)
        _validate_false("replaces_security_layer", self.replaces_security_layer)
        _validate_false("migrates_security_layer", self.migrates_security_layer)
        _validate_false("duplicates_security_logic", self.duplicates_security_logic)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_manifest": self.layer_manifest.to_dict(),
            "domain_enrollment": self.domain_enrollment.to_dict(),
            "dashboard_visibility": self.dashboard_visibility.to_dict(),
            "existing_security_surfaces": self.existing_security_surfaces,
            "security_registry_visible": self.security_registry_visible,
            "existing_security_layer_accounted": self.existing_security_layer_accounted,
            "replaces_security_layer": self.replaces_security_layer,
            "migrates_security_layer": self.migrates_security_layer,
            "duplicates_security_logic": self.duplicates_security_logic,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_security_foundation_enrollment_read_model() -> SecurityFoundationEnrollmentReadModel:
    return SecurityFoundationEnrollmentReadModel(
        read_model_id="security_foundation_enrollment_read_model_v1",
        layer_manifest=build_foundation_layer_manifest_model("security_layer"),
        domain_enrollment=build_foundation_domain_enrollment_model("security_layer"),
        dashboard_visibility=build_foundation_dashboard_visibility_model("security_layer"),
        existing_security_surfaces=SECURITY_FOUNDATION_EXISTING_SURFACES,
        security_registry_visible=True,
        existing_security_layer_accounted=True,
        replaces_security_layer=False,
        migrates_security_layer=False,
        duplicates_security_logic=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_control_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "security_foundation_registry_visible",
            "existing_security_layer_accounted",
            "security_layer_not_replaced",
            "registry_write_blocked",
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
