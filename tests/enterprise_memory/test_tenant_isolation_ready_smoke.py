from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_memory_isolation_contract,
    build_tenant_memory_scope_contract,
)


def test_tenant_isolation_ready_smoke() -> None:
    tenants = build_tenant_memory_scope_contract()
    isolation = build_memory_isolation_contract()

    assert tenants.ready_scopes == tenants.total_scopes
    assert isolation.ready_isolations == isolation.total_isolations
    assert isolation.cross_tenant_merge_allowed_isolations == 0
    assert isolation.cross_business_merge_allowed_isolations == 0
    assert isolation.cross_country_merge_allowed_isolations == 0
