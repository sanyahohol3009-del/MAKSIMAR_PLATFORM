from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    NodeRole,
    NodeRoleContract,
)


def test_node_role_models_build() -> None:
    """Node role models should build successfully."""
    contract = NodeRoleContract(
        total_nodes=3,
        nodes=(
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
        ),
    )

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.nodes[0].role_type == "mobile_node"
    assert contract.nodes[1].role_type == "dev_node"
    assert contract.nodes[2].role_type == "home_node"
