from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_registry_binding_contract,
)


def test_retrieval_memory_registry_ai_router_binding_smoke() -> None:
    contract = build_retrieval_registry_binding_contract()

    selected_components = {
        entry.component_kind
        for entry in contract.entries
        if entry.selected_by_retrieval
    }

    assert "memory_registry" in selected_components
    assert "global_registry" in selected_components
    assert "ai_router_binding" in selected_components
