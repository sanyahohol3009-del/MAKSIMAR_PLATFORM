from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract


def test_knowledge_graph_not_truth_smoke() -> None:
    contract = build_evidence_memory_contract()

    assert contract.memory_truth_records == contract.total_records
    assert contract.knowledge_graph_projection_records == contract.total_records

    for record in contract.records:
        assert record.memory_truth is True
        assert record.knowledge_graph_projection_only is True
