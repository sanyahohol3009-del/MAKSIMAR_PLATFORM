from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_registry_binding_contract,
)


def test_retrieval_registry_binding_components_smoke() -> None:
    contract = build_retrieval_registry_binding_contract()
    component_kinds = {entry.component_kind for entry in contract.entries}

    assert "memory_registry" in component_kinds
    assert "global_registry" in component_kinds
    assert "ai_router_binding" in component_kinds
    assert "memory_skill_metrics" in component_kinds
