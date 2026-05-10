from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_memory_isolation_contract,
)


def test_memory_isolation_models_smoke() -> None:
    contract = build_memory_isolation_contract()

    assert contract.total_isolations == 3
    assert contract.ready_isolations == contract.total_isolations
    assert contract.read_only_isolations == contract.total_isolations
    assert contract.cross_tenant_merge_allowed_isolations == 0
    assert contract.cross_business_merge_allowed_isolations == 0
    assert contract.cross_country_merge_allowed_isolations == 0
    assert contract.runtime_policy_binding_allowed_isolations == 0
