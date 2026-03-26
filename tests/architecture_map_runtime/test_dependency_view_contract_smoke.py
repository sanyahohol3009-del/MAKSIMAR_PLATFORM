from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_server_dependency_view_contract,
)


def test_server_dependency_view_contract_builds() -> None:
    """Server-side dependency view contract should build successfully."""
    contract = build_server_dependency_view_contract()

    assert contract.total_edges == 3
    assert len(contract.edges) == 3


def test_server_dependency_view_contract_is_bound_to_source_contracts() -> None:
    """Server-side dependency view contract must stay bound to source contracts."""
    contract = build_server_dependency_view_contract()

    assert all(edge.source_contract_bound for edge in contract.edges)
    assert contract.edges[0].upstream_module_id == "control_plane"
    assert contract.edges[-1].downstream_module_id == "oob_dashboard"
