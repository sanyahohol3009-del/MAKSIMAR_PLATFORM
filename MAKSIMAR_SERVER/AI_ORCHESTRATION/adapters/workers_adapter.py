from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkersAdapterReadModel:
    adapter_id: str
    target_surface: str
    existing_worker_binding_ref: str
    points_to_existing_workers: bool
    duplicates_worker_logic: bool
    worker_runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    proposal_only: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("adapter_id", self.adapter_id)
        _validate_non_empty("target_surface", self.target_surface)
        _validate_non_empty("existing_worker_binding_ref", self.existing_worker_binding_ref)
        _validate_true("points_to_existing_workers", self.points_to_existing_workers)
        _validate_false("duplicates_worker_logic", self.duplicates_worker_logic)
        _validate_false("worker_runtime_execution_allowed", self.worker_runtime_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "target_surface": self.target_surface,
            "existing_worker_binding_ref": self.existing_worker_binding_ref,
            "points_to_existing_workers": self.points_to_existing_workers,
            "duplicates_worker_logic": self.duplicates_worker_logic,
            "worker_runtime_execution_allowed": self.worker_runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "proposal_only": self.proposal_only,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_workers_adapter_read_model() -> WorkersAdapterReadModel:
    return WorkersAdapterReadModel(
        adapter_id="workers_adapter_v1",
        target_surface="MAKSIMAR_SERVER/WORKERS",
        existing_worker_binding_ref="AI_ORCHESTRATION/existing_bindings/worker_binding.yaml",
        points_to_existing_workers=True,
        duplicates_worker_logic=False,
        worker_runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        proposal_only=True,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "adapter_points_to_existing_workers",
            "no_worker_runtime_execution",
            "proposal_only",
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
