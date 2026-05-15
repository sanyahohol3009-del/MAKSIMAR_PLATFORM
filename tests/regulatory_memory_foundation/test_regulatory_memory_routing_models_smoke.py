from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_memory_routing_registry


def test_regulatory_memory_routing_models_smoke() -> None:
    registry = build_regulatory_memory_routing_registry()

    assert registry.registry_ready is True
    assert len(registry.routes) >= 3
    assert registry.update_approval_ready is True
    assert registry.tenant_scope_required is True
    assert registry.business_scope_required is True
    assert registry.jurisdiction_scope_required is True
    assert registry.source_scope_required is True
    assert registry.cross_tenant_retrieval_allowed is False
    assert registry.auto_routing_merge_allowed is False
