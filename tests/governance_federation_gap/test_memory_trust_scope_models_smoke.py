from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.memory_trust_scope_models import (
    build_memory_trust_scope_contract,
)


def test_memory_trust_scope_models_smoke() -> None:
    contract = build_memory_trust_scope_contract()

    assert contract.trust_scope_ready is True
    assert contract.canonical_scope_present is True
    assert contract.regulatory_scope_present is True
    assert contract.enterprise_policy_scope_present is True
    assert contract.tenant_scope_present is True
    assert contract.personal_scope_present is True
    assert contract.subordinate_backend_scope_present is True
    assert contract.tenant_personal_separation_ready is True
    assert contract.runtime_mutation_allowed is False
