from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotManagerReadinessReadModel,
    SnapshotReference,
    build_snapshot_blocked_read_model,
    build_snapshot_ready_read_model,
)


SNAPSHOT_MANAGER_RUNTIME_ID = "snapshot_manager_runtime_v1"


@dataclass(frozen=True, slots=True)
class SnapshotManagerRuntimeResult:
    runtime_id: str
    package_id: str
    read_model: SnapshotManagerReadinessReadModel
    wrapper_only: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.runtime_id != SNAPSHOT_MANAGER_RUNTIME_ID:
            raise ValueError("runtime_id must be snapshot_manager_runtime_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.read_model, SnapshotManagerReadinessReadModel):
            raise TypeError("read_model must be SnapshotManagerReadinessReadModel")
        if not self.wrapper_only:
            raise ValueError("wrapper_only must remain true")
        _validate_runtime_safety_flags(
            runtime_apply_allowed=self.runtime_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_id": self.runtime_id,
            "package_id": self.package_id,
            "read_model": self.read_model.to_dict(),
            "wrapper_only": self.wrapper_only,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "reason_codes": self.reason_codes,
        }


def run_snapshot_manager_ready(
    *,
    package_id: str,
    snapshot_reference: SnapshotReference,
) -> SnapshotManagerRuntimeResult:
    read_model = build_snapshot_ready_read_model(
        package_id=package_id,
        snapshot_reference=snapshot_reference,
    )
    return SnapshotManagerRuntimeResult(
        runtime_id=SNAPSHOT_MANAGER_RUNTIME_ID,
        package_id=package_id,
        read_model=read_model,
        wrapper_only=True,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=("snapshot_manager_runtime_wrapped_contract",),
    )


def run_snapshot_manager_blocked(
    *,
    package_id: str,
    reason_codes: tuple[str, ...],
) -> SnapshotManagerRuntimeResult:
    read_model = build_snapshot_blocked_read_model(
        package_id=package_id,
        reason_codes=reason_codes,
    )
    return SnapshotManagerRuntimeResult(
        runtime_id=SNAPSHOT_MANAGER_RUNTIME_ID,
        package_id=package_id,
        read_model=read_model,
        wrapper_only=True,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        reason_codes=("snapshot_manager_runtime_wrapped_blocked_contract",),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        _validate_non_empty("reason_code", reason_code)


def _validate_runtime_safety_flags(
    *,
    runtime_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if runtime_apply_allowed:
        raise ValueError("runtime_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
