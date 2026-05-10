from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_capability_contract,
)


def test_mempalace_capability_builder_smoke() -> None:
    contract = build_mempalace_capability_contract()

    assert contract.total_capabilities == 4
    assert contract.ready_capabilities == contract.total_capabilities
    assert contract.retrieval_allowed_capabilities == contract.total_capabilities
    assert contract.canonical_truth_allowed_capabilities == 0
    assert contract.regulatory_memory_allowed_capabilities == 0
    assert contract.enterprise_policy_memory_allowed_capabilities == 0
    assert contract.technical_truth_allowed_capabilities == 0
    assert contract.audit_truth_allowed_capabilities == 0
    assert contract.approval_truth_allowed_capabilities == 0
    assert contract.auto_promotion_allowed_capabilities == 0
    assert contract.auto_conflict_resolution_allowed_capabilities == 0
    assert contract.runtime_mutation_allowed_capabilities == 0
