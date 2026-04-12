from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class TopologyPanelContentEntry:
    """Canonical backward-compatible topology panel content entry."""

    panel_id: str
    workspace_id: str
    total_topology_entries: int
    mobile_nodes: int
    home_nodes: int
    operator_visible_entries: int
    topology_panel_status: str
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    topology_state: str
    read_only: bool
    main_dashboard_visible: bool
    oob_visible: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class TopologyPanelContentContract:
    """Canonical backward-compatible topology panel content contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: Tuple[TopologyPanelContentEntry, ...]
    operator_visible: bool
    description: str


def build_topology_panel_content_contract() -> TopologyPanelContentContract:
    """Build canonical backward-compatible topology panel content contract."""
    entries = (
        TopologyPanelContentEntry(
            panel_id="panel_topology_001",
            workspace_id="workspace_expansion_observability",
            total_topology_entries=3,
            mobile_nodes=1,
            home_nodes=1,
            operator_visible_entries=3,
            topology_panel_status="topology_visible",
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            topology_state="topology_content_stubbed_from_panel_content_spine",
            read_only=True,
            main_dashboard_visible=True,
            oob_visible=True,
            operator_visible=True,
            description=(
                "Canonical topology panel content entry derived from the "
                "surviving panel-content spine."
            ),
        ),
    )

    return TopologyPanelContentContract(
        contract_id="topology_panel_content_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.main_dashboard_visible
        ),
        oob_visible_entries=sum(1 for entry in entries if entry.oob_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical backward-compatible topology panel content contract.",
    )
