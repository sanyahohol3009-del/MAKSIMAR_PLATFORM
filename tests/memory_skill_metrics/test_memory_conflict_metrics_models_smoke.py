from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_conflict_metrics_contract,
)


def test_memory_conflict_metrics_models_smoke() -> None:
    contract = build_memory_conflict_metrics_contract()

    assert contract.total_entries == 3
    assert contract.ready_entries == contract.total_entries
    assert contract.conflict_entries == 0
    assert contract.resolution_required_entries == 0
    assert contract.evidence_truth_ready_entries == contract.total_entries
    assert contract.knowledge_graph_projection_entries == contract.total_entries
    assert contract.read_only_entries == contract.total_entries
