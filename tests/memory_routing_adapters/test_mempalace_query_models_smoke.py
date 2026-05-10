from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_query_contract,
)


def test_mempalace_query_models_smoke() -> None:
    contract = build_mempalace_query_contract()

    assert contract.total_queries == 4
    assert contract.ready_queries == contract.total_queries
    assert contract.retrieval_allowed_queries == contract.total_queries
    assert contract.evidence_pack_required_queries == contract.total_queries
    assert contract.preview_trace_required_queries == contract.total_queries
    assert contract.policy_check_required_queries == contract.total_queries
    assert contract.source_attribution_required_queries == contract.total_queries
    assert contract.canonical_truth_allowed_queries == 0
    assert contract.runtime_mutation_allowed_queries == 0
