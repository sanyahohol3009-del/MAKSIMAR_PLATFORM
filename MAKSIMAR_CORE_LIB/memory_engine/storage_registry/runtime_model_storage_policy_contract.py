from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RUNTIME_MODEL_ROOTS: tuple[str, ...] = (
    "~/MAKSIMAR_RUNTIME/runtime_models/chat",
    "~/MAKSIMAR_RUNTIME/runtime_models/planner",
    "~/MAKSIMAR_RUNTIME/runtime_models/coder",
    "~/MAKSIMAR_RUNTIME/runtime_models/vision",
    "~/MAKSIMAR_RUNTIME/runtime_models/stt",
    "~/MAKSIMAR_RUNTIME/runtime_models/tts",
    "~/MAKSIMAR_RUNTIME/runtime_models/image",
    "~/MAKSIMAR_RUNTIME/runtime_models/video",
    "~/MAKSIMAR_RUNTIME/runtime_models/3d",
    "~/MAKSIMAR_RUNTIME/runtime_models/robotics",
    "~/MAKSIMAR_RUNTIME/runtime_models/embedding",
    "~/MAKSIMAR_RUNTIME/runtime_models/reranker",
)


FORBIDDEN_MODEL_STORAGE_MARKERS: tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB",
    "MAKSIMAR_SERVER",
    "docs/",
    "tests/",
    "memory_engine",
    "oob_dashboard",
    ".git",
)


@dataclass(frozen=True, slots=True)
class RuntimeModelStoragePolicy:
    policy_id: str
    allowed_roots: tuple[str, ...]
    forbidden_markers: tuple[str, ...]
    runtime_assets_only: bool
    project_truth_allowed: bool
    git_storage_allowed: bool
    core_storage_allowed: bool
    dashboard_storage_allowed: bool
    model_download_allowed: bool
    runtime_start_allowed: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.policy_id, "policy_id")
        _require_non_empty_tuple(self.allowed_roots, "allowed_roots")
        _require_non_empty_tuple(self.forbidden_markers, "forbidden_markers")

        for root in self.allowed_roots:
            if not root.startswith("~/MAKSIMAR_RUNTIME/runtime_models/"):
                raise ValueError("model roots must live under ~/MAKSIMAR_RUNTIME/runtime_models")
            for marker in self.forbidden_markers:
                if marker in root:
                    raise ValueError(f"model root contains forbidden marker: {marker}")

        _require_true(self.runtime_assets_only, "runtime_assets_only")
        _require_false(self.project_truth_allowed, "project_truth_allowed")
        _require_false(self.git_storage_allowed, "git_storage_allowed")
        _require_false(self.core_storage_allowed, "core_storage_allowed")
        _require_false(self.dashboard_storage_allowed, "dashboard_storage_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_true(self.read_only, "read_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "allowed_roots": self.allowed_roots,
            "forbidden_markers": self.forbidden_markers,
            "runtime_assets_only": self.runtime_assets_only,
            "project_truth_allowed": self.project_truth_allowed,
            "git_storage_allowed": self.git_storage_allowed,
            "core_storage_allowed": self.core_storage_allowed,
            "dashboard_storage_allowed": self.dashboard_storage_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "read_only": self.read_only,
        }


def build_runtime_model_storage_policy() -> RuntimeModelStoragePolicy:
    return RuntimeModelStoragePolicy(
        policy_id="jarvis_live_runtime_model_storage_policy_v1",
        allowed_roots=RUNTIME_MODEL_ROOTS,
        forbidden_markers=FORBIDDEN_MODEL_STORAGE_MARKERS,
        runtime_assets_only=True,
        project_truth_allowed=False,
        git_storage_allowed=False,
        core_storage_allowed=False,
        dashboard_storage_allowed=False,
        model_download_allowed=False,
        runtime_start_allowed=False,
        read_only=True,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    for item in value:
        _require_non_empty(item, field_name)


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
