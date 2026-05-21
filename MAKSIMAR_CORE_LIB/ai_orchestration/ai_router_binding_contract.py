from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AIRouterBindingContract:
    contract_id: str
    existing_control_plane_router_ref: str
    existing_ai_orchestration_binding_ref: str
    existing_runtime_adapter_ref: str
    accounts_existing_router_binding: bool
    duplicates_control_plane_router: bool
    replaces_control_plane_router: bool
    route_execution_allowed: bool
    direct_model_execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("contract_id", self.contract_id)
        _validate_non_empty("existing_control_plane_router_ref", self.existing_control_plane_router_ref)
        _validate_non_empty("existing_ai_orchestration_binding_ref", self.existing_ai_orchestration_binding_ref)
        _validate_non_empty("existing_runtime_adapter_ref", self.existing_runtime_adapter_ref)

        _validate_true("accounts_existing_router_binding", self.accounts_existing_router_binding)
        _validate_false("duplicates_control_plane_router", self.duplicates_control_plane_router)
        _validate_false("replaces_control_plane_router", self.replaces_control_plane_router)
        _validate_false("route_execution_allowed", self.route_execution_allowed)
        _validate_false("direct_model_execution_allowed", self.direct_model_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "existing_control_plane_router_ref": self.existing_control_plane_router_ref,
            "existing_ai_orchestration_binding_ref": self.existing_ai_orchestration_binding_ref,
            "existing_runtime_adapter_ref": self.existing_runtime_adapter_ref,
            "accounts_existing_router_binding": self.accounts_existing_router_binding,
            "duplicates_control_plane_router": self.duplicates_control_plane_router,
            "replaces_control_plane_router": self.replaces_control_plane_router,
            "route_execution_allowed": self.route_execution_allowed,
            "direct_model_execution_allowed": self.direct_model_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_ai_router_binding_contract() -> AIRouterBindingContract:
    return AIRouterBindingContract(
        contract_id="ai_orchestration_ai_router_binding_accounting_v1",
        existing_control_plane_router_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
        existing_ai_orchestration_binding_ref="AI_ORCHESTRATION/existing_bindings/control_plane_ai_router_binding.yaml",
        existing_runtime_adapter_ref="MAKSIMAR_SERVER/AI_ORCHESTRATION/adapters/control_plane_ai_router_adapter.py",
        accounts_existing_router_binding=True,
        duplicates_control_plane_router=False,
        replaces_control_plane_router=False,
        route_execution_allowed=False,
        direct_model_execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "acceptance_accounting_contract_only",
            "existing_control_plane_router_accounted",
            "control_plane_router_not_duplicated",
            "route_execution_blocked",
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
