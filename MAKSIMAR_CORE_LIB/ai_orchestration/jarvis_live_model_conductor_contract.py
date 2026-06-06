from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class JarvisLiveModelRole(str, Enum):
    CHAT = "chat"
    PLANNER = "planner"
    CODER = "coder"
    VISION = "vision"
    STT = "stt"
    TTS = "tts"
    RETRIEVAL = "retrieval"
    IMAGE = "image"
    VIDEO = "video"
    EXTERNAL_TASK_BROKER = "external_task_broker"


@dataclass(frozen=True, slots=True)
class JarvisLiveModelRoleBinding:
    role: JarvisLiveModelRole
    existing_service_surface: str
    existing_router_surface: str
    existing_worker_surface: str
    proposal_only: bool
    enabled: bool

    def __post_init__(self) -> None:
        if not isinstance(self.role, JarvisLiveModelRole):
            raise TypeError("role must be JarvisLiveModelRole")
        _validate_non_empty("existing_service_surface", self.existing_service_surface)
        _validate_non_empty("existing_router_surface", self.existing_router_surface)
        _validate_non_empty("existing_worker_surface", self.existing_worker_surface)
        _validate_true("proposal_only", self.proposal_only)
        _validate_false("enabled", self.enabled)

    def to_read_model(self) -> dict[str, object]:
        return {
            "role": self.role.value,
            "existing_service_surface": self.existing_service_surface,
            "existing_router_surface": self.existing_router_surface,
            "existing_worker_surface": self.existing_worker_surface,
            "proposal_only": self.proposal_only,
            "enabled": self.enabled,
        }


@dataclass(frozen=True, slots=True)
class JarvisLiveModelConductorContract:
    contract_id: str
    role_bindings: tuple[JarvisLiveModelRoleBinding, ...]
    referenced_architecture_surfaces: tuple[str, ...]
    duplicated_registry_surfaces: tuple[str, ...]
    proposal_only: bool
    disabled_by_default: bool
    direct_execution_allowed: bool
    direct_shell_allowed: bool
    direct_core_write_allowed: bool
    direct_app_control_allowed: bool
    model_download_allowed: bool
    runtime_start_allowed: bool
    dashboard_execution_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("contract_id", self.contract_id)
        if not self.role_bindings:
            raise ValueError("role_bindings must not be empty")
        for binding in self.role_bindings:
            if not isinstance(binding, JarvisLiveModelRoleBinding):
                raise TypeError("role_bindings must contain JarvisLiveModelRoleBinding")

        expected_roles = {role for role in JarvisLiveModelRole}
        actual_roles = {binding.role for binding in self.role_bindings}
        if actual_roles != expected_roles:
            raise ValueError("role_bindings must cover every JarvisLiveModelRole")

        _validate_non_empty_tuple(
            "referenced_architecture_surfaces",
            self.referenced_architecture_surfaces,
        )
        required_surfaces = {
            "AI_SERVICES",
            "MAKSIMAR_CORE_LIB/ai_orchestration",
            "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            "MAKSIMAR_CORE_LIB/workers_registry",
            "MAKSIMAR_CORE_LIB/execution_control",
            "MAKSIMAR_CORE_LIB/security_layer",
            "MAKSIMAR_CORE_LIB/security_layer/approval_service_contract.py",
            "MAKSIMAR_SERVER/PROPOSAL_AUDIT",
        }
        missing_surfaces = required_surfaces - set(self.referenced_architecture_surfaces)
        if missing_surfaces:
            raise ValueError(
                "referenced_architecture_surfaces missing required surfaces: "
                f"{sorted(missing_surfaces)}"
            )

        if self.duplicated_registry_surfaces:
            raise ValueError("duplicated_registry_surfaces must remain empty")

        _validate_true("proposal_only", self.proposal_only)
        _validate_true("disabled_by_default", self.disabled_by_default)
        _validate_false("direct_execution_allowed", self.direct_execution_allowed)
        _validate_false("direct_shell_allowed", self.direct_shell_allowed)
        _validate_false("direct_core_write_allowed", self.direct_core_write_allowed)
        _validate_false("direct_app_control_allowed", self.direct_app_control_allowed)
        _validate_false("model_download_allowed", self.model_download_allowed)
        _validate_false("runtime_start_allowed", self.runtime_start_allowed)
        _validate_false("dashboard_execution_allowed", self.dashboard_execution_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "roles": tuple(binding.to_read_model() for binding in self.role_bindings),
            "referenced_architecture_surfaces": self.referenced_architecture_surfaces,
            "duplicated_registry_surfaces": self.duplicated_registry_surfaces,
            "proposal_only": self.proposal_only,
            "disabled_by_default": self.disabled_by_default,
            "direct_execution_allowed": self.direct_execution_allowed,
            "direct_shell_allowed": self.direct_shell_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_app_control_allowed": self.direct_app_control_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_jarvis_live_model_conductor_contract() -> JarvisLiveModelConductorContract:
    bindings = tuple(
        JarvisLiveModelRoleBinding(
            role=role,
            existing_service_surface="AI_SERVICES",
            existing_router_surface="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            existing_worker_surface="MAKSIMAR_CORE_LIB/workers_registry",
            proposal_only=True,
            enabled=False,
        )
        for role in JarvisLiveModelRole
    )

    return JarvisLiveModelConductorContract(
        contract_id="jarvis_live_model_conductor_contract_v1",
        role_bindings=bindings,
        referenced_architecture_surfaces=(
            "AI_SERVICES",
            "MAKSIMAR_CORE_LIB/ai_orchestration",
            "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            "MAKSIMAR_CORE_LIB/workers_registry",
            "MAKSIMAR_CORE_LIB/execution_control",
            "MAKSIMAR_CORE_LIB/security_layer",
            "MAKSIMAR_CORE_LIB/security_layer/approval_service_contract.py",
            "MAKSIMAR_SERVER/PROPOSAL_AUDIT",
        ),
        duplicated_registry_surfaces=(),
        proposal_only=True,
        disabled_by_default=True,
        direct_execution_allowed=False,
        direct_shell_allowed=False,
        direct_core_write_allowed=False,
        direct_app_control_allowed=False,
        model_download_allowed=False,
        runtime_start_allowed=False,
        dashboard_execution_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "jarvis_live_contract_entry_only",
            "existing_ai_services_reused",
            "existing_ai_router_binding_reused",
            "existing_workers_registry_reused",
            "security_approval_audit_required_before_runtime",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
