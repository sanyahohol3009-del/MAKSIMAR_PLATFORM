from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_ai_orchestration_enrollment_builder import (
    AIOrchestrationFoundationEnrollmentReadModel,
    build_ai_orchestration_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_data_plane_enrollment_builder import (
    DataPlaneFoundationEnrollmentReadModel,
    build_data_plane_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_network_containerization_enrollment_builder import (
    NetworkContainerizationFoundationEnrollmentReadModel,
    build_network_containerization_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_security_enrollment_builder import (
    SecurityFoundationEnrollmentReadModel,
    build_security_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_update_recovery_enrollment_builder import (
    UpdateRecoveryFoundationEnrollmentReadModel,
    build_update_recovery_foundation_enrollment_read_model,
)


FoundationEnrollmentReadModel = (
    SecurityFoundationEnrollmentReadModel
    | DataPlaneFoundationEnrollmentReadModel
    | UpdateRecoveryFoundationEnrollmentReadModel
    | NetworkContainerizationFoundationEnrollmentReadModel
    | AIOrchestrationFoundationEnrollmentReadModel
)


@dataclass(frozen=True, slots=True)
class FoundationLayerReadinessEntry:
    layer_id: str
    read_model_id: str
    registry_visible: bool
    dashboard_visible: bool
    existing_surfaces_accounted: bool
    read_only: bool
    dashboard_safe: bool
    registry_write_allowed: bool
    runtime_mutation_allowed: bool
    execution_allowed: bool

    def __post_init__(self) -> None:
        _validate_non_empty("layer_id", self.layer_id)
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_true("registry_visible", self.registry_visible)
        _validate_true("dashboard_visible", self.dashboard_visible)
        _validate_true("existing_surfaces_accounted", self.existing_surfaces_accounted)
        _validate_true("read_only", self.read_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("execution_allowed", self.execution_allowed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "read_model_id": self.read_model_id,
            "registry_visible": self.registry_visible,
            "dashboard_visible": self.dashboard_visible,
            "existing_surfaces_accounted": self.existing_surfaces_accounted,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "registry_write_allowed": self.registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "execution_allowed": self.execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class FoundationLayerReadinessSummaryReadModel:
    read_model_id: str
    readiness_entries: tuple[FoundationLayerReadinessEntry, ...]
    total_layers: int
    registry_visible_layers: int
    dashboard_visible_layers: int
    read_only_layers: int
    dashboard_safe_layers: int
    execution_allowed_layers: int
    all_foundation_layers_ready: bool
    all_foundation_layers_registry_visible: bool
    all_foundation_layers_dashboard_visible: bool
    registry_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_control_allowed: bool
    read_only: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.readiness_entries, tuple):
            raise TypeError("readiness_entries must be a tuple")
        if not self.readiness_entries:
            raise ValueError("readiness_entries must not be empty")
        for entry in self.readiness_entries:
            if not isinstance(entry, FoundationLayerReadinessEntry):
                raise TypeError("readiness_entries must contain FoundationLayerReadinessEntry values")

        _validate_count("total_layers", self.total_layers, len(self.readiness_entries))
        _validate_count(
            "registry_visible_layers",
            self.registry_visible_layers,
            sum(1 for entry in self.readiness_entries if entry.registry_visible),
        )
        _validate_count(
            "dashboard_visible_layers",
            self.dashboard_visible_layers,
            sum(1 for entry in self.readiness_entries if entry.dashboard_visible),
        )
        _validate_count(
            "read_only_layers",
            self.read_only_layers,
            sum(1 for entry in self.readiness_entries if entry.read_only),
        )
        _validate_count(
            "dashboard_safe_layers",
            self.dashboard_safe_layers,
            sum(1 for entry in self.readiness_entries if entry.dashboard_safe),
        )
        _validate_count(
            "execution_allowed_layers",
            self.execution_allowed_layers,
            sum(1 for entry in self.readiness_entries if entry.execution_allowed),
        )

        _validate_true("all_foundation_layers_ready", self.all_foundation_layers_ready)
        _validate_true("all_foundation_layers_registry_visible", self.all_foundation_layers_registry_visible)
        _validate_true("all_foundation_layers_dashboard_visible", self.all_foundation_layers_dashboard_visible)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_true("read_only", self.read_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "readiness_entries": tuple(entry.to_dict() for entry in self.readiness_entries),
            "total_layers": self.total_layers,
            "registry_visible_layers": self.registry_visible_layers,
            "dashboard_visible_layers": self.dashboard_visible_layers,
            "read_only_layers": self.read_only_layers,
            "dashboard_safe_layers": self.dashboard_safe_layers,
            "execution_allowed_layers": self.execution_allowed_layers,
            "all_foundation_layers_ready": self.all_foundation_layers_ready,
            "all_foundation_layers_registry_visible": self.all_foundation_layers_registry_visible,
            "all_foundation_layers_dashboard_visible": self.all_foundation_layers_dashboard_visible,
            "registry_write_allowed": self.registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_foundation_layer_readiness_summary_read_model() -> FoundationLayerReadinessSummaryReadModel:
    enrollments: tuple[FoundationEnrollmentReadModel, ...] = (
        build_security_foundation_enrollment_read_model(),
        build_data_plane_foundation_enrollment_read_model(),
        build_update_recovery_foundation_enrollment_read_model(),
        build_network_containerization_foundation_enrollment_read_model(),
        build_ai_orchestration_foundation_enrollment_read_model(),
    )
    entries = tuple(_entry_from_enrollment(enrollment) for enrollment in enrollments)

    return FoundationLayerReadinessSummaryReadModel(
        read_model_id="foundation_layer_readiness_summary_read_model_v1",
        readiness_entries=entries,
        total_layers=len(entries),
        registry_visible_layers=sum(1 for entry in entries if entry.registry_visible),
        dashboard_visible_layers=sum(1 for entry in entries if entry.dashboard_visible),
        read_only_layers=sum(1 for entry in entries if entry.read_only),
        dashboard_safe_layers=sum(1 for entry in entries if entry.dashboard_safe),
        execution_allowed_layers=sum(1 for entry in entries if entry.execution_allowed),
        all_foundation_layers_ready=True,
        all_foundation_layers_registry_visible=True,
        all_foundation_layers_dashboard_visible=True,
        registry_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_control_allowed=False,
        read_only=True,
        dashboard_safe=True,
        reason_codes=(
            "all_foundation_layers_registry_visible",
            "all_foundation_layers_dashboard_visible",
            "all_foundation_layers_read_only",
            "execution_blocked",
        ),
    )


def _entry_from_enrollment(enrollment: FoundationEnrollmentReadModel) -> FoundationLayerReadinessEntry:
    payload = enrollment.to_dict()
    layer_id = str(payload["layer_manifest"]["layer_id"])
    return FoundationLayerReadinessEntry(
        layer_id=layer_id,
        read_model_id=str(payload["read_model_id"]),
        registry_visible=_registry_visible_from_payload(payload),
        dashboard_visible=bool(payload["dashboard_safe"]),
        existing_surfaces_accounted=_existing_surfaces_accounted_from_payload(payload),
        read_only=bool(payload["read_only"]),
        dashboard_safe=bool(payload["dashboard_safe"]),
        registry_write_allowed=bool(payload["registry_write_allowed"]),
        runtime_mutation_allowed=bool(payload["runtime_mutation_allowed"]),
        execution_allowed=_execution_allowed_from_payload(payload),
    )


def _registry_visible_from_payload(payload: dict[str, Any]) -> bool:
    for key in (
        "security_registry_visible",
        "data_plane_registry_visible",
        "update_recovery_registry_visible",
        "network_containerization_registry_visible",
        "ai_orchestration_registry_visible",
    ):
        if key in payload:
            return bool(payload[key])
    raise ValueError("registry visibility flag is missing")


def _existing_surfaces_accounted_from_payload(payload: dict[str, Any]) -> bool:
    for key in (
        "existing_security_layer_accounted",
        "existing_data_plane_accounted",
        "existing_update_recovery_accounted",
        "existing_network_containerization_accounted",
        "existing_ai_orchestration_accounted",
    ):
        if key in payload:
            return bool(payload[key])
    raise ValueError("existing surface accounting flag is missing")


def _execution_allowed_from_payload(payload: dict[str, Any]) -> bool:
    for key in (
        "ai_execution_allowed",
        "direct_tool_execution_allowed",
        "deployment_allowed",
        "active_docker_deployment_allowed",
        "active_compose_deployment_allowed",
        "dashboard_control_allowed",
    ):
        if bool(payload.get(key, False)):
            return True
    return False


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
