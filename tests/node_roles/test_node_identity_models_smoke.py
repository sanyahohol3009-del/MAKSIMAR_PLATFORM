from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    CanonicalNodeIdentity,
    CanonicalNodeIdentityContract,
)


def test_node_identity_models_build() -> None:
    """Canonical node identity models should build successfully."""
    contract = CanonicalNodeIdentityContract(
        total_nodes=3,
        nodes=(
            CanonicalNodeIdentity(
                node_id="mobile_001",
                node_type="mobile_node",
            ),
            CanonicalNodeIdentity(
                node_id="dev_001",
                node_type="dev_node",
            ),
            CanonicalNodeIdentity(
                node_id="home_001",
                node_type="home_node",
            ),
        ),
    )

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.nodes[0].node_id == "mobile_001"
    assert contract.nodes[-1].node_type == "home_node"
