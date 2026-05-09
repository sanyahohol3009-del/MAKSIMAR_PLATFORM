from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_memory_layer_architecture_binding_contract,
)


def test_memory_layer_architecture_binding_smoke() -> None:
    contract = build_memory_layer_architecture_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.ready_bindings == contract.total_bindings
    assert contract.dashboard_visible_bindings == contract.total_bindings
    assert contract.source_contract_bound_bindings == contract.total_bindings
