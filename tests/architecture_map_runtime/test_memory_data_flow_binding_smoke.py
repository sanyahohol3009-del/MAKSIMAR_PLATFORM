from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_memory_data_flow_binding_contract,
)


def test_memory_data_flow_binding_smoke() -> None:
    contract = build_memory_data_flow_binding_contract()

    assert contract.total_flows == len(contract.entries)
    assert contract.ready_flows == contract.total_flows
    assert contract.dashboard_visible_flows == contract.total_flows
    assert contract.source_bound_flows == contract.total_flows
    assert contract.target_bound_flows == contract.total_flows
