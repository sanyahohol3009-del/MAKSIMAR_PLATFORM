from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ControlPlaneAIRouterAdapterReadModel:
    adapter_id: str
    target_surface: str
    existing_router_binding_ref: str
    points_to_existing_router_binding: bool
    duplicates_router_logic: bool
    route_execution_allowed: bool
    runtime_mutation_allowed: bool
    proposal_only: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("adapter_id", self.adapter_id)
        _validate_non_empty("target_surface", self.target_surface)
        _validate_non_empty("existing_router_binding_ref", self.existing_router_binding_ref)
        _validate_true("points_to_existing_router_binding", self.points_to_existing_router_binding)
        _validate_false("duplicates_router_logic", self.duplicates_router_logic)
        _validate_false("route_execution_allowed", self.route_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "target_surface": self.target_surface,
            "existing_router_binding_ref": self.existing_router_binding_ref,
            "points_to_existing_router_binding": self.points_to_existing_router_binding,
            "duplicates_router_logic": self.duplicates_router_logic,
            "route_execution_allowed": self.route_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "proposal_only": self.proposal_only,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_control_plane_ai_router_adapter_read_model() -> ControlPlaneAIRouterAdapterReadModel:
    return ControlPlaneAIRouterAdapterReadModel(
        adapter_id="control_plane_ai_router_adapter_v1",
        target_surface="CONTROL_PLANE/ai_router_binding",
        existing_router_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
        points_to_existing_router_binding=True,
        duplicates_router_logic=False,
        route_execution_allowed=False,
        runtime_mutation_allowed=False,
        proposal_only=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "adapter_points_to_existing_control_plane_ai_router_binding",
            "no_route_execution",
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
