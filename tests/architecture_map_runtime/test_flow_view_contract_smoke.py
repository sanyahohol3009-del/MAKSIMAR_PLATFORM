from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_server_flow_view_contract,
)


def test_server_flow_view_contract_builds() -> None:
    """Server-side flow view contract should build successfully."""
    contract = build_server_flow_view_contract()

    assert contract.total_steps == 5
    assert len(contract.steps) == 5


def test_server_flow_view_contract_is_bound_to_source_contracts() -> None:
    """Server-side flow view contract must stay bound to source contracts."""
    contract = build_server_flow_view_contract()

    assert all(step.source_contract_bound for step in contract.steps)
    assert contract.steps[0].source_component == "input_adapter"
    assert contract.steps[-1].target_component == "oob_dashboard"
