from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VersionPanelEntry:
    """Canonical read-only version panel entry."""

    repo_id: str
    branch_name: str
    sync_state: str
    snapshot_available: bool


@dataclass(frozen=True, slots=True)
class VersionPanelContract:
    """Unified read-only version panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[VersionPanelEntry, ...]
