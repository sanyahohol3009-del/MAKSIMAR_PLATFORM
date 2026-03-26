from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.node_role_models import (
    NodeRole,
    NodeRoleContract,
)


def build_node_role_contract() -> NodeRoleContract:
    """Build unified canonical node role contract."""

    nodes = (
        NodeRole(
            node_id="mobile_001",
            role_type="mobile_node",
            core_write_allowed=False,
            heavy_execution_allowed=False,
            security_root=False,
        ),
        NodeRole(
            node_id="dev_001",
            role_type="dev_node",
            core_write_allowed=False,
            heavy_execution_allowed=True,
            security_root=False,
        ),
        NodeRole(
            node_id="home_001",
            role_type="home_node",
            core_write_allowed=False,
            heavy_execution_allowed=True,
            security_root=False,
        ),
    )

    return NodeRoleContract(
        total_nodes=len(nodes),
        nodes=nodes,
    )
