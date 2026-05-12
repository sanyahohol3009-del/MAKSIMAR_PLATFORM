from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_proposal_context


def test_codegen_proposal_builder_smoke() -> None:
    proposal = build_codegen_proposal_context()

    assert proposal["proposal_context_ready"] is True
    assert "proposal_audit_spine" in proposal["proposal_package_flow"]
    assert proposal["operator_review_required"] is True
    assert proposal["approval_granted_by_default"] is False
    assert proposal["direct_core_write_allowed"] is False
