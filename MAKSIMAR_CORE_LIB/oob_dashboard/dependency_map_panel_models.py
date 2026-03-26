from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyMapPanelEntry:
    """Canonical read-only dependency map panel entry."""

    upstream_module_id: str
    downstream_module_id: str
    critical_path: bool


@dataclass(frozen=True, slots=True)
class DependencyMapPanelContract:
    """Unified read-only dependency map panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[DependencyMapPanelEntry, ...]
