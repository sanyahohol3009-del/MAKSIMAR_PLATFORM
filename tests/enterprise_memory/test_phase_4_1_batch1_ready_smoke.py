from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_legal_jurisdiction_contract,
    build_memory_isolation_contract,
    build_regulatory_memory_contract,
    build_tenant_memory_scope_contract,
)


def test_phase_4_1_batch1_ready_smoke() -> None:
    tenant = build_tenant_memory_scope_contract()
    jurisdiction = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()

    assert tenant.ready_scopes == tenant.total_scopes
    assert jurisdiction.ready_jurisdictions == jurisdiction.total_jurisdictions
    assert regulatory.ready_records == regulatory.total_records
    assert isolation.ready_isolations == isolation.total_isolations

    assert regulatory.runtime_policy_binding_allowed_records == 0
    assert isolation.cross_tenant_merge_allowed_isolations == 0
    assert isolation.cross_country_merge_allowed_isolations == 0
