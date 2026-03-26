from __future__ import annotations

from MAKSIMAR_CORE_LIB.version_control.panel_models import (
    VersionPanelContract,
    VersionPanelEntry,
)
from MAKSIMAR_CORE_LIB.version_control.sync_contract import (
    build_sync_state_contract,
)


def build_version_panel_contract() -> VersionPanelContract:
    """Build unified read-only version panel contract."""
    sync_contract = build_sync_state_contract()

    entries = tuple(
        VersionPanelEntry(
            repo_id=repo.repo_id,
            branch_name=repo.branch_name,
            sync_state=repo.sync_state,
            snapshot_available=True,
        )
        for repo in sync_contract.repos
    )

    return VersionPanelContract(
        panel_id="panel_version_control",
        total_entries=len(entries),
        entries=entries,
    )
