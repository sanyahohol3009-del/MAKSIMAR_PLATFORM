from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_dashboard_visibility_builder import (
    FoundationLayerDashboardVisibilityReadModel,
    build_foundation_layer_dashboard_visibility_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_readiness_summary_builder import (
    FoundationLayerReadinessSummaryReadModel,
    build_foundation_layer_readiness_summary_read_model,
)


FOUNDATION_LAYER_MANIFEST_PATHS: dict[str, str] = {
    "security_layer": "SECURITY_LAYER/layer_manifest.yaml",
    "data_plane": "DATA_PLANE/layer_manifest.yaml",
    "update_recovery_infra": "UPDATE_RECOVERY/layer_manifest.yaml",
    "network_containerization": "NETWORK_SEGMENTATION/layer_manifest.yaml",
    "ai_orchestration": "AI_ORCHESTRATION/layer_manifest.yaml",
}

FOUNDATION_LAYER_CONTAINER_BOUNDARY_PATHS: dict[str, tuple[str, ...]] = {
    "security_layer": (
        "SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
        "docs/architecture/foundation/security_layer_container_boundary_v1.md",
    ),
    "data_plane": (
        "DATA_PLANE/boundaries/container_adapter_boundary.yaml",
        "docs/architecture/foundation/data_plane_container_boundary_v1.md",
    ),
    "update_recovery_infra": (
        "UPDATE_RECOVERY/boundaries/container_adapter_boundary.yaml",
        "docs/architecture/foundation/update_recovery_container_boundary_v1.md",
    ),
    "network_containerization": (
        "NETWORK_SEGMENTATION/boundaries/container_adapter_boundary.yaml",
        "CONTAINER_DEPLOYMENT/container_contract.schema.yaml",
        "docs/architecture/foundation/network_containerization_container_boundary_v1.md",
    ),
    "ai_orchestration": (
        "AI_ORCHESTRATION/boundaries/container_adapter_boundary.yaml",
        "docs/architecture/foundation/ai_orchestration_container_boundary_v1.md",
    ),
}


@dataclass(frozen=True, slots=True)
class FoundationLayerFinalAcceptanceEntry:
    layer_id: str
    manifest_path: str
    container_boundary_paths: tuple[str, ...]
    has_manifest: bool
    has_dashboard_visibility: bool
    has_container_boundary: bool
    enrolled: bool
    direct_execution_allowed: bool
    dashboard_mutation_allowed: bool
    registry_write_allowed: bool
    runtime_mutation_allowed: bool
    accepted: bool

    def __post_init__(self) -> None:
        _validate_non_empty("layer_id", self.layer_id)
        _validate_non_empty("manifest_path", self.manifest_path)
        _validate_non_empty_tuple("container_boundary_paths", self.container_boundary_paths)
        _validate_true("has_manifest", self.has_manifest)
        _validate_true("has_dashboard_visibility", self.has_dashboard_visibility)
        _validate_true("has_container_boundary", self.has_container_boundary)
        _validate_true("enrolled", self.enrolled)
        _validate_false("direct_execution_allowed", self.direct_execution_allowed)
        _validate_false("dashboard_mutation_allowed", self.dashboard_mutation_allowed)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("accepted", self.accepted)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "manifest_path": self.manifest_path,
            "container_boundary_paths": self.container_boundary_paths,
            "has_manifest": self.has_manifest,
            "has_dashboard_visibility": self.has_dashboard_visibility,
            "has_container_boundary": self.has_container_boundary,
            "enrolled": self.enrolled,
            "direct_execution_allowed": self.direct_execution_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "registry_write_allowed": self.registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "accepted": self.accepted,
        }


