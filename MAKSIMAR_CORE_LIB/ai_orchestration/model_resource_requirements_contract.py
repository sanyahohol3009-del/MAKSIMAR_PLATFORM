from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_role_binding_contract import (
    JARVIS_LIVE_MODEL_ROLES,
)


@dataclass(frozen=True, slots=True)
class ModelResourceRequirement:
    role: str
    requirement_id: str
    min_vram_gb: int
    preferred_vram_gb: int
    min_ram_gb: int
    min_cpu_threads: int
    queue_required: bool
    admission_required: bool
    resource_snapshot_required: bool
    runtime_asset_root: str
    model_download_allowed: bool
    runtime_start_allowed: bool

    def __post_init__(self) -> None:
        if self.role not in JARVIS_LIVE_MODEL_ROLES:
            raise ValueError(f"unknown model role: {self.role!r}")
        _require_non_empty(self.requirement_id, "requirement_id")
        _require_non_empty(self.runtime_asset_root, "runtime_asset_root")
        for field_name in ("min_vram_gb", "preferred_vram_gb", "min_ram_gb", "min_cpu_threads"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{field_name} must be a non-negative integer")
        if self.preferred_vram_gb < self.min_vram_gb:
            raise ValueError("preferred_vram_gb must be >= min_vram_gb")
        _require_true(self.queue_required, "queue_required")
        _require_true(self.admission_required, "admission_required")
        _require_true(self.resource_snapshot_required, "resource_snapshot_required")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "requirement_id": self.requirement_id,
            "min_vram_gb": self.min_vram_gb,
            "preferred_vram_gb": self.preferred_vram_gb,
            "min_ram_gb": self.min_ram_gb,
            "min_cpu_threads": self.min_cpu_threads,
            "queue_required": self.queue_required,
            "admission_required": self.admission_required,
            "resource_snapshot_required": self.resource_snapshot_required,
            "runtime_asset_root": self.runtime_asset_root,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
        }


def build_default_model_resource_requirements() -> tuple[ModelResourceRequirement, ...]:
    specs: dict[str, tuple[int, int, int, int]] = {
        "chat": (4, 8, 8, 4),
        "planner": (4, 8, 8, 4),
        "coder": (8, 12, 12, 6),
        "vision": (6, 12, 12, 6),
        "stt": (2, 6, 6, 4),
        "tts": (0, 4, 4, 2),
        "retrieval": (0, 2, 4, 2),
        "embedding": (0, 4, 4, 2),
        "reranker": (0, 4, 4, 2),
        "image": (8, 12, 16, 6),
        "video": (12, 24, 24, 8),
        "external_task_broker": (0, 0, 2, 1),
    }

    return tuple(
        ModelResourceRequirement(
            role=role,
            requirement_id=f"jarvis_live_resource_requirement_{role}",
            min_vram_gb=specs[role][0],
            preferred_vram_gb=specs[role][1],
            min_ram_gb=specs[role][2],
            min_cpu_threads=specs[role][3],
            queue_required=True,
            admission_required=True,
            resource_snapshot_required=True,
            runtime_asset_root="~/MAKSIMAR_RUNTIME/runtime_models",
            model_download_allowed=False,
            runtime_start_allowed=False,
        )
        for role in JARVIS_LIVE_MODEL_ROLES
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
