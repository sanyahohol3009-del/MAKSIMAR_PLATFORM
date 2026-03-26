from __future__ import annotations

from MAKSIMAR_CORE_LIB.version_control import (
    SnapshotRequest,
    SnapshotRequestContract,
)


def test_snapshot_models_build() -> None:
    """Snapshot request models should build successfully."""
    contract = SnapshotRequestContract(
        total_requests=2,
        requests=(
            SnapshotRequest(
                snapshot_id="snapshot_001",
                snapshot_type="manual_snapshot",
                approval_required=True,
                core_write_allowed=False,
            ),
            SnapshotRequest(
                snapshot_id="snapshot_002",
                snapshot_type="conversation_snapshot",
                approval_required=True,
                core_write_allowed=False,
            ),
        ),
    )

    assert contract.total_requests == 2
    assert len(contract.requests) == 2
    assert contract.requests[0].snapshot_type == "manual_snapshot"
    assert contract.requests[-1].snapshot_type == "conversation_snapshot"
    assert contract.requests[0].approval_required is True
    assert contract.requests[0].core_write_allowed is False
