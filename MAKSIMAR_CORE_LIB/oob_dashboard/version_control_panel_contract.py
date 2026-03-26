from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.version_control_panel_models import (
    VersionControlPanelContract,
    VersionControlPanelEntry,
)
from MAKSIMAR_CORE_LIB.version_control import (
    build_version_panel_contract,
)


def build_version_control_panel_contract() -> VersionControlPanelContract:
    """Build unified read-only version control panel contract."""
    version_contract = build_version_panel_contract()

    entries = tuple(
        VersionControlPanelEntry(
            repo_id=entry.repo_id,
            branch_name=entry.branch_name,
            sync_state=entry.sync_state,
            snapshot_available=entry.snapshot_available,
        )
        for entry in version_contract.entries
    )

    return VersionControlPanelContract(
        panel_id="panel_version_control_dashboard",
        total_entries=len(entries),
        entries=entries,
    )
