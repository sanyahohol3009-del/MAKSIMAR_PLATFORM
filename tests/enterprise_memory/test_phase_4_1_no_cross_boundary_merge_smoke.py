from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_customer_metrics_memory_contract,
    build_enterprise_memory_phase_readiness,
    build_memory_isolation_contract,
)


def test_phase_4_1_no_cross_boundary_merge_smoke() -> None:
    isolation = build_memory_isolation_contract()
    metrics = build_customer_metrics_memory_contract()
    readiness = build_enterprise_memory_phase_readiness()

    assert isolation.cross_tenant_merge_allowed_isolations == 0
    assert isolation.cross_business_merge_allowed_isolations == 0
    assert isolation.cross_country_merge_allowed_isolations == 0
    assert metrics.cross_tenant_aggregation_allowed_metrics == 0
    assert readiness.no_cross_boundary_merge is True
