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


UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES: tuple[str, ...] = (
    "UPDATE_RECOVERY/layer_manifest.yaml",
    "UPDATE_RECOVERY/container_contract.yaml",
    "UPDATE_RECOVERY/config/update_recovery_policy.yaml",
    "UPDATE_RECOVERY/existing_bindings/runtime_recovery_manager_binding.yaml",
    "UPDATE_RECOVERY/existing_bindings/secure_sync_update_transport_binding.yaml",
    "MAKSIMAR_CORE_LIB/update_recovery/update_recovery_read_model.py",
    "MAKSIMAR_CORE_LIB/update_recovery/signed_update_service_contract.py",
    "MAKSIMAR_CORE_LIB/update_recovery/snapshot_manager_contract.py",
    "MAKSIMAR_CORE_LIB/update_recovery/rollback_manager_contract.py",
    "MAKSIMAR_CORE_LIB/update_recovery/recovery_service_contract.py",
    "MAKSIMAR_CORE_LIB/update_recovery/offline_import_gate_contract.py",
    "MAKSIMAR_SERVER/UPDATE_RECOVERY/update_recovery_read_model_builder.py",
    "MAKSIMAR_SERVER/UPDATE_RECOVERY/recovery_service.py",
    "MAKSIMAR_SERVER/UPDATE_RECOVERY/rollback_manager.py",
    "docs/architecture/foundation/update_recovery_infra_foundation_v1.md",
    "docs/architecture/foundation/update_recovery_container_boundary_v1.md",
    "docs/architecture/foundation/update_recovery_existing_binding_review_v1.md",
    "tests/update_recovery",
)


@dataclass(frozen=True, slots=True)
class UpdateRecoveryFoundationEnrollmentReadModel:
    read_model_id: str
    layer_manifest: FoundationLayerManifestModel
    domain_enrollment: FoundationDomainEnrollmentModel
    dashboard_visibility: FoundationDashboardVisibilityModel
    existing_update_recovery_surfaces: tuple[str, ...]
    update_recovery_registry_visible: bool
    existing_update_recovery_accounted: bool
    replaces_update_recovery: bool
    migrates_update_recovery: bool
    duplicates_update_recovery_logic: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_control_allowed: bool
    deployment_allowed: bool
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

        if self.layer_manifest.layer_id != "update_recovery_infra":
            raise ValueError("layer_manifest must describe update_recovery_infra")
        if self.domain_enrollment.registry_domain_id != "update_recovery_infra":
            raise ValueError("domain_enrollment must describe update_recovery_infra")
        if self.dashboard_visibility.domain_enrollment.registry_domain_id != "update_recovery_infra":
            raise ValueError("dashboard_visibility must describe update_recovery_infra")

        _validate_non_empty_tuple("existing_update_recovery_surfaces", self.existing_update_recovery_surfaces)
        _validate_true("update_recovery_registry_visible", self.update_recovery_registry_visible)
        _validate_true("existing_update_recovery_accounted", self.existing_update_recovery_accounted)
        _validate_false("replaces_update_recovery", self.replaces_update_recovery)
        _validate_false("migrates_update_recovery", self.migrates_update_recovery)
        _validate_false("duplicates_update_recovery_logic", self.duplicates_update_recovery_logic)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("deployment_allowed", self.deployment_allowed)
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
            "existing_update_recovery_surfaces": self.existing_update_recovery_surfaces,
            "update_recovery_registry_visible": self.update_recovery_registry_visible,
            "existing_update_recovery_accounted": self.existing_update_recovery_accounted,
            "replaces_update_recovery": self.replaces_update_recovery,
            "migrates_update_recovery": self.migrates_update_recovery,
            "duplicates_update_recovery_logic": self.duplicates_update_recovery_logic,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "deployment_allowed": self.deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_update_recovery_foundation_enrollment_read_model() -> UpdateRecoveryFoundationEnrollmentReadModel:
    return UpdateRecoveryFoundationEnrollmentReadModel(
        read_model_id="update_recovery_foundation_enrollment_read_model_v1",
        layer_manifest=build_foundation_layer_manifest_model("update_recovery_infra"),
        domain_enrollment=build_foundation_domain_enrollment_model("update_recovery_infra"),
        dashboard_visibility=build_foundation_dashboard_visibility_model("update_recovery_infra"),
        existing_update_recovery_surfaces=UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES,
        update_recovery_registry_visible=True,
        existing_update_recovery_accounted=True,
        replaces_update_recovery=False,
        migrates_update_recovery=False,
        duplicates_update_recovery_logic=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_control_allowed=False,
        deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "update_recovery_foundation_registry_visible",
            "existing_update_recovery_accounted",
            "update_recovery_not_replaced",
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
