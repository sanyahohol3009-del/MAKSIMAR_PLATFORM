from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.regulatory_memory_final_summary_builder import (
    build_regulatory_memory_final_summary,
)


def test_regulatory_memory_final_summary_builder_smoke() -> None:
    summary = build_regulatory_memory_final_summary()

    assert summary["summary_ready"] is True
    assert summary["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_FINAL_CLOSURE"
    assert summary["closed_step_count"] == 9
    assert summary["acceptance_doc_count"] == 10
    assert summary["same_tenant_only"] is True
    assert summary["leak_detected"] is False
    assert summary["operator_approval_required_for_future_changes"] is True
