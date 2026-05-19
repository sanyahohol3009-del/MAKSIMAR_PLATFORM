from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotManagerReadinessReadModel,
)


ROLLBACK_MANAGER_CONTRACT_ID = "rollback_manager_contract_v1"


class RollbackReadinessStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RollbackPlanReference:
    rollback_plan_id: str
    rollback_uri: str
    rollback_sha256: str
    target_snapshot_id: str
    tested: bool
    reversible: bool

    def __post_init__(self) -> None:
        _validate_non_empty("rollback_plan_id", self.rollback_plan_id)
        _validate_non_empty("rollback_uri", self.rollback_uri)
        _validate_sha256("rollback_sha256", self.rollback_sha256)
        _validate_non_empty("target_snapshot_id", self.target_snapshot_id)
        if not self.tested:
            raise ValueError("tested must remain true")
        if not self.reversible:
            raise ValueError("reversible must remain true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_plan_id": self.rollback_plan_id,
            "rollback_uri": self.rollback_uri,
            "rollback_sha256": self.rollback_sha256,
            "target_snapshot_id": self.target_snapshot_id,
            "tested": self.tested,
            "reversible": self.reversible,
        }


@dataclass(frozen=True, slots=True)
class RollbackManagerReadinessReadModel:
    read_model_id: str
    contract_id: str
    package_id: str
    status: RollbackReadinessStatus
    rollback_plan_reference: RollbackPlanReference | None
    snapshot_readiness: SnapshotManagerReadinessReadModel
    rollback_ready: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if self.contract_id != ROLLBACK_MANAGER_CONTRACT_ID:
            raise ValueError("contract_id must be rollback_manager_contract_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, RollbackReadinessStatus):
            raise TypeError("status must be RollbackReadinessStatus")
        if not isinstance(self.snapshot_readiness, SnapshotManagerReadinessReadModel):
            raise TypeError("snapshot_readiness must be SnapshotManagerReadinessReadModel")
        if self.status is RollbackReadinessStatus.READY:
            if not self.rollback_ready:
                raise ValueError("READY rollback readiness requires rollback_ready true")
            if not isinstance(self.rollback_plan_reference, RollbackPlanReference):
                raise ValueError("READY rollback readiness requires rollback_plan_reference")
            if not self.snapshot_readiness.snapshot_ready:
                raise ValueError("READY rollback readiness requires snapshot readiness")
            if self.rollback_plan_reference.target_snapshot_id != self.snapshot_readiness.snapshot_reference.snapshot_id:
                raise ValueError("rollback plan must target the ready snapshot")
        if self.status is RollbackReadinessStatus.BLOCKED and self.rollback_ready:
            raise ValueError("BLOCKED rollback readiness cannot have rollback_ready true")
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
            "rollback_plan_reference": None if self.rollback_plan_reference is None else self.rollback_plan_reference.to_dict(),
            "snapshot_readiness": self.snapshot_readiness.to_dict(),
            "rollback_ready": self.rollback_ready,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_rollback_ready_read_model(
    *,
    package_id: str,
    rollback_plan_reference: RollbackPlanReference,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
) -> RollbackManagerReadinessReadModel:
    return RollbackManagerReadinessReadModel(
        read_model_id=f"rollback_manager_readiness:{package_id}",
        contract_id=ROLLBACK_MANAGER_CONTRACT_ID,
        package_id=package_id,
        status=RollbackReadinessStatus.READY,
        rollback_plan_reference=rollback_plan_reference,
        snapshot_readiness=snapshot_readiness,
        rollback_ready=True,
        reason_codes=("rollback_plan_available", "rollback_plan_tested", "snapshot_bound"),
    )


def build_rollback_blocked_read_model(
    *,
    package_id: str,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
    reason_codes: tuple[str, ...],
) -> RollbackManagerReadinessReadModel:
    return RollbackManagerReadinessReadModel(
        read_model_id=f"rollback_manager_readiness:{package_id}",
        contract_id=ROLLBACK_MANAGER_CONTRACT_ID,
        package_id=package_id,
        status=RollbackReadinessStatus.BLOCKED,
        rollback_plan_reference=None,
        snapshot_readiness=snapshot_readiness,
        rollback_ready=False,
        reason_codes=reason_codes,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_sha256(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
    int(value, 16)


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
