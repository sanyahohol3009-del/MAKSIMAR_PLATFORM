from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ComposedViewPanel:
    """One panel inside final dashboard composition."""

    panel_id: str
    display_id: int
    zone: str
    visible: bool
    active: bool


@dataclass(frozen=True, slots=True)
class DashboardViewCompositionContract:
    """Unified dashboard view composition contract."""

    total_panels: int
    composed_panels: tuple[ComposedViewPanel, ...]
    active_panel_id: str
