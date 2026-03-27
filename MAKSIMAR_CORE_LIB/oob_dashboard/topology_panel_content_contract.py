from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_contract import (
    build_node_topology_panel_contract,
)


TopologyPanelStatus = Literal[
    "topology_visible",
    "no_topology_visible",
]


@dataclass(frozen=True, slots=True)
class TopologyPanelContentEntry:
    """Canonical content entry for the topology panel."""

    panel_id: str
    total_topology_entries: int
    mobile_nodes: int
    home_nodes: int
    operator_visible_entries: int
    topology_panel_status: TopologyPanelStatus
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class TopologyPanelContentContract:
    """Canonical content contract for the topology panel."""

    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: tuple[TopologyPanelContentEntry, ...]


def build_topology_panel_content_contract() -> TopologyPanelContentContract:
    """Build canonical content contract for the topology panel."""
    topology_contract = build_node_topology_panel_contract()

    entries = (
        TopologyPanelContentEntry(
            panel_id="panel_topology_001",
            total_topology_entries=len(topology_contract.entries),
            mobile_nodes=sum(
                1
                for entry in topology_contract.entries
                if entry.role_type == "mobile_node"
            ),
            home_nodes=sum(
                1
                for entry in topology_contract.entries
                if entry.role_type == "home_node"
            ),
            operator_visible_entries=sum(
                1 for entry in topology_contract.entries
            ),
            topology_panel_status=(
                "topology_visible"
                if len(topology_contract.entries) > 0
                else "no_topology_visible"
            ),
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            read_only=True,
            description=(
                "Canonical topology panel content contract built from "
                "node topology panel contract."
            ),
        ),
    )

    return TopologyPanelContentContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for entry in entries if entry.visible_in_oob_dashboard
        ),
        entries=entries,
    )
