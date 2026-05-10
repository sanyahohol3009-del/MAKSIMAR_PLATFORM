from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_policy_memory_contract,
    build_regulatory_memory_contract,
)


def test_regulatory_memory_ready_smoke() -> None:
    regulatory = build_regulatory_memory_contract()
    policies = build_enterprise_policy_memory_contract()

    assert regulatory.ready_records == regulatory.total_records
    assert regulatory.source_bound_records == regulatory.total_records
    assert regulatory.pending_approval_records == regulatory.total_records
    assert regulatory.runtime_policy_binding_allowed_records == 0

    assert policies.ready_policies == policies.total_policies
    assert policies.governance_gate_required_policies == policies.total_policies
    assert policies.runtime_policy_binding_allowed_policies == 0
