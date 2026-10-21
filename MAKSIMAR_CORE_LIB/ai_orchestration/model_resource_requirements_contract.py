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


@dataclass(frozen=True, slots=True)
class ModelLoadResourceDemand:
    """Validated full-load upper bound, not weights size or an execution permission.

    Peaks include weights, KV/context, workspace, offload and concurrent work.
    Accelerator placement uses verified physical identities. Unknown bounds are
    represented by no demand on the existing runtime profile.
    """

    model_id: str
    backend_id: str
    model_revision: str
    context_tokens: int
    max_concurrency: int
    peak_ram_bytes: int
    accelerator_bytes: tuple[tuple[str, int], ...]
    min_cpu_threads: int
    provenance: str
    max_observation_age_seconds: float
    bound_kind: str = "UNKNOWN"
    ram_headroom_bytes: int = 0
    accelerator_headroom_bytes: int = 0

    def __post_init__(self) -> None:
        import math
        for name in ("model_id", "backend_id", "model_revision", "provenance"):
            _require_non_empty(getattr(self, name), name)
        for name in ("context_tokens", "max_concurrency", "peak_ram_bytes", "min_cpu_threads"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(name + " must be a positive integer")
        for name in ("ram_headroom_bytes", "accelerator_headroom_bytes"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 0:
                raise ValueError(name + " must be a non-negative integer")
        age = self.max_observation_age_seconds
        if type(age) not in (int, float) or not math.isfinite(age) or age <= 0:
            raise ValueError("max_observation_age_seconds invalid")
        if self.bound_kind not in ("UNKNOWN", "VERIFIED_UPPER_BOUND"):
            raise ValueError("unsupported resource bound kind")
        if type(self.accelerator_bytes) is not tuple:
            raise ValueError("accelerator_bytes must be immutable")
        seen = set()
        for entry in self.accelerator_bytes:
            if type(entry) is not tuple or len(entry) != 2:
                raise ValueError("invalid accelerator placement")
            device, size = entry
            _require_non_empty(device, "physical accelerator identity")
            if device in seen or type(size) is not int or size <= 0:
                raise ValueError("duplicate or invalid accelerator placement")
            seen.add(device)
