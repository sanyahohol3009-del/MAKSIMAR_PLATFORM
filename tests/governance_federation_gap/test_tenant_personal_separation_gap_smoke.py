from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy.memory_federation_policy_models import (
    build_memory_federation_policy,
)
from MAKSIMAR_CORE_LIB.memory_policy.memory_trust_scope_models import (
    build_memory_trust_scope_contract,
)


def test_tenant_personal_separation_gap_smoke() -> None:
    trust = build_memory_trust_scope_contract()
    federation = build_memory_federation_policy()

    assert trust.tenant_personal_separation_ready is True
    assert federation.tenant_isolation_required is True
    assert federation.personal_memory_isolation_required is True
    assert federation.cross_tenant_merge_allowed_without_approval is False
