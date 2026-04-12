from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_contract import (
    build_dashboard_workspace_contract,
)


@dataclass(frozen=True)
class PanelOrchestrationEntry:
    """Canonical backward-compatible panel orchestration entry."""

    panel_id: str
    workspace_id: str
    display_id: int
    display_target_id: str
    is_active: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class PanelOrchestrationContract:
    """Canonical backward-compatible panel orchestration contract."""

    contract_id: str
    panels: Tuple[PanelOrchestrationEntry, ...]
    active_panel_id: str
    navigation_enabled: bool
    input_routing_enabled: bool
    operator_visible: bool
    description: str


def build_dashboard_panel_orchestration_contract() -> PanelOrchestrationContract:
    """Build canonical backward-compatible panel orchestration contract."""
    workspace_contract = build_dashboard_workspace_contract()

    entries = tuple(
        PanelOrchestrationEntry(
            panel_id=placement.panel_id,
            workspace_id=placement.workspace_id,
            display_id=placement.display_id,
            display_target_id=placement.display_target_id,
            is_active=(placement.panel_id == "panel_chat"),
            operator_visible=True,
            description=(
                f"Canonical orchestration entry for {placement.panel_id} "
                f"in {placement.workspace_id}."
            ),
        )
        for placement in workspace_contract.placements
    )

    return PanelOrchestrationContract(
        contract_id="panel_orchestration_contract_001",
        panels=entries,
        active_panel_id="panel_chat",
        navigation_enabled=True,
        input_routing_enabled=True,
        operator_visible=True,
        description="Canonical backward-compatible panel orchestration contract.",
    )


def build_panel_orchestration_contract() -> PanelOrchestrationContract:
    """Backward-compatible alias."""
    return build_dashboard_panel_orchestration_contract()
