from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.self_expansion_gate_summary_builder import (
    build_self_expansion_gate_summary,
)


def test_self_expansion_gate_summary_builder_smoke() -> None:
    summary = build_self_expansion_gate_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.5"
    assert summary["gap_detection_allowed"] is True
    assert summary["proposal_preparation_allowed"] is True
    assert summary["client_metrics_learning_allowed_next"] is True
    assert summary["productization_allowed_now"] is False
