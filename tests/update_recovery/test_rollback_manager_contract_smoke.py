from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.rollback_manager_contract import (
    RollbackPlanReference,
    RollbackReadinessStatus,
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


def _rollback_plan(target_snapshot_id: str = "snapshot-001") -> RollbackPlanReference:
    return RollbackPlanReference(
        rollback_plan_id="rollback-plan-001",
        rollback_uri="rollback://update-package-001/rollback-plan-001",
        rollback_sha256=TWO,
        target_snapshot_id=target_snapshot_id,
        tested=True,
        reversible=True,
    )


def test_rollback_manager_ready_requires_snapshot_readiness() -> None:
    read_model = build_rollback_ready_read_model(
        package_id="update-package-001",
        rollback_plan_reference=_rollback_plan(),
        snapshot_readiness=_snapshot_ready(),
    )

    assert read_model.status is RollbackReadinessStatus.READY
    assert read_model.rollback_ready is True
    assert read_model.snapshot_readiness.snapshot_ready is True
    assert read_model.direct_apply_allowed is False


def test_rollback_manager_blocks_when_snapshot_blocked() -> None:
    snapshot_blocked = build_snapshot_blocked_read_model(
        package_id="update-package-001",
        reason_codes=("snapshot_missing",),
    )
    read_model = build_rollback_blocked_read_model(
        package_id="update-package-001",
        snapshot_readiness=snapshot_blocked,
        reason_codes=("rollback_blocked_without_snapshot",),
    )

    assert read_model.status is RollbackReadinessStatus.BLOCKED
    assert read_model.rollback_ready is False


def test_rollback_manager_rejects_plan_targeting_wrong_snapshot() -> None:
    with pytest.raises(ValueError, match="target the ready snapshot"):
        build_rollback_ready_read_model(
            package_id="update-package-001",
            rollback_plan_reference=_rollback_plan(target_snapshot_id="wrong-snapshot"),
            snapshot_readiness=_snapshot_ready(),
        )
