from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_adapter_selection_metrics_contract,
    build_memory_conflict_metrics_contract,
    build_memory_promotion_metrics_contract,
    build_memory_retrieval_metrics_contract,
    build_memory_skill_metrics_contract,
    build_memory_skill_preview,
    build_memory_skill_summary,
)


def test_phase_2_2_final_acceptance_smoke() -> None:
    base = build_memory_skill_metrics_contract()
    retrieval = build_memory_retrieval_metrics_contract()
    conflict = build_memory_conflict_metrics_contract()
    promotion = build_memory_promotion_metrics_contract()
    adapter = build_memory_adapter_selection_metrics_contract()
    summary = build_memory_skill_summary()
    preview = build_memory_skill_preview()

    assert base.total_entries == 5
    assert base.active_entries == base.total_entries

    assert retrieval.total_entries == 3
    assert retrieval.ready_entries == retrieval.total_entries
    assert retrieval.conflict_entries == 0
    assert retrieval.backend_execution_allowed_entries == 0
    assert retrieval.mgrep_blocked_entries == retrieval.total_entries
    assert retrieval.sqlite_vec_blocked_entries == retrieval.total_entries
    assert retrieval.read_only_entries == retrieval.total_entries

    assert conflict.total_entries == 3
    assert conflict.ready_entries == conflict.total_entries
    assert conflict.conflict_entries == 0
    assert conflict.resolution_required_entries == 0
    assert conflict.evidence_truth_ready_entries == conflict.total_entries
    assert conflict.knowledge_graph_projection_entries == conflict.total_entries
    assert conflict.read_only_entries == conflict.total_entries

    assert promotion.total_entries == 3
    assert promotion.ready_entries == promotion.total_entries
    assert promotion.auto_promotion_allowed_entries == 0
    assert promotion.approval_required_entries == promotion.total_entries
    assert promotion.conflict_clear_entries == promotion.total_entries
    assert promotion.citation_ready_entries == promotion.total_entries
    assert promotion.read_only_entries == promotion.total_entries

    assert adapter.total_entries == 2
    assert adapter.ready_entries == adapter.total_entries
    assert adapter.backend_execution_allowed_entries == 0
    assert adapter.policy_gate_ready_entries == adapter.total_entries
    assert adapter.mgrep_blocked_entries == adapter.total_entries
    assert adapter.sqlite_vec_blocked_entries == adapter.total_entries
    assert adapter.read_only_entries == adapter.total_entries

    assert summary["total_metric_entries"] == 16
    assert summary["ready_metric_entries"] == 16
    assert summary["conflict_entries"] == 0
    assert summary["promotion_auto_allowed_entries"] == 0
    assert summary["backend_execution_allowed_entries"] == 0
    assert summary["mgrep_blocked"] is True
    assert summary["sqlite_vec_blocked"] is True
    assert summary["read_only_ready"] is True
    assert summary["summary_ready"] is True

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
