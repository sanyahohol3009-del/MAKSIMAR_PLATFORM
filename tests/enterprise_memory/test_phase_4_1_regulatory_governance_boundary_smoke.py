from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_memory_phase_readiness,
    build_enterprise_policy_memory_contract,
    build_regulatory_memory_contract,
)


def test_phase_4_1_regulatory_governance_boundary_smoke() -> None:
    regulatory = build_regulatory_memory_contract()
    policies = build_enterprise_policy_memory_contract()
    readiness = build_enterprise_memory_phase_readiness()

    assert regulatory.pending_approval_records == regulatory.total_records
    assert regulatory.runtime_policy_binding_allowed_records == 0

    assert policies.governance_gate_required_policies == policies.total_policies
    assert policies.pending_approval_policies == policies.total_policies
    assert policies.runtime_policy_binding_allowed_policies == 0
    assert policies.auto_enforcement_allowed_policies == 0

    assert readiness.governance_gate_ready is True
    assert readiness.pending_approval_ready is True
    assert readiness.no_runtime_policy_binding is True
