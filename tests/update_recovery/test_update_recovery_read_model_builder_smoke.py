from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import OfflineImportCandidate
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import RollbackPlanReference
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import SnapshotReference
from MAKSIMAR_CORE_LIB.update_recovery.update_recovery_read_model import UpdateRecoveryReadinessStatus
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.runtime_recovery_manager_adapter import (
    build_runtime_recovery_manager_adapter_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.adapters.secure_sync_update_transport_adapter import (
    build_secure_sync_update_transport_adapter_read_model,
)
from MAKSIMAR_SERVER.UPDATE_RECOVERY.offline_import_gate import run_offline_import_gate
from MAKSIMAR_SERVER.UPDATE_RECOVERY.recovery_service import run_recovery_service_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.rollback_manager import run_rollback_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.snapshot_manager import run_snapshot_manager_ready
from MAKSIMAR_SERVER.UPDATE_RECOVERY.update_recovery_read_model_builder import (
    UPDATE_RECOVERY_RUNTIME_READ_MODEL_ID,
    build_update_recovery_runtime_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


def _runtime_read_model():
    package_id = "update-package-runtime-builder-001"
    snapshot_runtime = run_snapshot_manager_ready(
        package_id=package_id,
        snapshot_reference=SnapshotReference(
            snapshot_id="snapshot-builder-001",
            snapshot_uri="snapshot://builder/snapshot-builder-001",
            snapshot_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            immutable=True,
            state_manifest_present=True,
            rollback_compatible=True,
        ),
    )
    rollback_runtime = run_rollback_manager_ready(
        package_id=package_id,
        rollback_plan_reference=RollbackPlanReference(
            rollback_plan_id="rollback-builder-001",
            rollback_uri="rollback://builder/rollback-builder-001",
            rollback_sha256=TWO,
            target_snapshot_id="snapshot-builder-001",
            tested=True,
            reversible=True,
        ),
        snapshot_readiness=snapshot_runtime.read_model,
    )
    recovery_runtime = run_recovery_service_ready(
        package_id=package_id,
        snapshot_readiness=snapshot_runtime.read_model,
        rollback_readiness=rollback_runtime.read_model,
    )
    offline_runtime = run_offline_import_gate(
        OfflineImportCandidate(
            import_id="offline-builder-001",
            package_id=package_id,
            source_uri="offline-media://builder/update-package-runtime-builder-001",
            package_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            signature_present=True,
            air_gap_transfer_confirmed=True,
            media_quarantined=True,
            operator_approval_present=True,
        )
    )

    return build_update_recovery_runtime_read_model(
        package_id=package_id,
        secure_sync_transport_adapter=build_secure_sync_update_transport_adapter_read_model(project_root=Path.cwd()),
        runtime_recovery_manager_adapter=build_runtime_recovery_manager_adapter_read_model(project_root=Path.cwd()),
        snapshot_runtime=snapshot_runtime,
        rollback_runtime=rollback_runtime,
        recovery_runtime=recovery_runtime,
        offline_import_runtime=offline_runtime,
    )


def test_update_recovery_runtime_read_model_is_dashboard_safe_and_read_only() -> None:
    read_model = _runtime_read_model()

    assert read_model.read_model_id == UPDATE_RECOVERY_RUNTIME_READ_MODEL_ID
    assert read_model.runtime_wrapper_only is True
    assert read_model.existing_transport_preserved is True
    assert read_model.existing_recovery_manager_preserved is True
    assert read_model.runtime_apply_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.readiness.status is UpdateRecoveryReadinessStatus.READY_FOR_NEXT_GATE
    assert read_model.readiness.update_apply_allowed is False
