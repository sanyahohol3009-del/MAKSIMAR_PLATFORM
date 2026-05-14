from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_polyglot_model_worker_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.polyglot_model_worker_bridge_summary_builder import (
    build_polyglot_model_worker_bridge_summary,
)


def test_polyglot_model_worker_final_acceptance_smoke() -> None:
    preview = build_polyglot_model_worker_preview()
    summary = build_polyglot_model_worker_bridge_summary()
    doc = Path("docs/architecture/foundation/phase_6_7_polyglot_model_worker_bridge_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["productization_allowed_next"] is True
    assert preview["productization_allowed_now"] is False
