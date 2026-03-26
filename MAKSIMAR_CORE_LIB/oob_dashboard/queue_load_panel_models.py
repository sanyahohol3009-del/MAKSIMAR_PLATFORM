from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QueueLoadPanelEntry:
    """Canonical read-only queue/load panel entry."""

    metric_name: str
    metric_value: int
    metric_unit: str


@dataclass(frozen=True, slots=True)
class QueueLoadPanelContract:
    """Unified read-only queue/load panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[QueueLoadPanelEntry, ...]
