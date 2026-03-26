from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PanelCategory = Literal[
    "core",
    "diagnostics",
    "interaction",
    "settings",
    "control",
]


@dataclass(frozen=True, slots=True)
class RegisteredPanel:
    """One dashboard panel registered in sidebar/panel registry."""

    panel_id: str
    label: str
    category: PanelCategory
    visible_in_sidebar: bool


@dataclass(frozen=True, slots=True)
class DashboardPanelRegistryContract:
    """Unified registry of dashboard panels."""

    total_panels: int
    panels: tuple[RegisteredPanel, ...]
