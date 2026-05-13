from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.client_learning_input_summary_builder import (
    build_client_learning_input_summary,
)


def test_client_learning_input_summary_builder_smoke() -> None:
    summary = build_client_learning_input_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.6"
    assert summary["tenant_boundary_ready"] is True
    assert summary["privacy_boundary_ready"] is True
    assert summary["polyglot_model_worker_allowed_next"] is True
