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
            "model_download_allowed_now": True,
            "runtime_start_allowed_now": False,
        }


@dataclass(frozen=True, slots=True)
class JarvisRuntimeModelRoleProfile:
    role_id: str
    model_id: str
    target_model_id: str
    status: str
    role: str
    use_cases: tuple[str, ...]
    load_policy: str
    exclusive_gpu: bool
    default_context_tokens: int
    max_safe_context_tokens: int
    installed: bool
    proposal_only: bool
    agents_direct_access_allowed: bool
    model_download_allowed: bool
    runtime_start_allowed: bool
    pc_control_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("role_id", "model_id", "target_model_id", "status", "role", "load_policy"):
            _require_non_empty(getattr(self, field_name), field_name)
        if self.status not in ("installed", "planned", "not_installed"):
            raise ValueError(f"unsupported model profile status: {self.status!r}")
        if not self.use_cases:
            raise ValueError("use_cases must not be empty")
        if self.default_context_tokens <= 0 or self.max_safe_context_tokens <= 0:
            raise ValueError("context token limits must be positive")
        if self.default_context_tokens > self.max_safe_context_tokens:
            raise ValueError("default_context_tokens must not exceed max_safe_context_tokens")
        _require_true(self.proposal_only, "proposal_only")
        _require_false(self.agents_direct_access_allowed, "agents_direct_access_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        if self.role_id == "heavy_coder_model":
            if self.model_id != "jarvis:coder14b":
                raise ValueError("heavy_coder_model must use installed jarvis:coder14b wrapper")
            _require_true(self.exclusive_gpu, "exclusive_gpu")
            if self.load_policy != "load_on_demand":
                raise ValueError("heavy_coder_model must be load_on_demand")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "role_id": self.role_id,
            "model_id": self.model_id,
            "target_model_id": self.target_model_id,
            "status": self.status,
            "role": self.role,
            "use_cases": self.use_cases,
            "load_policy": self.load_policy,
            "exclusive_gpu": self.exclusive_gpu,
            "default_context_tokens": self.default_context_tokens,
            "max_safe_context_tokens": self.max_safe_context_tokens,
            "installed": self.installed,
            "proposal_only": self.proposal_only,
            "agents_direct_access_allowed": self.agents_direct_access_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


def build_jarvis_live_runtime_model_role_profiles() -> tuple[JarvisRuntimeModelRoleProfile, ...]:
    return (
        JarvisRuntimeModelRoleProfile(
            role_id="heavy_coder_model",
            model_id="jarvis:coder14b",
            target_model_id="qwen2.5-coder:14b",
            status="installed",
            role="heavy_coder",
            use_cases=(
                "traceback analysis",
                "complex code review",
                "patch proposal",
                "architecture check",
                "complex bug-fix planning",
            ),
            load_policy="load_on_demand",
            exclusive_gpu=True,
            default_context_tokens=4096,
            max_safe_context_tokens=8192,
            installed=True,
            proposal_only=True,
            agents_direct_access_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            pc_control_allowed=False,
        ),
        JarvisRuntimeModelRoleProfile(
            role_id="daily_coder_model",
            model_id="jarvis:coder7b",
            target_model_id="qwen2.5-coder:7b",
            status="installed",
            role="daily_coder",
            use_cases=(
                "simple code review",
                "small bug-fix plan",
                "pytest failure explanation",
                "quick coding help",
            ),
            load_policy="installed_ollama_wrapper",
            exclusive_gpu=False,
            default_context_tokens=4096,
            max_safe_context_tokens=6144,
            installed=True,
            proposal_only=True,
            agents_direct_access_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            pc_control_allowed=False,
        ),
        JarvisRuntimeModelRoleProfile(
            role_id="helper_classifier_model",
            model_id="jarvis:helper3b",
            target_model_id="qwen2.5-coder:3b",
            status="installed",
            role="helper_classifier",
            use_cases=("task classification", "route selection", "short summaries", "cheap checks"),
            load_policy="installed_ollama_wrapper",
            exclusive_gpu=False,
            default_context_tokens=2048,
            max_safe_context_tokens=4096,
            installed=True,
            proposal_only=True,
            agents_direct_access_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            pc_control_allowed=False,
        ),
        JarvisRuntimeModelRoleProfile(
            role_id="jarvis_chat_model",
            model_id="jarvis:chat8b",
            target_model_id="qwen3:8b",
            status="installed",
            role="jarvis_chat",
            use_cases=("daily conversation", "planning", "simple explanations", "voice interaction"),
            load_policy="installed_ollama_wrapper",
            exclusive_gpu=False,
            default_context_tokens=4096,
            max_safe_context_tokens=8192,
            installed=True,
            proposal_only=True,
            agents_direct_access_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            pc_control_allowed=False,
        ),
    )


def build_jarvis_live_runtime_model_role_read_model() -> dict[str, Any]:
    profiles = build_jarvis_live_runtime_model_role_profiles()
    return {
        "profile_map_id": "jarvis_live_runtime_model_role_profile_map_v1",
        "profiles": tuple(profile.to_read_model() for profile in profiles),
        "heavy_coder_model_id": "jarvis:coder14b",
        "heavy_coder_base_model_id": "qwen2.5-coder:14b",
        "heavy_coder_load_policy": "load_on_demand",
        "heavy_coder_exclusive_gpu": True,
        "installed_ollama_wrappers": (
            "jarvis:chat8b",
            "jarvis:helper3b",
            "jarvis:coder7b",
            "jarvis:coder14b",
        ),
        "ollama_model_storage_root": "~/MAKSIMAR_RUNTIME/runtime_models/ollama",
        "missing_future_models_are_planned": False,
        "agents_enabled": False,
        "agents_may_call_14b_directly": False,
        "model_download_allowed": False,
        "runtime_start_allowed": False,
        "pc_control_allowed": False,
        "reused_existing_registry": "MAKSIMAR_CORE_LIB/ai_orchestration/model_profile_registry_contract.py",
        "reused_router_surface": "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_router.py",
        "reused_execution_surface": "MAKSIMAR_CORE_LIB/execution_control",
    }


def select_jarvis_live_model_role(request_text: str) -> dict[str, Any]:
    lowered = request_text.casefold()
    if any(marker in lowered for marker in ("классифиц", "summary", "сводк", "кратко проверь")):
        role_id = "helper_classifier_model"
        route_reason = "classification_or_summary"
    elif any(
        marker in lowered
        for marker in ("traceback", "architecture", "архитектур", "сложн", "патч", "diff", "complex", "регресс")
    ):
        role_id = "heavy_coder_model"
        route_reason = "complex_code_or_architecture"
    elif any(marker in lowered for marker in ("клик", "открой", "запусти", "мыш", "клавиат", "браузер")):
        role_id = "jarvis_chat_model"
        route_reason = "pc_action_request_proposal_only"
    elif any(
        marker in lowered
        for marker in ("pytest", "ошибка", "код", "git", "тест", "файл", "python", "brokenpipe")
    ):
        role_id = "daily_coder_model"
        route_reason = "simple_code_help"
    else:
        role_id = "jarvis_chat_model"
        route_reason = "normal_conversation"
    profiles = {profile.role_id: profile for profile in build_jarvis_live_runtime_model_role_profiles()}
    profile = profiles[role_id].to_read_model()
    return {
        **profile,
        "selected_model_role": role_id,
        "route_reason": route_reason,
        "direct_execution_allowed": False,
        "pc_control_allowed": False,
        "model_download_allowed": False,
        "runtime_start_allowed": False,
        "enqueue_required": True,
        "admission_required": True,
        "resource_gate_required": True,
        "queue_surface": "MAKSIMAR_CORE_LIB/execution_control",
        "worker_registry_surface": "MAKSIMAR_CORE_LIB/workers_registry",
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
