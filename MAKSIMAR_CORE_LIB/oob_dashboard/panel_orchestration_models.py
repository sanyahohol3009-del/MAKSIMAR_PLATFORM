from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrchestratedPanel:
    """One panel registered in dashboard orchestration."""

    panel_id: str
    active: bool
    display_id: int
    zone: str


@dataclass(frozen=True, slots=True)
class DashboardPanelOrchestrationContract:
    """Unified orchestration contract for dashboard panels."""

    panels: tuple[OrchestratedPanel, ...]
    active_panel_id: str
    navigation_enabled: bool
    input_routing_enabled: bool
