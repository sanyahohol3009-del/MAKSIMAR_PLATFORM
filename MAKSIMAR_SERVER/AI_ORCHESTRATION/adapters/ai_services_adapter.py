from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AIServicesAdapterReadModel:
    adapter_id: str
    target_surface: str
    existing_service_binding_ref: str
    points_to_existing_service: bool
    duplicates_service_logic: bool
    model_runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    proposal_only: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("adapter_id", self.adapter_id)
        _validate_non_empty("target_surface", self.target_surface)
        _validate_non_empty("existing_service_binding_ref", self.existing_service_binding_ref)
        _validate_true("points_to_existing_service", self.points_to_existing_service)
        _validate_false("duplicates_service_logic", self.duplicates_service_logic)
        _validate_false("model_runtime_execution_allowed", self.model_runtime_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "target_surface": self.target_surface,
            "existing_service_binding_ref": self.existing_service_binding_ref,
            "points_to_existing_service": self.points_to_existing_service,
            "duplicates_service_logic": self.duplicates_service_logic,
            "model_runtime_execution_allowed": self.model_runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "proposal_only": self.proposal_only,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_services_adapter_read_model() -> AIServicesAdapterReadModel:
    return AIServicesAdapterReadModel(
        adapter_id="ai_services_adapter_v1",
        target_surface="AI_SERVICES",
        existing_service_binding_ref="AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml",
        points_to_existing_service=True,
        duplicates_service_logic=False,
        model_runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        proposal_only=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "adapter_points_to_existing_ai_services",
            "no_model_runtime_execution",
            "proposal_only",
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
