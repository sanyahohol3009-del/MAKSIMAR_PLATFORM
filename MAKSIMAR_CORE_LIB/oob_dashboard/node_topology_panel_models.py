from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NodeTopologyPanelEntry:
    """Canonical read-only node topology panel entry."""

    node_id: str
    role_type: str
    heavy_execution_allowed: bool
    security_root: bool


@dataclass(frozen=True, slots=True)
class NodeTopologyPanelContract:
    """Unified read-only node topology panel contract."""

    panel_id: str
    total_entries: int
    entries: tuple[NodeTopologyPanelEntry, ...]
