from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.update_recovery.snapshot_manager_contract import (
    SnapshotReadinessStatus,
    SnapshotReference,
    build_snapshot_blocked_read_model,
    build_snapshot_ready_read_model,
)

ONE = "1" * 64


def _snapshot() -> SnapshotReference:
    return SnapshotReference(
        snapshot_id="snapshot-001",
        snapshot_uri="snapshot://update-package-001/snapshot-001",
        snapshot_sha256=ONE,
        created_at_utc="2026-01-01T00:00:00Z",
        immutable=True,
        state_manifest_present=True,
        rollback_compatible=True,
    )


def test_snapshot_manager_ready_read_model_is_dashboard_safe() -> None:
    read_model = build_snapshot_ready_read_model(
        package_id="update-package-001",
        snapshot_reference=_snapshot(),
    )

    assert read_model.status is SnapshotReadinessStatus.READY
    assert read_model.snapshot_ready is True
    assert read_model.dashboard_safe is True
    assert read_model.direct_apply_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False


def test_snapshot_manager_blocked_read_model_blocks_update() -> None:
    read_model = build_snapshot_blocked_read_model(
        package_id="update-package-001",
        reason_codes=("snapshot_missing",),
    )

    assert read_model.status is SnapshotReadinessStatus.BLOCKED
    assert read_model.snapshot_ready is False
    assert read_model.snapshot_reference is None


def test_snapshot_reference_rejects_mutable_snapshot() -> None:
    with pytest.raises(ValueError, match="immutable"):
        SnapshotReference(
            snapshot_id="snapshot-001",
            snapshot_uri="snapshot://update-package-001/snapshot-001",
            snapshot_sha256=ONE,
            created_at_utc="2026-01-01T00:00:00Z",
            immutable=False,
            state_manifest_present=True,
            rollback_compatible=True,
        )
