from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.proposal_audit_spine_summary_builder import (
    build_proposal_audit_spine_summary,
)


def test_proposal_audit_spine_summary_builder_smoke() -> None:
    summary = build_proposal_audit_spine_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.2"
    assert summary["proposal_visible"] is True
    assert summary["audit_visible"] is True
    assert summary["approval_visible"] is True
    assert summary["controlled_codegen_allowed_next"] is True
