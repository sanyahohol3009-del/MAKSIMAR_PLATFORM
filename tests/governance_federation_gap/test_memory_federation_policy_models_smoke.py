from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.memory_federation_policy_models import (
    build_memory_federation_policy,
)


def test_memory_federation_policy_models_smoke() -> None:
    policy = build_memory_federation_policy()

    assert policy.federation_policy_ready is True
    assert policy.tenant_isolation_required is True
    assert policy.personal_memory_isolation_required is True
    assert policy.jurisdiction_isolation_required is True
    assert policy.cross_tenant_merge_allowed_without_approval is False
    assert policy.automatic_federation_write_allowed is False
    assert policy.runtime_mutation_allowed is False
