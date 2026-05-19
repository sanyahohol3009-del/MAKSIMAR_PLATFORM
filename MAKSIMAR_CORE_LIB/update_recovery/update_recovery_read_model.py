from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import (
    OfflineImportGateDecisionReadModel,
)
from MAKSIMAR_CORE_LIB.update_recovery.recovery_service_contract import (
    RecoveryServiceReadinessReadModel,
)
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import (
    RollbackManagerReadinessReadModel,
)
from MAKSIMAR_CORE_LIB.update_recovery.secure_sync_update_facade_contract import (
    SecureSyncUpdateFacadeReadModel,
)
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotManagerReadinessReadModel,
)


UPDATE_RECOVERY_READINESS_READ_MODEL_ID = "update_recovery_readiness_read_model_v1"


class UpdateRecoveryReadinessStatus(str, Enum):
    READY_FOR_NEXT_GATE = "ready_for_next_gate"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class UpdateRecoveryReadinessReadModel:
    read_model_id: str
    package_id: str
    status: UpdateRecoveryReadinessStatus
    snapshot_readiness: SnapshotManagerReadinessReadModel
    rollback_readiness: RollbackManagerReadinessReadModel
    recovery_readiness: RecoveryServiceReadinessReadModel
    offline_import_decision: OfflineImportGateDecisionReadModel
    secure_sync_facade: SecureSyncUpdateFacadeReadModel
    update_recovery_ready_for_next_gate: bool
    update_apply_allowed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    direct_apply_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if self.read_model_id != UPDATE_RECOVERY_READINESS_READ_MODEL_ID:
            raise ValueError("read_model_id must be update_recovery_readiness_read_model_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.status, UpdateRecoveryReadinessStatus):
            raise TypeError("status must be UpdateRecoveryReadinessStatus")
        if not isinstance(self.snapshot_readiness, SnapshotManagerReadinessReadModel):
            raise TypeError("snapshot_readiness must be SnapshotManagerReadinessReadModel")
        if not isinstance(self.rollback_readiness, RollbackManagerReadinessReadModel):
            raise TypeError("rollback_readiness must be RollbackManagerReadinessReadModel")
        if not isinstance(self.recovery_readiness, RecoveryServiceReadinessReadModel):
            raise TypeError("recovery_readiness must be RecoveryServiceReadinessReadModel")
        if not isinstance(self.offline_import_decision, OfflineImportGateDecisionReadModel):
            raise TypeError("offline_import_decision must be OfflineImportGateDecisionReadModel")
        if not isinstance(self.secure_sync_facade, SecureSyncUpdateFacadeReadModel):
            raise TypeError("secure_sync_facade must be SecureSyncUpdateFacadeReadModel")

        if self.status is UpdateRecoveryReadinessStatus.READY_FOR_NEXT_GATE:
            if not self.update_recovery_ready_for_next_gate:
                raise ValueError("READY_FOR_NEXT_GATE requires update_recovery_ready_for_next_gate true")
            if not self.snapshot_readiness.snapshot_ready:
                raise ValueError("READY_FOR_NEXT_GATE requires snapshot readiness")
            if not self.rollback_readiness.rollback_ready:
                raise ValueError("READY_FOR_NEXT_GATE requires rollback readiness")
            if not self.recovery_readiness.recovery_ready:
                raise ValueError("READY_FOR_NEXT_GATE requires recovery readiness")
            if not self.offline_import_decision.offline_import_allowed_for_verification:
                raise ValueError("READY_FOR_NEXT_GATE requires offline import verification gate")
            if not self.secure_sync_facade.existing_transport_bound:
                raise ValueError("READY_FOR_NEXT_GATE requires secure sync facade binding")

        if self.status is UpdateRecoveryReadinessStatus.BLOCKED and self.update_recovery_ready_for_next_gate:
            raise ValueError("BLOCKED update recovery readiness cannot be ready for next gate")
        if self.update_apply_allowed:
            raise ValueError("update_apply_allowed must remain false in BATCH 3.3")

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
            "package_id": self.package_id,
            "status": self.status.value,
            "snapshot_readiness": self.snapshot_readiness.to_dict(),
            "rollback_readiness": self.rollback_readiness.to_dict(),
            "recovery_readiness": self.recovery_readiness.to_dict(),
            "offline_import_decision": self.offline_import_decision.to_dict(),
            "secure_sync_facade": self.secure_sync_facade.to_dict(),
            "update_recovery_ready_for_next_gate": self.update_recovery_ready_for_next_gate,
            "update_apply_allowed": self.update_apply_allowed,
            "reason_codes": self.reason_codes,
            "dashboard_safe": self.dashboard_safe,
            "direct_apply_allowed": self.direct_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_update_recovery_readiness_read_model(
    *,
    package_id: str,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
    rollback_readiness: RollbackManagerReadinessReadModel,
    recovery_readiness: RecoveryServiceReadinessReadModel,
    offline_import_decision: OfflineImportGateDecisionReadModel,
    secure_sync_facade: SecureSyncUpdateFacadeReadModel,
) -> UpdateRecoveryReadinessReadModel:
    ready = (
        snapshot_readiness.snapshot_ready
        and rollback_readiness.rollback_ready
        and recovery_readiness.recovery_ready
        and offline_import_decision.offline_import_allowed_for_verification
        and secure_sync_facade.existing_transport_bound
    )

    if ready:
        status = UpdateRecoveryReadinessStatus.READY_FOR_NEXT_GATE
        reason_codes = (
            "snapshot_ready",
            "rollback_ready",
            "recovery_ready",
            "offline_import_verified_for_next_gate",
            "secure_sync_update_facade_bound",
        )
    else:
        status = UpdateRecoveryReadinessStatus.BLOCKED
        reason_codes = _collect_blocking_reasons(
            snapshot_readiness=snapshot_readiness,
            rollback_readiness=rollback_readiness,
            recovery_readiness=recovery_readiness,
            offline_import_decision=offline_import_decision,
            secure_sync_facade=secure_sync_facade,
        )

    return UpdateRecoveryReadinessReadModel(
        read_model_id=UPDATE_RECOVERY_READINESS_READ_MODEL_ID,
        package_id=package_id,
        status=status,
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
        recovery_readiness=recovery_readiness,
        offline_import_decision=offline_import_decision,
        secure_sync_facade=secure_sync_facade,
        update_recovery_ready_for_next_gate=ready,
        update_apply_allowed=False,
        reason_codes=reason_codes,
    )


def _collect_blocking_reasons(
    *,
    snapshot_readiness: SnapshotManagerReadinessReadModel,
    rollback_readiness: RollbackManagerReadinessReadModel,
    recovery_readiness: RecoveryServiceReadinessReadModel,
    offline_import_decision: OfflineImportGateDecisionReadModel,
    secure_sync_facade: SecureSyncUpdateFacadeReadModel,
) -> tuple[str, ...]:
    reasons: list[str] = ["update_recovery_blocked"]
    if not snapshot_readiness.snapshot_ready:
        reasons.append("snapshot_not_ready")
    if not rollback_readiness.rollback_ready:
        reasons.append("rollback_not_ready")
    if not recovery_readiness.recovery_ready:
        reasons.append("recovery_not_ready")
    if not offline_import_decision.offline_import_allowed_for_verification:
        reasons.append("offline_import_gate_not_ready")
    if not secure_sync_facade.existing_transport_bound:
        reasons.append("secure_sync_update_facade_not_bound")
    return tuple(reasons)


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
