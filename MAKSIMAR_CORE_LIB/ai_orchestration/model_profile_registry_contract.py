from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_resource_requirements_contract import (
    ModelResourceRequirement,
    build_default_model_resource_requirements,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_role_binding_contract import (
    JARVIS_LIVE_MODEL_ROLES,
    ModelRoleBinding,
    build_default_model_role_bindings,
)


@dataclass(frozen=True, slots=True)
class ModelProfile:
    profile_id: str
    role: str
    candidate_family: str
    existing_service_surface: str
    resource_requirement_id: str
    runtime_asset_subdir: str
    proposal_only: bool
    enabled: bool
    model_download_allowed: bool
    runtime_start_allowed: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.profile_id, "profile_id")
        if self.role not in JARVIS_LIVE_MODEL_ROLES:
            raise ValueError(f"unknown model role: {self.role!r}")
        for field_name in (
            "candidate_family",
            "existing_service_surface",
            "resource_requirement_id",
            "runtime_asset_subdir",
        ):
            _require_non_empty(getattr(self, field_name), field_name)
        _require_true(self.proposal_only, "proposal_only")
        _require_false(self.enabled, "enabled")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "role": self.role,
            "candidate_family": self.candidate_family,
            "existing_service_surface": self.existing_service_surface,
            "resource_requirement_id": self.resource_requirement_id,
            "runtime_asset_subdir": self.runtime_asset_subdir,
            "proposal_only": self.proposal_only,
            "enabled": self.enabled,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
        }


@dataclass(frozen=True, slots=True)
class ModelProfileRegistry:
    registry_id: str
    profiles: tuple[ModelProfile, ...]
    role_bindings: tuple[ModelRoleBinding, ...]
    resource_requirements: tuple[ModelResourceRequirement, ...]
    referenced_architecture_surfaces: tuple[str, ...]
    duplicated_registry_surfaces: tuple[str, ...]
    read_only: bool
    dashboard_safe: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.registry_id, "registry_id")
        if {profile.role for profile in self.profiles} != set(JARVIS_LIVE_MODEL_ROLES):
            raise ValueError("profiles must cover every JARVIS-LIVE model role")
        if {binding.role for binding in self.role_bindings} != set(JARVIS_LIVE_MODEL_ROLES):
            raise ValueError("role_bindings must cover every JARVIS-LIVE model role")
        if {requirement.role for requirement in self.resource_requirements} != set(JARVIS_LIVE_MODEL_ROLES):
            raise ValueError("resource_requirements must cover every JARVIS-LIVE model role")
        for surface in (
            "AI_SERVICES/config",
            "MAKSIMAR_CORE_LIB/ai_orchestration",
            "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            "MAKSIMAR_CORE_LIB/workers_registry",
            "MAKSIMAR_CORE_LIB/execution_control",
        ):
            if surface not in self.referenced_architecture_surfaces:
                raise ValueError(f"missing referenced architecture surface: {surface}")
        if self.duplicated_registry_surfaces:
            raise ValueError("duplicated_registry_surfaces must remain empty")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "profiles": tuple(profile.to_read_model() for profile in self.profiles),
            "role_bindings": tuple(binding.to_read_model() for binding in self.role_bindings),
            "resource_requirements": tuple(
                requirement.to_read_model() for requirement in self.resource_requirements
            ),
            "referenced_architecture_surfaces": self.referenced_architecture_surfaces,
            "duplicated_registry_surfaces": self.duplicated_registry_surfaces,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "model_download_allowed_now": False,
            "runtime_start_allowed_now": False,
        }


def build_default_model_profiles() -> tuple[ModelProfile, ...]:
    candidate_by_role = {
        "chat": "qwen-class-chat-candidate",
        "planner": "qwen-class-planner-candidate",
        "coder": "qwen-coder-class-candidate",
        "vision": "vision-vlm-candidate",
        "stt": "stt-candidate",
        "tts": "tts-candidate",
        "retrieval": "retrieval-router-candidate",
        "embedding": "embedding-candidate",
        "reranker": "reranker-candidate",
        "image": "image-service-candidate",
        "video": "video-service-candidate",
        "external_task_broker": "external-task-broker-candidate",
    }
    return tuple(
        ModelProfile(
            profile_id=f"jarvis_live_model_profile_{role}",
            role=role,
            candidate_family=candidate_by_role[role],
            existing_service_surface="AI_SERVICES/config",
            resource_requirement_id=f"jarvis_live_resource_requirement_{role}",
            runtime_asset_subdir=role,
            proposal_only=True,
            enabled=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
        )
        for role in JARVIS_LIVE_MODEL_ROLES
    )


def build_model_profile_registry() -> ModelProfileRegistry:
    return ModelProfileRegistry(
        registry_id="jarvis_live_model_profile_registry_v1",
        profiles=build_default_model_profiles(),
        role_bindings=build_default_model_role_bindings(),
        resource_requirements=build_default_model_resource_requirements(),
        referenced_architecture_surfaces=(
            "AI_SERVICES/config",
            "MAKSIMAR_CORE_LIB/ai_orchestration",
            "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            "MAKSIMAR_CORE_LIB/workers_registry",
            "MAKSIMAR_CORE_LIB/execution_control",
        ),
        duplicated_registry_surfaces=(),
        read_only=True,
        dashboard_safe=True,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
