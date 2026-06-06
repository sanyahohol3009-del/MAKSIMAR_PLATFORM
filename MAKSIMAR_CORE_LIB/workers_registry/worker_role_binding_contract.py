from __future__ import annotations

from dataclasses import dataclass
from typing import Any


WORKER_ROLE_BINDING_SURFACES: tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/workers_registry",
    "MAKSIMAR_CORE_LIB/workers_runtime",
    "MAKSIMAR_CORE_LIB/execution_control",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION",
)

JARVIS_LIVE_WORKER_ROLES: tuple[str, ...] = (
    "model_chat",
    "model_planner",
    "model_coder",
    "model_vision",
    "model_stt",
    "model_tts",
    "model_retrieval",
    "model_embedding",
    "model_reranker",
    "model_image",
    "model_video",
    "external_task_broker",
    "voice_runtime",
    "screen_observer",
)


@dataclass(frozen=True, slots=True)
class WorkerRoleBinding:
    role: str
    canonical_worker_id: str
    source_surface: str
    reused_existing_worker_registry: bool = True
    new_worker_registry_created: bool = False
    runtime_start_allowed: bool = False
    direct_execution_allowed: bool = False
    shell_allowed: bool = False
    model_download_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_member(self.role, JARVIS_LIVE_WORKER_ROLES, "role")
        _require_non_empty(self.canonical_worker_id, "canonical_worker_id")
        _require_member(self.source_surface, WORKER_ROLE_BINDING_SURFACES, "source_surface")
        if self.reused_existing_worker_registry is not True:
            raise ValueError("worker role bindings must reuse the existing worker registry")
        if self.new_worker_registry_created is not False:
            raise ValueError("worker role bindings must not create a new worker registry")
        _require_disabled(self.runtime_start_allowed, "runtime_start_allowed")
        _require_disabled(self.direct_execution_allowed, "direct_execution_allowed")
        _require_disabled(self.shell_allowed, "shell_allowed")
        _require_disabled(self.model_download_allowed, "model_download_allowed")
        _require_disabled(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "canonical_worker_id": self.canonical_worker_id,
            "source_surface": self.source_surface,
            "reused_existing_worker_registry": self.reused_existing_worker_registry,
            "new_worker_registry_created": self.new_worker_registry_created,
            "runtime_start_allowed": self.runtime_start_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "shell_allowed": self.shell_allowed,
            "model_download_allowed": self.model_download_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class WorkerRoleBindingContract:
    bindings: tuple[WorkerRoleBinding, ...]
    referenced_surfaces: tuple[str, ...] = WORKER_ROLE_BINDING_SURFACES
    reused_existing_worker_registry: bool = True
    new_worker_registry_created: bool = False
    runtime_start_allowed: bool = False
    direct_execution_allowed: bool = False
    shell_allowed: bool = False
    model_download_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.bindings:
            raise ValueError("bindings must not be empty")
        roles = tuple(binding.role for binding in self.bindings)
        if roles != JARVIS_LIVE_WORKER_ROLES:
            raise ValueError("bindings must cover every JARVIS-LIVE worker role in order")
        for surface in self.referenced_surfaces:
            _require_member(surface, WORKER_ROLE_BINDING_SURFACES, "referenced_surfaces")
        if self.reused_existing_worker_registry is not True:
            raise ValueError("contract must reuse the existing worker registry")
        if self.new_worker_registry_created is not False:
            raise ValueError("contract must not create a new worker registry")
        _require_disabled(self.runtime_start_allowed, "runtime_start_allowed")
        _require_disabled(self.direct_execution_allowed, "direct_execution_allowed")
        _require_disabled(self.shell_allowed, "shell_allowed")
        _require_disabled(self.model_download_allowed, "model_download_allowed")
        _require_disabled(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "bindings": tuple(binding.to_read_model() for binding in self.bindings),
            "role_count": len(self.bindings),
            "roles": tuple(binding.role for binding in self.bindings),
            "canonical_worker_ids": tuple(
                dict.fromkeys(binding.canonical_worker_id for binding in self.bindings)
            ),
            "referenced_surfaces": self.referenced_surfaces,
            "reused_existing_worker_registry": self.reused_existing_worker_registry,
            "new_worker_registry_created": self.new_worker_registry_created,
            "runtime_start_allowed": self.runtime_start_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "shell_allowed": self.shell_allowed,
            "model_download_allowed": self.model_download_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_disabled(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")


DEFAULT_WORKER_ROLE_BINDINGS: tuple[WorkerRoleBinding, ...] = (
    WorkerRoleBinding("model_chat", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_planner", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_coder", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_vision", "worker_sim_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_stt", "worker_voice_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_tts", "worker_voice_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_retrieval", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_embedding", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_reranker", "worker_ai_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_image", "worker_sim_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding("model_video", "worker_sim_001", "MAKSIMAR_CORE_LIB/workers_registry"),
    WorkerRoleBinding(
        "external_task_broker",
        "worker_ai_001",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION",
    ),
    WorkerRoleBinding("voice_runtime", "worker_voice_001", "MAKSIMAR_CORE_LIB/workers_runtime"),
    WorkerRoleBinding("screen_observer", "worker_sim_001", "MAKSIMAR_CORE_LIB/workers_runtime"),
)


def build_worker_role_binding_contract() -> WorkerRoleBindingContract:
    return WorkerRoleBindingContract(bindings=DEFAULT_WORKER_ROLE_BINDINGS)


def list_worker_role_bindings() -> tuple[WorkerRoleBinding, ...]:
    return build_worker_role_binding_contract().bindings
