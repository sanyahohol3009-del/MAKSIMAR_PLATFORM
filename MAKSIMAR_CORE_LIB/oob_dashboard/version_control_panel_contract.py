from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class VersionControlPanelEntry:
    """Canonical version control panel entry."""

    sync_state: str
    branch_name: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class VersionControlPanelContract:
    """Canonical version control panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[VersionControlPanelEntry, ...]
    operator_visible: bool
    description: str


def build_version_control_panel_contract() -> VersionControlPanelContract:
    """Build canonical version control panel contract."""
    entries = (
        VersionControlPanelEntry(
            sync_state="pending_changes",
            branch_name="main",
            operator_visible=True,
            description="Canonical pending-changes state.",
        ),
        VersionControlPanelEntry(
            sync_state="clean",
            branch_name="main",
            operator_visible=True,
            description="Canonical clean state.",
        ),
    )

    return VersionControlPanelContract(
        panel_id="panel_version_control_dashboard",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical version control panel contract.",
    )
