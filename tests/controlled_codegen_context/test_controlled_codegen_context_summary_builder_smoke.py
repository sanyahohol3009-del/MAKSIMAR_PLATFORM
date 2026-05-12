from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.controlled_codegen_context_summary_builder import (
    build_controlled_codegen_context_summary,
)


def test_controlled_codegen_context_summary_builder_smoke() -> None:
    summary = build_controlled_codegen_context_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.3"
    assert summary["intent_models_ready"] is True
    assert summary["boundary_models_ready"] is True
    assert summary["sandbox_owner_review_allowed_next"] is True
