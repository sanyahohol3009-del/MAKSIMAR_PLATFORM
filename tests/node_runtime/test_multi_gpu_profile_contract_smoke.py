from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_multi_gpu_profile_contract,
)


def test_multi_gpu_profile_contract_builds() -> None:
    """Multi-GPU profile contract should build successfully."""
    contract = build_multi_gpu_profile_contract()

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3


def test_multi_gpu_profile_contract_is_consistent() -> None:
    """Multi-GPU profile contract should stay consistent per node."""
    contract = build_multi_gpu_profile_contract()

    assert contract.nodes[0].node_id == "mobile_001"
    assert contract.nodes[-1].node_id == "home_001"
    assert all(node.gpu_count == len(node.accelerators) for node in contract.nodes)
