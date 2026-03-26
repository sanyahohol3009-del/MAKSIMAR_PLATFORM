from __future__ import annotations

from MAKSIMAR_CORE_LIB.version_control.sync_models import (
    SyncState,
    SyncStateContract,
)


def build_sync_state_contract() -> SyncStateContract:
    """Build unified sync state contract."""

    repos = (
        SyncState(
            repo_id="maksimar_platform",
            branch_name="main",
            sync_state="pending_changes",
            approval_required_for_push=True,
        ),
        SyncState(
            repo_id="maksimar_mobile",
            branch_name="main",
            sync_state="clean",
            approval_required_for_push=True,
        ),
    )

    return SyncStateContract(
        total_repos=len(repos),
        repos=repos,
    )
