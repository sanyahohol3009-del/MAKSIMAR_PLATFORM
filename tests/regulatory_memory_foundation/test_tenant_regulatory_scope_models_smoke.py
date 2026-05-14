from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_tenant_regulatory_scope_registry


def test_tenant_regulatory_scope_models_smoke() -> None:
    registry = build_tenant_regulatory_scope_registry()

    assert registry.registry_ready is True
    assert len(registry.entries) >= 3
    assert registry.tenant_id_required is True
    assert registry.business_id_required is True
    assert registry.country_code_required is True
    assert registry.jurisdiction_id_required is True
    assert registry.tenant_isolation_required is True
    assert registry.cross_tenant_merge_allowed is False
    assert registry.runtime_mutation_allowed is False
