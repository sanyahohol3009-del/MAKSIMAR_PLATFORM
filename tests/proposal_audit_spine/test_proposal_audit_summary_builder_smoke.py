from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_summary


def test_proposal_audit_summary_builder_smoke() -> None:
    summary = build_proposal_audit_summary()

    assert summary["summary_ready"] is True
    assert summary["proposal_visible"] is True
    assert summary["audit_visible"] is True
    assert summary["approval_visible"] is True
    assert summary["controlled_codegen_allowed_next"] is True
    assert summary["code_write_allowed"] is False
