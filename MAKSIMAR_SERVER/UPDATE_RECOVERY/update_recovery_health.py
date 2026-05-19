from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_recovery_read_model_builder import (
    UpdateRecoveryRuntimeReadModel,
)


UPDATE_RECOVERY_HEALTH_READ_MODEL_ID = "update_recovery_health_read_model_v1"


class UpdateRecoveryHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class UpdateRecoveryHealthReadModel:
    read_model_id: str
    status: UpdateRecoveryHealthStatus
    runtime_read_model: UpdateRecoveryRuntimeReadModel
    runtime_wrapper_only: bool
    existing_transport_preserved: bool
    existing_recovery_manager_preserved: bool
    update_recovery_ready_for_next_gate: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.read_model_id != UPDATE_RECOVERY_HEALTH_READ_MODEL_ID:
            raise ValueError("read_model_id must be update_recovery_health_read_model_v1")
        if not isinstance(self.status, UpdateRecoveryHealthStatus):
            raise TypeError("status must be UpdateRecoveryHealthStatus")
        if not isinstance(self.runtime_read_model, UpdateRecoveryRuntimeReadModel):
            raise TypeError("runtime_read_model must be UpdateRecoveryRuntimeReadModel")
        if not self.runtime_wrapper_only:
            raise ValueError("runtime_wrapper_only must remain true")
        if not self.existing_transport_preserved:
            raise ValueError("existing_transport_preserved must remain true")
        if not self.existing_recovery_manager_preserved:
            raise ValueError("existing_recovery_manager_preserved must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_runtime_safety_flags(
            runtime_apply_allowed=self.runtime_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "status": self.status.value,
            "runtime_read_model": self.runtime_read_model.to_dict(),
            "runtime_wrapper_only": self.runtime_wrapper_only,
            "existing_transport_preserved": self.existing_transport_preserved,
            "existing_recovery_manager_preserved": self.existing_recovery_manager_preserved,
            "update_recovery_ready_for_next_gate": self.update_recovery_ready_for_next_gate,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_update_recovery_health_read_model(
    runtime_read_model: UpdateRecoveryRuntimeReadModel,
) -> UpdateRecoveryHealthReadModel:
    if not isinstance(runtime_read_model, UpdateRecoveryRuntimeReadModel):
        raise TypeError("runtime_read_model must be UpdateRecoveryRuntimeReadModel")

    ready = runtime_read_model.readiness.update_recovery_ready_for_next_gate
    status = UpdateRecoveryHealthStatus.HEALTHY if ready else UpdateRecoveryHealthStatus.DEGRADED
    reason_codes = (
        ("update_recovery_runtime_healthy",)
        if ready
        else ("update_recovery_runtime_degraded",)
    ) + runtime_read_model.reason_codes

    return UpdateRecoveryHealthReadModel(
        read_model_id=UPDATE_RECOVERY_HEALTH_READ_MODEL_ID,
        status=status,
        runtime_read_model=runtime_read_model,
        runtime_wrapper_only=runtime_read_model.runtime_wrapper_only,
        existing_transport_preserved=runtime_read_model.existing_transport_preserved,
        existing_recovery_manager_preserved=runtime_read_model.existing_recovery_manager_preserved,
        update_recovery_ready_for_next_gate=ready,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        dashboard_safe=True,
        reason_codes=reason_codes,
    )


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        if not isinstance(reason_code, str):
            raise TypeError("reason_codes must contain strings")
        if not reason_code:
            raise ValueError("reason_codes must not contain empty values")


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
