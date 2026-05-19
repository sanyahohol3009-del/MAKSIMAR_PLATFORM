from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import (
    RollbackManagerReadinessReadModel,
)
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotManagerReadinessReadModel,
)


RECOVERY_SERVICE_CONTRACT_ID = "recovery_service_contract_v1"


class RecoveryServiceReadinessStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RecoveryServiceReadinessReadModel:
    read_model_id: str
    contract_id: str
    package_id: str
    status: RecoveryServiceReadinessStatus
    snapshot_readiness: SnapshotManagerReadinessReadModel
    rollback_readiness: RollbackManagerReadinessReadModel
    recovery_ready: bool
    recovery_service_bound: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if self.contract_id != RECOVERY_SERVICE_CONTRACT_ID:
            raise ValueError("contract_id must be recovery_service_contract_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, RecoveryServiceReadinessStatus):
            raise TypeError("status must be RecoveryServiceReadinessStatus")
        if not isinstance(self.snapshot_readiness, SnapshotManagerReadinessReadModel):
            raise TypeError("snapshot_readiness must be SnapshotManagerReadinessReadModel")
        if not isinstance(self.rollback_readiness, RollbackManagerReadinessReadModel):
            raise TypeError("rollback_readiness must be RollbackManagerReadinessReadModel")
        if self.status is RecoveryServiceReadinessStatus.READY:
            if not self.recovery_ready:
                raise ValueError("READY recovery readiness requires recovery_ready true")
            if not self.recovery_service_bound:
                raise ValueError("READY recovery readiness requires recovery_service_bound true")
            if not self.snapshot_readiness.snapshot_ready:
                raise ValueError("READY recovery readiness requires snapshot readiness")
            if not self.rollback_readiness.rollback_ready:
                raise ValueError("READY recovery readiness requires rollback readiness")
        if self.status is RecoveryServiceReadinessStatus.BLOCKED and self.recovery_ready:
            raise ValueError("BLOCKED recovery readiness cannot have recovery_ready true")
        _validate_reason_codes(self.reason_codes)
        _validate_safety_flags(
            dashboard_safe=self.dashboard_safe,
            direct_apply_allowed=self.direct_apply_allowed,
            canonical_write_allowed=self.canonical_write_allowed,
            dashboard_execution_allowed=self.dashboard_execution_allowed,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "contract_id": self.contract_id,
            "package_id": self.package_id,
            "status": self.status.value,
            "snapshot_readiness": self.snapshot_readiness.to_dict(),
            "rollback_readiness": self.rollback_readiness.to_dict(),
            "recovery_ready": self.recovery_ready,
            "recovery_service_bound": self.recovery_service_bound,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_recovery_service_ready_read_model(
    *,
    package_id: str,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
    rollback_readiness: RollbackManagerReadinessReadModel,
) -> RecoveryServiceReadinessReadModel:
    return RecoveryServiceReadinessReadModel(
        read_model_id=f"recovery_service_readiness:{package_id}",
        contract_id=RECOVERY_SERVICE_CONTRACT_ID,
        package_id=package_id,
        status=RecoveryServiceReadinessStatus.READY,
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
        recovery_ready=True,
        recovery_service_bound=True,
        reason_codes=("recovery_service_bound", "snapshot_ready", "rollback_ready"),
    )


def build_recovery_service_blocked_read_model(
    *,
    package_id: str,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
    rollback_readiness: RollbackManagerReadinessReadModel,
    reason_codes: tuple[str, ...],
) -> RecoveryServiceReadinessReadModel:
    return RecoveryServiceReadinessReadModel(
        read_model_id=f"recovery_service_readiness:{package_id}",
        contract_id=RECOVERY_SERVICE_CONTRACT_ID,
        package_id=package_id,
        status=RecoveryServiceReadinessStatus.BLOCKED,
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
        recovery_ready=False,
        recovery_service_bound=False,
        reason_codes=reason_codes,
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


def _validate_safety_flags(
    *,
    dashboard_safe: bool,
    direct_apply_allowed: bool,
    canonical_write_allowed: bool,
    dashboard_execution_allowed: bool,
) -> None:
    if not dashboard_safe:
        raise ValueError("dashboard_safe must remain true")
    if direct_apply_allowed:
        raise ValueError("direct_apply_allowed must remain false")
    if canonical_write_allowed:
        raise ValueError("canonical_write_allowed must remain false")
    if dashboard_execution_allowed:
        raise ValueError("dashboard_execution_allowed must remain false")
