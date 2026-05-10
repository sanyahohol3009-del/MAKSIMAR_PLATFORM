from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_customer_metrics_memory_contract,
    build_enterprise_memory_preview,
    build_enterprise_memory_summary,
    build_enterprise_policy_memory_contract,
    build_legal_jurisdiction_contract,
    build_memory_isolation_contract,
    build_regulatory_memory_contract,
    build_tenant_memory_scope_contract,
)


def test_enterprise_memory_ready_smoke() -> None:
    tenants = build_tenant_memory_scope_contract()
    jurisdictions = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()
    policies = build_enterprise_policy_memory_contract()
    metrics = build_customer_metrics_memory_contract()
    summary = build_enterprise_memory_summary()
    preview = build_enterprise_memory_preview()

    assert tenants.ready_scopes == tenants.total_scopes
    assert jurisdictions.ready_jurisdictions == jurisdictions.total_jurisdictions
    assert regulatory.ready_records == regulatory.total_records
    assert isolation.ready_isolations == isolation.total_isolations
    assert policies.ready_policies == policies.total_policies
    assert metrics.ready_metrics == metrics.total_metrics
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["runtime_policy_binding_allowed"] == 0
    assert preview["cross_boundary_merge_allowed"] == 0
