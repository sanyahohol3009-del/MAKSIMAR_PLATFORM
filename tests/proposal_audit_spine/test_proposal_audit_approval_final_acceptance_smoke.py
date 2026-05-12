from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.proposal_audit_spine_summary_builder import (
    build_proposal_audit_spine_summary,
)


def test_proposal_audit_approval_final_acceptance_smoke() -> None:
    preview = build_proposal_audit_preview()
    summary = build_proposal_audit_spine_summary()
    doc = Path("docs/architecture/foundation/phase_6_2_proposal_audit_approval_spine_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["controlled_codegen_allowed_next"] is True
    assert preview["code_write_allowed"] is False
