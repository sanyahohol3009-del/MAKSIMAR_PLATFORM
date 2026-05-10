from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_customer_metrics_memory_contract,
)


def test_customer_metrics_memory_models_smoke() -> None:
    contract = build_customer_metrics_memory_contract()

    assert contract.total_metrics == 3
    assert contract.ready_metrics == contract.total_metrics
    assert contract.tenant_isolated_metrics == contract.total_metrics
    assert contract.client_isolated_metrics == contract.total_metrics
    assert contract.country_bound_metrics == contract.total_metrics
    assert contract.read_only_metrics == contract.total_metrics
    assert contract.pii_exposure_allowed_metrics == 0
    assert contract.cross_tenant_aggregation_allowed_metrics == 0
    assert contract.runtime_policy_binding_allowed_metrics == 0
