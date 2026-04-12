from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class NodeTopologyPanelEntry:
    """Canonical node topology panel entry."""

    node_id: str
    role_type: str
    core_write_allowed: bool
    heavy_execution_allowed: bool
    security_root: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class NodeTopologyPanelContract:
    """Canonical node topology panel contract."""

    panel_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: Tuple[NodeTopologyPanelEntry, ...]
    operator_visible: bool
    description: str


def build_node_topology_panel_contract() -> NodeTopologyPanelContract:
    """Build canonical node topology panel contract."""
    entries = (
        NodeTopologyPanelEntry(
            node_id="mobile_001",
            role_type="mobile_node",
            core_write_allowed=False,
            heavy_execution_allowed=False,
            security_root=False,
            operator_visible=True,
            description="Canonical mobile node.",
        ),
        NodeTopologyPanelEntry(
            node_id="dev_001",
            role_type="dev_node",
            core_write_allowed=False,
            heavy_execution_allowed=True,
            security_root=True,
            operator_visible=True,
            description="Canonical development/control node.",
        ),
        NodeTopologyPanelEntry(
            node_id="home_001",
            role_type="home_node",
            core_write_allowed=False,
            heavy_execution_allowed=True,
            security_root=False,
            operator_visible=True,
            description="Canonical home node.",
        ),
    )

    return NodeTopologyPanelContract(
        panel_id="panel_node_topology",
        total_entries=len(entries),
        read_only_entries=len(entries),
        main_dashboard_visible_entries=len(entries),
        oob_visible_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical node topology panel contract.",
    )
