from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectMapPanelEntry:
    """Canonical read-only project map panel entry."""

    module_id: str
    layer_name: str
    criticality: str
    read_only_view_available: bool


@dataclass(frozen=True, slots=True)
class ProjectMapPanelContract:
    """Unified read-only project map panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[ProjectMapPanelEntry, ...]
