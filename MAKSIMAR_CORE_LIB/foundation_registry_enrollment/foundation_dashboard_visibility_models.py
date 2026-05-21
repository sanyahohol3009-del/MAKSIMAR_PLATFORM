from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    FoundationDomainEnrollmentModel,
    build_default_foundation_domain_enrollments,
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    FoundationLayerId,
)


@dataclass(frozen=True, slots=True)
class FoundationDashboardVisibilityModel:
    visibility_id: str
    domain_enrollment: FoundationDomainEnrollmentModel
    dashboard_surface_id: str
    visible_in_foundation_dashboard: bool
    dashboard_control_allowed: bool
    dashboard_registry_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("visibility_id", self.visibility_id)
        if not isinstance(self.domain_enrollment, FoundationDomainEnrollmentModel):
            raise TypeError("domain_enrollment must be FoundationDomainEnrollmentModel")
        _validate_non_empty("dashboard_surface_id", self.dashboard_surface_id)
        _validate_true("visible_in_foundation_dashboard", self.visible_in_foundation_dashboard)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("dashboard_registry_write_allowed", self.dashboard_registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "visibility_id": self.visibility_id,
            "domain_enrollment": self.domain_enrollment.to_dict(),
            "dashboard_surface_id": self.dashboard_surface_id,
            "visible_in_foundation_dashboard": self.visible_in_foundation_dashboard,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "dashboard_registry_write_allowed": self.dashboard_registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_foundation_dashboard_visibility_model(
    layer_id: FoundationLayerId = "root_artifact_hygiene",
) -> FoundationDashboardVisibilityModel:
    domain_enrollment = build_foundation_domain_enrollment_model(layer_id)
    return FoundationDashboardVisibilityModel(
        visibility_id=f"{layer_id}_dashboard_visibility_v1",
        domain_enrollment=domain_enrollment,
        dashboard_surface_id="foundation_registry_enrollment_dashboard_read_model",
        visible_in_foundation_dashboard=True,
        dashboard_control_allowed=False,
        dashboard_registry_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "foundation_dashboard_visibility_declared",
            "dashboard_read_model_only",
            "dashboard_control_blocked",
        ),
    )


def build_default_foundation_dashboard_visibility_models() -> tuple[FoundationDashboardVisibilityModel, ...]:
    return tuple(build_foundation_dashboard_visibility_model(layer_id) for layer_id in FOUNDATION_LAYER_IDS)


def build_dashboard_visibility_from_enrollments(
    enrollments: tuple[FoundationDomainEnrollmentModel, ...] | None = None,
) -> tuple[FoundationDashboardVisibilityModel, ...]:
    source = enrollments if enrollments is not None else build_default_foundation_domain_enrollments()
    return tuple(
        FoundationDashboardVisibilityModel(
            visibility_id=f"{enrollment.registry_domain_id}_dashboard_visibility_v1",
            domain_enrollment=enrollment,
            dashboard_surface_id="foundation_registry_enrollment_dashboard_read_model",
            visible_in_foundation_dashboard=True,
            dashboard_control_allowed=False,
            dashboard_registry_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=(
                "foundation_dashboard_visibility_declared",
                "dashboard_read_model_only",
                "dashboard_control_blocked",
            ),
        )
        for enrollment in source
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
