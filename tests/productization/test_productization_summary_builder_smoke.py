from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.productization_summary_builder import (
    build_productization_summary,
)


def test_productization_summary_builder_smoke() -> None:
    summary = build_productization_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.8"
    assert summary["sale_ready_claim_allowed"] is True
    assert summary["operator_approval_required"] is True
    assert summary["operator_approval_granted"] is False
    assert summary["roadmap_v5_1_closure_allowed_next"] is True
