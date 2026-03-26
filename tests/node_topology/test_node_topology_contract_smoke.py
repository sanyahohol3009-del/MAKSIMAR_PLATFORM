from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_node_topology_runtime_contract,
)


def test_node_topology_runtime_contract_builds() -> None:
    """Node topology runtime contract should build successfully."""
    contract = build_node_topology_runtime_contract()

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.online_nodes >= 1
    assert contract.offline_nodes == 0


def test_node_topology_runtime_contract_contains_expected_nodes() -> None:
    """Node topology runtime contract should expose expected nodes and states."""
    contract = build_node_topology_runtime_contract()

    assert contract.nodes[0].node_id == "mobile_001"
    assert contract.nodes[-1].node_id == "home_001"
    assert contract.nodes[0].topology_visible is True
    assert all(entry.connectivity_state in ("online", "degraded", "offline") for entry in contract.nodes)
