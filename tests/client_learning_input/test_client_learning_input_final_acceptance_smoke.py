from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_client_learning_input_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.client_learning_input_summary_builder import (
    build_client_learning_input_summary,
)


def test_client_learning_input_final_acceptance_smoke() -> None:
    preview = build_client_learning_input_preview()
    summary = build_client_learning_input_summary()
    doc = Path("docs/architecture/foundation/phase_6_6_client_metrics_learning_input_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["polyglot_model_worker_allowed_next"] is True
    assert preview["productization_allowed_now"] is False