@dataclass(frozen=True, slots=True)
class FoundationLayersFinalAcceptanceReadModel:
    read_model_id: str
    readiness_summary: FoundationLayerReadinessSummaryReadModel
    dashboard_visibility: FoundationLayerDashboardVisibilityReadModel
    acceptance_entries: tuple[FoundationLayerFinalAcceptanceEntry, ...]
    total_layers: int
    manifest_layers: int
    dashboard_visible_layers: int
    container_boundary_layers: int
    enrolled_layers: int
    direct_execution_allowed_layers: int
    dashboard_mutation_allowed_layers: int
    registry_write_allowed_layers: int
    runtime_mutation_allowed_layers: int
    all_foundation_layers_have_manifest: bool
    all_foundation_layers_have_dashboard_visibility: bool
    all_foundation_layers_have_container_boundary: bool
    all_foundation_layers_enrolled: bool
    all_foundation_layers_enrolled_without_direct_execution: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_mutation_allowed: bool
    direct_execution_allowed: bool
    deployment_allowed: bool
    public_exposure_allowed: bool
    final_acceptance_ready: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.readiness_summary, FoundationLayerReadinessSummaryReadModel):
            raise TypeError("readiness_summary must be FoundationLayerReadinessSummaryReadModel")
        if not isinstance(self.dashboard_visibility, FoundationLayerDashboardVisibilityReadModel):
            raise TypeError("dashboard_visibility must be FoundationLayerDashboardVisibilityReadModel")
        if not isinstance(self.acceptance_entries, tuple):
            raise TypeError("acceptance_entries must be a tuple")
        if not self.acceptance_entries:
            raise ValueError("acceptance_entries must not be empty")
        for entry in self.acceptance_entries:
            if not isinstance(entry, FoundationLayerFinalAcceptanceEntry):
                raise TypeError("acceptance_entries must contain FoundationLayerFinalAcceptanceEntry values")

        _validate_count("total_layers", self.total_layers, len(self.acceptance_entries))
        _validate_count("manifest_layers", self.manifest_layers, sum(1 for entry in self.acceptance_entries if entry.has_manifest))
        _validate_count("dashboard_visible_layers", self.dashboard_visible_layers, sum(1 for entry in self.acceptance_entries if entry.has_dashboard_visibility))
        _validate_count("container_boundary_layers", self.container_boundary_layers, sum(1 for entry in self.acceptance_entries if entry.has_container_boundary))
        _validate_count("enrolled_layers", self.enrolled_layers, sum(1 for entry in self.acceptance_entries if entry.enrolled))
        _validate_count("direct_execution_allowed_layers", self.direct_execution_allowed_layers, sum(1 for entry in self.acceptance_entries if entry.direct_execution_allowed))
        _validate_count("dashboard_mutation_allowed_layers", self.dashboard_mutation_allowed_layers, sum(1 for entry in self.acceptance_entries if entry.dashboard_mutation_allowed))
        _validate_count("registry_write_allowed_layers", self.registry_write_allowed_layers, sum(1 for entry in self.acceptance_entries if entry.registry_write_allowed))
        _validate_count("runtime_mutation_allowed_layers", self.runtime_mutation_allowed_layers, sum(1 for entry in self.acceptance_entries if entry.runtime_mutation_allowed))

        _validate_true("all_foundation_layers_have_manifest", self.all_foundation_layers_have_manifest)
        _validate_true("all_foundation_layers_have_dashboard_visibility", self.all_foundation_layers_have_dashboard_visibility)
        _validate_true("all_foundation_layers_have_container_boundary", self.all_foundation_layers_have_container_boundary)
        _validate_true("all_foundation_layers_enrolled", self.all_foundation_layers_enrolled)
        _validate_true("all_foundation_layers_enrolled_without_direct_execution", self.all_foundation_layers_enrolled_without_direct_execution)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_mutation_allowed", self.dashboard_mutation_allowed)
        _validate_false("direct_execution_allowed", self.direct_execution_allowed)
        _validate_false("deployment_allowed", self.deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("final_acceptance_ready", self.final_acceptance_ready)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "readiness_summary": self.readiness_summary.to_dict(),
            "dashboard_visibility": self.dashboard_visibility.to_dict(),
            "acceptance_entries": tuple(entry.to_dict() for entry in self.acceptance_entries),
            "total_layers": self.total_layers,
            "manifest_layers": self.manifest_layers,
            "dashboard_visible_layers": self.dashboard_visible_layers,
            "container_boundary_layers": self.container_boundary_layers,
            "enrolled_layers": self.enrolled_layers,
            "direct_execution_allowed_layers": self.direct_execution_allowed_layers,
            "dashboard_mutation_allowed_layers": self.dashboard_mutation_allowed_layers,
            "registry_write_allowed_layers": self.registry_write_allowed_layers,
            "runtime_mutation_allowed_layers": self.runtime_mutation_allowed_layers,
            "all_foundation_layers_have_manifest": self.all_foundation_layers_have_manifest,
            "all_foundation_layers_have_dashboard_visibility": self.all_foundation_layers_have_dashboard_visibility,
            "all_foundation_layers_have_container_boundary": self.all_foundation_layers_have_container_boundary,
            "all_foundation_layers_enrolled": self.all_foundation_layers_enrolled,
            "all_foundation_layers_enrolled_without_direct_execution": self.all_foundation_layers_enrolled_without_direct_execution,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_mutation_allowed": self.dashboard_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "deployment_allowed": self.deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "final_acceptance_ready": self.final_acceptance_ready,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_foundation_layers_final_acceptance_read_model() -> FoundationLayersFinalAcceptanceReadModel:
    readiness_summary = build_foundation_layer_readiness_summary_read_model()
    dashboard_visibility = build_foundation_layer_dashboard_visibility_read_model()
    readiness_by_layer = {entry.layer_id: entry for entry in readiness_summary.readiness_entries}
    visibility_by_layer = {entry.layer_id: entry for entry in dashboard_visibility.visibility_entries}

    entries = tuple(
        FoundationLayerFinalAcceptanceEntry(
            layer_id=layer_id,
            manifest_path=manifest_path,
            container_boundary_paths=FOUNDATION_LAYER_CONTAINER_BOUNDARY_PATHS[layer_id],
            has_manifest=True,
            has_dashboard_visibility=visibility_by_layer[layer_id].dashboard_visible,
            has_container_boundary=True,
            enrolled=readiness_by_layer[layer_id].registry_visible,
            direct_execution_allowed=readiness_by_layer[layer_id].execution_allowed,
            dashboard_mutation_allowed=visibility_by_layer[layer_id].dashboard_control_allowed,
            registry_write_allowed=readiness_by_layer[layer_id].registry_write_allowed,
            runtime_mutation_allowed=readiness_by_layer[layer_id].runtime_mutation_allowed,
            accepted=True,
        )
        for layer_id, manifest_path in FOUNDATION_LAYER_MANIFEST_PATHS.items()
    )

    return FoundationLayersFinalAcceptanceReadModel(
        read_model_id="foundation_layers_final_acceptance_read_model_v1",
        readiness_summary=readiness_summary,
        dashboard_visibility=dashboard_visibility,
        acceptance_entries=entries,
        total_layers=len(entries),
        manifest_layers=sum(1 for entry in entries if entry.has_manifest),
        dashboard_visible_layers=sum(1 for entry in entries if entry.has_dashboard_visibility),
        container_boundary_layers=sum(1 for entry in entries if entry.has_container_boundary),
        enrolled_layers=sum(1 for entry in entries if entry.enrolled),
        direct_execution_allowed_layers=sum(1 for entry in entries if entry.direct_execution_allowed),
        dashboard_mutation_allowed_layers=sum(1 for entry in entries if entry.dashboard_mutation_allowed),
        registry_write_allowed_layers=sum(1 for entry in entries if entry.registry_write_allowed),
        runtime_mutation_allowed_layers=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        all_foundation_layers_have_manifest=True,
        all_foundation_layers_have_dashboard_visibility=True,
        all_foundation_layers_have_container_boundary=True,
        all_foundation_layers_enrolled=True,
        all_foundation_layers_enrolled_without_direct_execution=True,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_mutation_allowed=False,
        direct_execution_allowed=False,
        deployment_allowed=False,
        public_exposure_allowed=False,
        final_acceptance_ready=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "all_foundation_layers_have_manifest",
            "all_foundation_layers_have_dashboard_visibility",
            "all_foundation_layers_have_container_boundary",
            "all_foundation_layers_enrolled",
            "direct_execution_blocked",
            "final_acceptance_ready",
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


def _validate_count(field_name: str, value: int, expected: int) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value != expected:
        raise ValueError(f"{field_name} must equal {expected}")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
