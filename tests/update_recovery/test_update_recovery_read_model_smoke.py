from __future__ import annotations

from MAKSIMAR_CORE_LIB.update_recovery.offline_import_gate_contract import (
    OfflineImportCandidate,
    evaluate_offline_import_gate,
)
from MAKSIMAR_CORE_LIB.update_recovery.recovery_service_contract import (
    build_recovery_service_blocked_read_model,
    build_recovery_service_ready_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import (
    RollbackPlanReference,
    build_rollback_blocked_read_model,
    build_rollback_ready_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.secure_sync_update_facade_contract import (
    build_secure_sync_update_facade_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotReference,
    build_snapshot_blocked_read_model,
    build_snapshot_ready_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.update_recovery_read_model import (
    UpdateRecoveryReadinessStatus,
    build_update_recovery_readiness_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


def _offline_import_decision(signature_present: bool = True):
    return evaluate_offline_import_gate(
        OfflineImportCandidate(
            import_id="offline-import-001",
            package_id="update-package-001",
            source_uri="offline-media://usb-001/update-package-001",
            package_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            signature_present=signature_present,
            air_gap_transfer_confirmed=True,
            media_quarantined=True,
            operator_approval_present=True,
        )
    )


def _snapshot_ready():
    return build_snapshot_ready_read_model(
        package_id="update-package-001",
        snapshot_reference=SnapshotReference(
            snapshot_id="snapshot-001",
            snapshot_uri="snapshot://update-package-001/snapshot-001",
            snapshot_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            immutable=True,
            state_manifest_present=True,
            rollback_compatible=True,
        ),
    )


def _rollback_ready(snapshot_readiness):
    return build_rollback_ready_read_model(
        package_id="update-package-001",
        rollback_plan_reference=RollbackPlanReference(
            rollback_plan_id="rollback-plan-001",
            rollback_uri="rollback://update-package-001/rollback-plan-001",
            rollback_sha256=TWO,
            target_snapshot_id="snapshot-001",
            tested=True,
            reversible=True,
        ),
        snapshot_readiness=snapshot_readiness,
    )


def test_update_recovery_readiness_requires_all_gates_for_next_gate() -> None:
    snapshot_readiness = _snapshot_ready()
    rollback_readiness = _rollback_ready(snapshot_readiness)
    recovery_readiness = build_recovery_service_ready_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
    )

    read_model = build_update_recovery_readiness_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
        recovery_readiness=recovery_readiness,
        offline_import_decision=_offline_import_decision(),
        secure_sync_facade=build_secure_sync_update_facade_read_model(),
    )

    assert read_model.status is UpdateRecoveryReadinessStatus.READY_FOR_NEXT_GATE
    assert read_model.update_recovery_ready_for_next_gate is True
    assert read_model.update_apply_allowed is False
    assert read_model.direct_apply_allowed is False
    assert read_model.dashboard_execution_allowed is False


def test_update_recovery_readiness_blocks_without_snapshot() -> None:
    snapshot_blocked = build_snapshot_blocked_read_model(
        package_id="update-package-001",
        reason_codes=("snapshot_missing",),
    )
    rollback_blocked = build_rollback_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        reason_codes=("rollback_blocked_without_snapshot",),
    )
    recovery_blocked = build_recovery_service_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        rollback_readiness=rollback_blocked,
        reason_codes=("recovery_blocked_without_snapshot_and_rollback",),
    )

    read_model = build_update_recovery_readiness_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        rollback_readiness=rollback_blocked,
        recovery_readiness=recovery_blocked,
        offline_import_decision=_offline_import_decision(),
        secure_sync_facade=build_secure_sync_update_facade_read_model(),
    )

    assert read_model.status is UpdateRecoveryReadinessStatus.BLOCKED
    assert read_model.update_recovery_ready_for_next_gate is False
    assert "snapshot_not_ready" in read_model.reason_codes
    assert "rollback_not_ready" in read_model.reason_codes
    assert "recovery_not_ready" in read_model.reason_codes
