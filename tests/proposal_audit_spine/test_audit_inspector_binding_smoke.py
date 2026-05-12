from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_audit_inspector_binding


def test_audit_inspector_binding_smoke() -> None:
    binding = build_audit_inspector_binding()

    assert binding["binding_ready"] is True
    assert binding["missing_surfaces"] == ()
    assert binding["audit_visible"] is True
    assert binding["sandbox_contract_visible_read_only"] is True
    assert binding["sandbox_execution_allowed_now"] is False
