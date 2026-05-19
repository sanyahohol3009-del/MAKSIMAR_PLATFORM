from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.update_recovery.update_recovery_read_model import (
    UpdateRecoveryReadinessReadModel,
    build_update_recovery_readiness_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.runtime_recovery_manager_adapter import (
    RuntimeRecoveryManagerAdapterReadModel,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.secure_sync_update_transport_adapter import (
    SecureSyncUpdateTransportAdapterReadModel,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.offline_import_gate import OfflineImportGateRuntimeResult
from MAKSIMAR_SERVER.UPDATE_RECOVERY.recovery_service import RecoveryServiceRuntimeResult
from MAKSIMAR_SERVER.UPDATE_RECOVERY.rollback_manager import RollbackManagerRuntimeResult
from MAKSIMAR_SERVER.UPDATE_RECOVERY.snapshot_manager import SnapshotManagerRuntimeResult


UPDATE_RECOVERY_RUNTIME_READ_MODEL_ID = "update_recovery_runtime_read_model_v1"


@dataclass(frozen=True, slots=True)
class UpdateRecoveryRuntimeReadModel:
    read_model_id: str
    package_id: str
    readiness: UpdateRecoveryReadinessReadModel
    secure_sync_transport_adapter: SecureSyncUpdateTransportAdapterReadModel
    runtime_recovery_manager_adapter: RuntimeRecoveryManagerAdapterReadModel
    snapshot_runtime: SnapshotManagerRuntimeResult
    rollback_runtime: RollbackManagerRuntimeResult
    recovery_runtime: RecoveryServiceRuntimeResult
    offline_import_runtime: OfflineImportGateRuntimeResult
    runtime_wrapper_only: bool
    existing_transport_preserved: bool
    existing_recovery_manager_preserved: bool
    runtime_apply_allowed: bool
    canonical_write_allowed: bool
    dashboard_execution_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.read_model_id != UPDATE_RECOVERY_RUNTIME_READ_MODEL_ID:
            raise ValueError("read_model_id must be update_recovery_runtime_read_model_v1")
        _validate_non_empty("package_id", self.package_id)
        if not isinstance(self.readiness, UpdateRecoveryReadinessReadModel):
            raise TypeError("readiness must be UpdateRecoveryReadinessReadModel")
        if not isinstance(self.secure_sync_transport_adapter, SecureSyncUpdateTransportAdapterReadModel):
            raise TypeError("secure_sync_transport_adapter must be SecureSyncUpdateTransportAdapterReadModel")
        if not isinstance(self.runtime_recovery_manager_adapter, RuntimeRecoveryManagerAdapterReadModel):
            raise TypeError("runtime_recovery_manager_adapter must be RuntimeRecoveryManagerAdapterReadModel")
        if not isinstance(self.snapshot_runtime, SnapshotManagerRuntimeResult):
            raise TypeError("snapshot_runtime must be SnapshotManagerRuntimeResult")
        if not isinstance(self.rollback_runtime, RollbackManagerRuntimeResult):
            raise TypeError("rollback_runtime must be RollbackManagerRuntimeResult")
        if not isinstance(self.recovery_runtime, RecoveryServiceRuntimeResult):
            raise TypeError("recovery_runtime must be RecoveryServiceRuntimeResult")
        if not isinstance(self.offline_import_runtime, OfflineImportGateRuntimeResult):
            raise TypeError("offline_import_runtime must be OfflineImportGateRuntimeResult")
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
            "package_id": self.package_id,
            "readiness": self.readiness.to_dict(),
            "secure_sync_transport_adapter": self.secure_sync_transport_adapter.to_dict(),
            "runtime_recovery_manager_adapter": self.runtime_recovery_manager_adapter.to_dict(),
            "snapshot_runtime": self.snapshot_runtime.to_dict(),
            "rollback_runtime": self.rollback_runtime.to_dict(),
            "recovery_runtime": self.recovery_runtime.to_dict(),
            "offline_import_runtime": self.offline_import_runtime.to_dict(),
            "runtime_wrapper_only": self.runtime_wrapper_only,
            "existing_transport_preserved": self.existing_transport_preserved,
            "existing_recovery_manager_preserved": self.existing_recovery_manager_preserved,
            "runtime_apply_allowed": self.runtime_apply_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_update_recovery_runtime_read_model(
    *,
    package_id: str,
    secure_sync_transport_adapter: SecureSyncUpdateTransportAdapterReadModel,
    runtime_recovery_manager_adapter: RuntimeRecoveryManagerAdapterReadModel,
    snapshot_runtime: SnapshotManagerRuntimeResult,
    rollback_runtime: RollbackManagerRuntimeResult,
    recovery_runtime: RecoveryServiceRuntimeResult,
    offline_import_runtime: OfflineImportGateRuntimeResult,
) -> UpdateRecoveryRuntimeReadModel:
    readiness = build_update_recovery_readiness_read_model(
        package_id=package_id,
        snapshot_readiness=snapshot_runtime.read_model,
        rollback_readiness=rollback_runtime.read_model,
        recovery_readiness=recovery_runtime.read_model,
        offline_import_decision=offline_import_runtime.decision,
        secure_sync_facade=secure_sync_transport_adapter.facade_read_model,
    )

    return UpdateRecoveryRuntimeReadModel(
        read_model_id=UPDATE_RECOVERY_RUNTIME_READ_MODEL_ID,
        package_id=package_id,
        readiness=readiness,
        secure_sync_transport_adapter=secure_sync_transport_adapter,
        runtime_recovery_manager_adapter=runtime_recovery_manager_adapter,
        snapshot_runtime=snapshot_runtime,
        rollback_runtime=rollback_runtime,
        recovery_runtime=recovery_runtime,
        offline_import_runtime=offline_import_runtime,
        runtime_wrapper_only=True,
        existing_transport_preserved=not secure_sync_transport_adapter.replaces_existing_transport,
        existing_recovery_manager_preserved=runtime_recovery_manager_adapter.recovery_manager_preserved,
        runtime_apply_allowed=False,
        canonical_write_allowed=False,
        dashboard_execution_allowed=False,
        dashboard_safe=True,
        reason_codes=(
            "update_recovery_runtime_read_model_built",
            "runtime_wrapper_only",
            "existing_transport_preserved",
            "existing_recovery_manager_preserved",
        ),
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
