from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CanonicalPanelId = Literal[
    "panel_queue_load",
    "panel_node_topology",
    "panel_degraded_mode",
    "panel_project_map",
    "panel_data_flow",
    "panel_dependency_map",
    "panel_version_control_dashboard",
]


@dataclass(frozen=True, slots=True)
class CanonicalPanelIdentity:
    """Canonical dashboard panel identity entry."""

    panel_id: CanonicalPanelId
    panel_name: str


@dataclass(frozen=True, slots=True)
class CanonicalPanelIdentityContract:
    """Unified canonical dashboard panel identity contract."""

    total_panels: int
    panels: tuple[CanonicalPanelIdentity, ...]
