from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import build_memory_policy_scope_contract


def test_memory_policy_scope_models_smoke() -> None:
    contract = build_memory_policy_scope_contract()

    assert contract.total_scopes >= 1
    assert contract.ready_scopes == contract.total_scopes
    assert contract.evidence_required_scopes == contract.total_scopes
    assert contract.approval_required_scopes == contract.total_scopes
    assert contract.conflict_resolution_required_scopes == contract.total_scopes
    assert contract.promotion_allowed_scopes == contract.total_scopes
    assert contract.auto_promotion_allowed_scopes == 0
    assert contract.read_only_scopes == contract.total_scopes
