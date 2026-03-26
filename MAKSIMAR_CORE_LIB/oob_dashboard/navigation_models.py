from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PanelType = Literal[
    "consistency",
    "snapshot",
    "incident",
    "diagnostics",
    "chat",
    "settings",
    "gesture_control",
]


@dataclass(frozen=True, slots=True)
class NavigationItem:
    """Single sidebar item."""

    item_id: str
    label: str
    panel_type: PanelType
    enabled: bool


@dataclass(frozen=True, slots=True)
class DisplayPanelPlacement:
    """Placement of a panel on a specific display."""

    panel_id: str
    panel_type: PanelType
    display_id: int
    position: Literal["left", "center", "right", "full"]


@dataclass(frozen=True, slots=True)
class DashboardNavigationContract:
    """Full navigation + layout contract (multi-panel, multi-display ready)."""

    items: tuple[NavigationItem, ...]
    placements: tuple[DisplayPanelPlacement, ...]
    active_panel: PanelType
