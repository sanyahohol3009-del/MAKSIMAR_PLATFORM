from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_preview


def test_proposal_audit_preview_builder_smoke() -> None:
    preview = build_proposal_audit_preview()

    assert preview["preview_ready"] is True
    assert "proposal_inspector_binding" in preview["preview_path"]
    assert "approval_read_model" in preview["preview_path"]
    assert "controlled_codegen_next_only" in preview["preview_path"]
    assert preview["controlled_codegen_allowed_next"] is True
