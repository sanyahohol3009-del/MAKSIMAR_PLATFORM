from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


AI_SERVICE_BINDING_PATHS: tuple[str, ...] = (
    "AI_SERVICES",
    "MAKSIMAR_CORE_LIB/ai_services",
    "MAKSIMAR_CORE_LIB/real_ai_services_model_adapters",
)

WORKER_BINDING_PATHS: tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/workers_registry",
    "MAKSIMAR_CORE_LIB/workers_runtime",
    "MAKSIMAR_SERVER/WORKERS",
    "MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE",
)

CONTROL_PLANE_AI_ROUTER_BINDING_PATHS: tuple[str, ...] = (
    "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
    "CONTROL_PLANE",
    "MAKSIMAR_SERVER/CONTROL_PLANE",
)


@dataclass(frozen=True, slots=True)
class ExistingAIOrchestrationBindingReadModel:
    read_model_id: str
    layer_id: str
    ai_services_bound: bool
    workers_bound: bool
    control_plane_ai_router_bound: bool
    ai_service_binding_paths: tuple[str, ...]
    worker_binding_paths: tuple[str, ...]
    control_plane_ai_router_binding_paths: tuple[str, ...]
    duplicate_ai_services_allowed: bool
    duplicate_workers_allowed: bool
    duplicate_router_allowed: bool
    mempalace_source_of_truth: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_non_empty("layer_id", self.layer_id)
        _validate_true("ai_services_bound", self.ai_services_bound)
        _validate_true("workers_bound", self.workers_bound)
        _validate_true("control_plane_ai_router_bound", self.control_plane_ai_router_bound)
        _validate_non_empty_tuple("ai_service_binding_paths", self.ai_service_binding_paths)
        _validate_non_empty_tuple("worker_binding_paths", self.worker_binding_paths)
        _validate_non_empty_tuple(
            "control_plane_ai_router_binding_paths",
            self.control_plane_ai_router_binding_paths,
        )
        _validate_false("duplicate_ai_services_allowed", self.duplicate_ai_services_allowed)
        _validate_false("duplicate_workers_allowed", self.duplicate_workers_allowed)
        _validate_false("duplicate_router_allowed", self.duplicate_router_allowed)
        _validate_false("mempalace_source_of_truth", self.mempalace_source_of_truth)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_id": self.layer_id,
            "ai_services_bound": self.ai_services_bound,
            "workers_bound": self.workers_bound,
            "control_plane_ai_router_bound": self.control_plane_ai_router_bound,
            "ai_service_binding_paths": self.ai_service_binding_paths,
            "worker_binding_paths": self.worker_binding_paths,
            "control_plane_ai_router_binding_paths": self.control_plane_ai_router_binding_paths,
            "duplicate_ai_services_allowed": self.duplicate_ai_services_allowed,
            "duplicate_workers_allowed": self.duplicate_workers_allowed,
            "duplicate_router_allowed": self.duplicate_router_allowed,
            "mempalace_source_of_truth": self.mempalace_source_of_truth,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, slots=True)
class AIOrchestrationSurfaceReadModel:
    read_model_id: str
    layer_id: str
    binding: ExistingAIOrchestrationBindingReadModel
    direct_autonomous_execution_allowed: bool
    proposal_execution_allowed: bool
    stage_execution_allowed: bool
    runtime_mutation_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        _validate_non_empty("layer_id", self.layer_id)
        if not isinstance(self.binding, ExistingAIOrchestrationBindingReadModel):
            raise TypeError("binding must be ExistingAIOrchestrationBindingReadModel")
        _validate_false(
            "direct_autonomous_execution_allowed",
            self.direct_autonomous_execution_allowed,
        )
        _validate_false("proposal_execution_allowed", self.proposal_execution_allowed)
        _validate_false("stage_execution_allowed", self.stage_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "layer_id": self.layer_id,
            "binding": self.binding.to_dict(),
            "direct_autonomous_execution_allowed": self.direct_autonomous_execution_allowed,
            "proposal_execution_allowed": self.proposal_execution_allowed,
            "stage_execution_allowed": self.stage_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_existing_ai_orchestration_binding_read_model(
    *,
    project_root: Path | None = None,
) -> ExistingAIOrchestrationBindingReadModel:
    root = Path.cwd() if project_root is None else project_root

    return ExistingAIOrchestrationBindingReadModel(
        read_model_id="existing_ai_orchestration_binding_read_model_v1",
        layer_id="AI_ORCHESTRATION",
        ai_services_bound=_all_paths_exist(root, AI_SERVICE_BINDING_PATHS),
        workers_bound=_all_paths_exist(root, WORKER_BINDING_PATHS),
        control_plane_ai_router_bound=_all_paths_exist(
            root,
            CONTROL_PLANE_AI_ROUTER_BINDING_PATHS,
        ),
        ai_service_binding_paths=AI_SERVICE_BINDING_PATHS,
        worker_binding_paths=WORKER_BINDING_PATHS,
        control_plane_ai_router_binding_paths=CONTROL_PLANE_AI_ROUTER_BINDING_PATHS,
        duplicate_ai_services_allowed=False,
        duplicate_workers_allowed=False,
        duplicate_router_allowed=False,
        mempalace_source_of_truth=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "bind_to_existing_ai_services",
            "bind_to_existing_workers",
            "bind_to_existing_control_plane_ai_router",
            "do_not_duplicate_existing_surfaces",
        ),
    )


def build_ai_orchestration_surface_read_model(
    *,
    project_root: Path | None = None,
) -> AIOrchestrationSurfaceReadModel:
    return AIOrchestrationSurfaceReadModel(
        read_model_id="ai_orchestration_surface_read_model_v1",
        layer_id="AI_ORCHESTRATION",
        binding=build_existing_ai_orchestration_binding_read_model(
            project_root=project_root,
        ),
        direct_autonomous_execution_allowed=False,
        proposal_execution_allowed=False,
        stage_execution_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_orchestration_surface_only",
            "proposal_stage_execution_blocked",
            "runtime_mutation_blocked",
            "deployment_blocked",
        ),
    )


def _all_paths_exist(root: Path, paths: tuple[str, ...]) -> bool:
    return all((root / path).exists() for path in paths)


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for item in value:
        _validate_non_empty(field_name, item)


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    _validate_tuple(field_name, value)
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
