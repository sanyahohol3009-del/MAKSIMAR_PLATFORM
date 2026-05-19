from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.recovery_service_contract import (
    RecoveryServiceReadinessStatus,
    build_recovery_service_blocked_read_model,
    build_recovery_service_ready_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import (
    RollbackPlanReference,
    build_rollback_blocked_read_model,
    build_rollback_ready_read_model,
)
from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotReference,
    build_snapshot_blocked_read_model,
    build_snapshot_ready_read_model,
)

ONE = "1" * 64
TWO = "2" * 64


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


def test_recovery_service_ready_requires_snapshot_and_rollback() -> None:
    snapshot_readiness = _snapshot_ready()
    rollback_readiness = _rollback_ready(snapshot_readiness)

    read_model = build_recovery_service_ready_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_readiness,
        rollback_readiness=rollback_readiness,
    )

    assert read_model.status is RecoveryServiceReadinessStatus.READY
    assert read_model.recovery_ready is True
    assert read_model.recovery_service_bound is True
    assert read_model.direct_apply_allowed is False


def test_recovery_service_blocks_when_dependencies_are_blocked() -> None:
    snapshot_blocked = build_snapshot_blocked_read_model(
        package_id="update-package-001",
        reason_codes=("snapshot_missing",),
    )
    rollback_blocked = build_rollback_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        reason_codes=("rollback_blocked_without_snapshot",),
    )

    read_model = build_recovery_service_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        rollback_readiness=rollback_blocked,
        reason_codes=("recovery_blocked_without_snapshot_and_rollback",),
    )

    assert read_model.status is RecoveryServiceReadinessStatus.BLOCKED
    assert read_model.recovery_ready is False


def test_recovery_service_rejects_ready_state_without_rollback() -> None:
    snapshot_blocked = build_snapshot_blocked_read_model(
        package_id="update-package-001",
        reason_codes=("snapshot_missing",),
    )
    rollback_blocked = build_rollback_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        reason_codes=("rollback_blocked_without_snapshot",),
    )

    with pytest.raises(ValueError, match="snapshot readiness"):
        build_recovery_service_ready_read_model(
            package_id="update-package-001",
            snapshot_readiness=snapshot_blocked,
            rollback_readiness=rollback_blocked,
        )
