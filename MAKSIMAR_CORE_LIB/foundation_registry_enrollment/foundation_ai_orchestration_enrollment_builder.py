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


AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES: tuple[str, ...] = (
    "AI_ORCHESTRATION/layer_manifest.yaml",
    "AI_ORCHESTRATION/container_contract.yaml",
    "AI_ORCHESTRATION/config/ai_orchestration_policy.yaml",
    "AI_ORCHESTRATION/boundaries/container_adapter_boundary.yaml",
    "AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml",
    "AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
    "AI_ORCHESTRATION/existing_bindings/worker_binding.yaml",
    "MAKSIMAR_CORE_LIB/ai_orchestration/ai_orchestration_acceptance_read_model.py",
    "MAKSIMAR_CORE_LIB/ai_orchestration/ai_orchestration_read_model.py",
    "MAKSIMAR_CORE_LIB/ai_orchestration/ai_router_binding_contract.py",
    "MAKSIMAR_CORE_LIB/ai_orchestration/model_router_contract.py",
    "MAKSIMAR_CORE_LIB/ai_orchestration/tool_call_boundary_models.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/ai_orchestration_read_model_builder.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_router.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/proposal_staging_service.py",
    "docs/architecture/foundation/ai_orchestration_foundation_v1.md",
    "docs/architecture/foundation/ai_orchestration_phase_5_final_closure_v1.md",
    "tests/ai_orchestration",
)


@dataclass(frozen=True, slots=True)
class AIOrchestrationFoundationEnrollmentReadModel:
    read_model_id: str
    layer_manifest: FoundationLayerManifestModel
    domain_enrollment: FoundationDomainEnrollmentModel
    dashboard_visibility: FoundationDashboardVisibilityModel
    existing_ai_orchestration_surfaces: tuple[str, ...]
    ai_orchestration_registry_visible: bool
    ai_orchestration_dashboard_visible: bool
    existing_ai_orchestration_accounted: bool
    replaces_ai_orchestration: bool
    migrates_ai_orchestration: bool
    duplicates_ai_orchestration_logic: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_control_allowed: bool
    ai_execution_allowed: bool
    direct_tool_execution_allowed: bool
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

        if self.layer_manifest.layer_id != "ai_orchestration":
            raise ValueError("layer_manifest must describe ai_orchestration")
        if self.domain_enrollment.registry_domain_id != "ai_orchestration":
            raise ValueError("domain_enrollment must describe ai_orchestration")
        if self.dashboard_visibility.domain_enrollment.registry_domain_id != "ai_orchestration":
            raise ValueError("dashboard_visibility must describe ai_orchestration")

        _validate_non_empty_tuple("existing_ai_orchestration_surfaces", self.existing_ai_orchestration_surfaces)
        _validate_true("ai_orchestration_registry_visible", self.ai_orchestration_registry_visible)
        _validate_true("ai_orchestration_dashboard_visible", self.ai_orchestration_dashboard_visible)
        _validate_true("existing_ai_orchestration_accounted", self.existing_ai_orchestration_accounted)
        _validate_false("replaces_ai_orchestration", self.replaces_ai_orchestration)
        _validate_false("migrates_ai_orchestration", self.migrates_ai_orchestration)
        _validate_false("duplicates_ai_orchestration_logic", self.duplicates_ai_orchestration_logic)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("ai_execution_allowed", self.ai_execution_allowed)
        _validate_false("direct_tool_execution_allowed", self.direct_tool_execution_allowed)
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
            "existing_ai_orchestration_surfaces": self.existing_ai_orchestration_surfaces,
            "ai_orchestration_registry_visible": self.ai_orchestration_registry_visible,
            "ai_orchestration_dashboard_visible": self.ai_orchestration_dashboard_visible,
            "existing_ai_orchestration_accounted": self.existing_ai_orchestration_accounted,
            "replaces_ai_orchestration": self.replaces_ai_orchestration,
            "migrates_ai_orchestration": self.migrates_ai_orchestration,
            "duplicates_ai_orchestration_logic": self.duplicates_ai_orchestration_logic,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "ai_execution_allowed": self.ai_execution_allowed,
            "direct_tool_execution_allowed": self.direct_tool_execution_allowed,
            "deployment_allowed": self.deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_orchestration_foundation_enrollment_read_model() -> AIOrchestrationFoundationEnrollmentReadModel:
    return AIOrchestrationFoundationEnrollmentReadModel(
        read_model_id="ai_orchestration_foundation_enrollment_read_model_v1",
        layer_manifest=build_foundation_layer_manifest_model("ai_orchestration"),
        domain_enrollment=build_foundation_domain_enrollment_model("ai_orchestration"),
        dashboard_visibility=build_foundation_dashboard_visibility_model("ai_orchestration"),
        existing_ai_orchestration_surfaces=AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES,
        ai_orchestration_registry_visible=True,
        ai_orchestration_dashboard_visible=True,
        existing_ai_orchestration_accounted=True,
        replaces_ai_orchestration=False,
        migrates_ai_orchestration=False,
        duplicates_ai_orchestration_logic=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_control_allowed=False,
        ai_execution_allowed=False,
        direct_tool_execution_allowed=False,
        deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_orchestration_foundation_registry_visible",
            "ai_orchestration_dashboard_visible",
            "existing_ai_orchestration_accounted",
            "ai_execution_blocked",
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
