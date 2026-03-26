from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


WorkspaceZone = Literal[
    "sidebar",
    "main",
    "secondary",
    "chat",
    "settings",
    "gesture",
]


@dataclass(frozen=True, slots=True)
class DisplayWorkspace:
    """One physical display workspace."""

    display_id: int
    enabled: bool
    zone_count: int


@dataclass(frozen=True, slots=True)
class WorkspacePlacement:
    """One panel placement inside workspace layout."""

    display_id: int
    zone: WorkspaceZone
    panel_id: str


@dataclass(frozen=True, slots=True)
class DashboardWorkspaceContract:
    """Unified multi-display workspace contract."""

    displays: tuple[DisplayWorkspace, ...]
    placements: tuple[WorkspacePlacement, ...]
