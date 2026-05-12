from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.governance_federation_gap_summary_builder import (
    build_governance_federation_gap_summary,
)


def test_governance_federation_gap_summary_builder_smoke() -> None:
    summary = build_governance_federation_gap_summary()

    assert summary["summary_ready"] is True
    assert summary["existing_surfaces_reused"] is True
    assert summary["missing_required_surface_count"] == 0
    assert summary["proposal_audit_allowed_next"] is True
    assert summary["codegen_allowed_now"] is False
    assert summary["sandbox_allowed_now"] is False
    assert summary["self_expansion_allowed_now"] is False
