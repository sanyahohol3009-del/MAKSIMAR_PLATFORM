from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DegradedModePanelEntry:
    """Canonical read-only degraded mode panel entry."""

    disabled_feature: str
    safety_critical: bool
    remains_active: bool


@dataclass(frozen=True, slots=True)
class DegradedModePanelContract:
    """Unified read-only degraded mode panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[DegradedModePanelEntry, ...]
