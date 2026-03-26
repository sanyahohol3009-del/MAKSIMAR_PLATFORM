from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VersionControlPanelEntry:
    """Canonical read-only version control panel entry."""

    repo_id: str
    branch_name: str
    sync_state: str
    snapshot_available: bool


@dataclass(frozen=True, slots=True)
class VersionControlPanelContract:
    """Unified read-only version control panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[VersionControlPanelEntry, ...]
