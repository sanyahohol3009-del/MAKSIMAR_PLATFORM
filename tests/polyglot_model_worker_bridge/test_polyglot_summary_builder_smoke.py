from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.polyglot_model_worker_bridge_summary_builder import (
    build_polyglot_model_worker_bridge_summary,
)


def test_polyglot_summary_builder_smoke() -> None:
    summary = build_polyglot_model_worker_bridge_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.7"
    assert summary["artifact_language_models_ready"] is True
    assert summary["model_worker_bridge_models_ready"] is True
    assert summary["productization_allowed_next"] is True
