from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_server_module_view_contract,
)


def test_server_module_view_contract_builds() -> None:
    """Server-side module view contract should build successfully."""
    contract = build_server_module_view_contract()

    assert contract.total_modules == 3
    assert len(contract.modules) == 3


def test_server_module_view_contract_is_bound_to_source_contracts() -> None:
    """Server-side module view contract must stay bound to source contracts."""
    contract = build_server_module_view_contract()

    assert all(module.source_contract_bound for module in contract.modules)
    assert contract.modules[0].module_id == "control_plane"
    assert contract.modules[-1].module_id == "oob_dashboard"
