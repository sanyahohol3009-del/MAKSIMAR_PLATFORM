from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_distributed_workload_placement_contract,
)


def test_distributed_workload_placement_contract_builds() -> None:
    """Distributed workload placement contract should build successfully."""
    contract = build_distributed_workload_placement_contract()

    assert contract.total_decisions == 3
    assert len(contract.decisions) == 3


def test_distributed_workload_placement_contract_contains_expected_workloads() -> None:
    """Distributed workload placement should expose expected workload kinds."""
    contract = build_distributed_workload_placement_contract()

    workload_kinds = {entry.workload_kind for entry in contract.decisions}

    assert "ai_chat" in workload_kinds
    assert "media_render" in workload_kinds
    assert "simulation_task" in workload_kinds


def test_distributed_workload_placement_contract_contains_selected_node() -> None:
    """Distributed workload placement should select eligible nodes."""
    contract = build_distributed_workload_placement_contract()

    first = contract.decisions[0]
    assert first.workload_kind == "ai_chat"
    assert first.selected_node_id == "mobile_001"
    assert first.decision_status in ("selected", "degraded_selected", "unavailable")
