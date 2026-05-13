from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.self_expansion_gate_summary_builder import (
    build_self_expansion_gate_summary,
)


def test_self_expansion_final_acceptance_smoke() -> None:
    preview = build_self_expansion_preview()
    summary = build_self_expansion_gate_summary()
    doc = Path("docs/architecture/foundation/phase_6_5_bootstrapped_self_expansion_gate_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["client_metrics_learning_allowed_next"] is True
    assert preview["productization_allowed_now"] is False
