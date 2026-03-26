from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DataFlowPanelEntry:
    """Canonical read-only data flow panel entry."""

    step_order: int
    source_component: str
    target_component: str
    flow_name: str


@dataclass(frozen=True, slots=True)
class DataFlowPanelContract:
    """Unified read-only data flow panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[DataFlowPanelEntry, ...]
