from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_tenant_memory_scope_contract,
)


def test_tenant_memory_models_smoke() -> None:
    contract = build_tenant_memory_scope_contract()

    assert contract.total_scopes == 3
    assert contract.ready_scopes == contract.total_scopes
    assert contract.tenant_isolated_scopes == contract.total_scopes
    assert contract.business_isolated_scopes == contract.total_scopes
    assert contract.client_isolated_scopes == contract.total_scopes
    assert contract.country_bound_scopes == contract.total_scopes
    assert contract.read_only_scopes == contract.total_scopes
    assert contract.runtime_policy_approved_scopes == 0
