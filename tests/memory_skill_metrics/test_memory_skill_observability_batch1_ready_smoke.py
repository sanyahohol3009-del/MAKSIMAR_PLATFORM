from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_conflict_metrics_contract,
    build_memory_retrieval_metrics_contract,
)


def test_memory_skill_observability_batch1_ready_smoke() -> None:
    retrieval = build_memory_retrieval_metrics_contract()
    conflict = build_memory_conflict_metrics_contract()

    assert retrieval.ready_entries == retrieval.total_entries
    assert conflict.ready_entries == conflict.total_entries
    assert retrieval.backend_execution_allowed_entries == 0
    assert conflict.conflict_entries == 0
