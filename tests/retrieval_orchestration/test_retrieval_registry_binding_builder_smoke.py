from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_registry_binding_contract,
)


def test_retrieval_registry_binding_builder_smoke() -> None:
    contract = build_retrieval_registry_binding_contract()

    assert contract.binding_ready is True
    assert contract.total_bindings == len(contract.entries)
    assert contract.ready_bindings == contract.total_bindings
    assert contract.selected_by_retrieval_bindings >= 1
    assert contract.retrieval_visible_total >= 1
    assert contract.observability_visible_total >= 1
