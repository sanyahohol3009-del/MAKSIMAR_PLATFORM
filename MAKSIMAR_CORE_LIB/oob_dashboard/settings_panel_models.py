from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SettingsCategory = Literal[
    "system",
    "display",
    "input",
    "security",
    "advanced",
]


@dataclass(frozen=True, slots=True)
class SettingsEntry:
    """One settings entry in dashboard."""

    key: str
    category: SettingsCategory
    editable: bool


@dataclass(frozen=True, slots=True)
class DashboardSettingsPanel:
    """Read-only settings panel contract."""

    panel_id: str
    entries: tuple[SettingsEntry, ...]
