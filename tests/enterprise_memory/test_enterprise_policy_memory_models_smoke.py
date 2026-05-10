from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_policy_memory_contract,
)


def test_enterprise_policy_memory_models_smoke() -> None:
    contract = build_enterprise_policy_memory_contract()

    assert contract.total_policies == 3
    assert contract.ready_policies == contract.total_policies
    assert contract.source_bound_policies == contract.total_policies
    assert contract.versioned_policies == contract.total_policies
    assert contract.governance_gate_required_policies == contract.total_policies
    assert contract.approval_required_policies == contract.total_policies
    assert contract.read_only_policies == contract.total_policies
    assert contract.auto_enforcement_allowed_policies == 0
    assert contract.runtime_policy_binding_allowed_policies == 0
    assert contract.pending_approval_policies == contract.total_policies
