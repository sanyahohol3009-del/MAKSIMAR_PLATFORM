from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_node_runtime_summary_contract,
)


def test_node_runtime_summary_contract_builds() -> None:
    """Node runtime summary contract should build successfully."""
    contract = build_node_runtime_summary_contract()

    assert contract.summary_id == "node_runtime_summary"
    assert contract.total_nodes == 3
    assert contract.gpu_enabled_nodes == 2
    assert contract.degraded_nodes == 0
    assert contract.max_queue_depth == 4
    assert contract.min_health_score == 84
