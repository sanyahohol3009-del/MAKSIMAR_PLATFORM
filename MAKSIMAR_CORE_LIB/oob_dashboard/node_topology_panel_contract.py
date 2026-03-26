from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_node_role_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_models import (
    NodeTopologyPanelContract,
    NodeTopologyPanelEntry,
)


def build_node_topology_panel_contract() -> NodeTopologyPanelContract:
    """Build unified read-only node topology panel contract."""
    node_contract = build_node_role_contract()

    entries = tuple(
        NodeTopologyPanelEntry(
            node_id=node.node_id,
            role_type=node.role_type,
            heavy_execution_allowed=node.heavy_execution_allowed,
            security_root=node.security_root,
        )
        for node in node_contract.nodes
    )

    return NodeTopologyPanelContract(
        panel_id="panel_node_topology",
        total_entries=len(entries),
        entries=entries,
    )
