from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_memory_self_read_summary_builder import (
    build_jarvis_memory_self_read_summary,
)


def test_jarvis_memory_self_read_summary_smoke() -> None:
    summary = build_jarvis_memory_self_read_summary()

    assert summary["summary_ready"] is True
    assert summary["preview_ready"] is True
    assert summary["can_explain_where_searched"] is True
    assert summary["can_explain_sources_used"] is True
    assert summary["can_explain_constraints_applied"] is True
    assert summary["can_explain_evidence_pack"] is True
    assert summary["can_explain_preview_trace"] is True
    assert summary["canonical_write_allowed"] is False
    assert summary["runtime_mutation_allowed"] is False
