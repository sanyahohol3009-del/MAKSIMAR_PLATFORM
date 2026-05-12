from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_summary


def test_no_codegen_in_proposal_audit_spine_smoke() -> None:
    summary = build_proposal_audit_summary()

    assert summary["code_write_allowed"] is False
    assert summary["action_execution_allowed"] is False
    assert summary["sandbox_execution_allowed_now"] is False
    assert summary["self_expansion_allowed_now"] is False
    assert summary["productization_allowed_now"] is False
