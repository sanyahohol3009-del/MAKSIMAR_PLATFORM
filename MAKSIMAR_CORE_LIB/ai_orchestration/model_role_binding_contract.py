from __future__ import annotations

from dataclasses import dataclass
from typing import Any


JARVIS_LIVE_MODEL_ROLES: tuple[str, ...] = (
    "chat",
    "planner",
    "coder",
    "vision",
    "stt",
    "tts",
    "retrieval",
    "embedding",
    "reranker",
    "image",
    "video",
    "external_task_broker",
)


@dataclass(frozen=True, slots=True)
class ModelRoleBinding:
    role: str
    existing_service_surface: str
    existing_router_surface: str
    existing_worker_surface: str
    existing_execution_surface: str
    existing_security_surface: str
    existing_audit_surface: str
    proposal_only: bool
    enabled: bool
    direct_execution_allowed: bool
    direct_shell_allowed: bool
    direct_core_write_allowed: bool
    direct_app_control_allowed: bool
    model_download_allowed: bool
    runtime_start_allowed: bool

    def __post_init__(self) -> None:
        _require_role(self.role)
        for field_name in (
            "existing_service_surface",
            "existing_router_surface",
            "existing_worker_surface",
            "existing_execution_surface",
            "existing_security_surface",
            "existing_audit_surface",
        ):
            _require_non_empty(getattr(self, field_name), field_name)

        _require_true(self.proposal_only, "proposal_only")
        _require_false(self.enabled, "enabled")
        _require_false(self.direct_execution_allowed, "direct_execution_allowed")
        _require_false(self.direct_shell_allowed, "direct_shell_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_app_control_allowed, "direct_app_control_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "existing_service_surface": self.existing_service_surface,
            "existing_router_surface": self.existing_router_surface,
            "existing_worker_surface": self.existing_worker_surface,
            "existing_execution_surface": self.existing_execution_surface,
            "existing_security_surface": self.existing_security_surface,
            "existing_audit_surface": self.existing_audit_surface,
            "proposal_only": self.proposal_only,
            "enabled": self.enabled,
            "direct_execution_allowed": self.direct_execution_allowed,
            "direct_shell_allowed": self.direct_shell_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_app_control_allowed": self.direct_app_control_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
        }


def build_default_model_role_bindings() -> tuple[ModelRoleBinding, ...]:
    return tuple(
        ModelRoleBinding(
            role=role,
            existing_service_surface="AI_SERVICES/config",
            existing_router_surface="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            existing_worker_surface="MAKSIMAR_CORE_LIB/workers_registry",
            existing_execution_surface="MAKSIMAR_CORE_LIB/execution_control",
            existing_security_surface="MAKSIMAR_CORE_LIB/security_layer",
            existing_audit_surface="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            proposal_only=True,
            enabled=False,
            direct_execution_allowed=False,
            direct_shell_allowed=False,
            direct_core_write_allowed=False,
            direct_app_control_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
        )
        for role in JARVIS_LIVE_MODEL_ROLES
    )


def _require_role(value: str) -> None:
    if value not in JARVIS_LIVE_MODEL_ROLES:
        raise ValueError(f"unknown model role: {value!r}")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
