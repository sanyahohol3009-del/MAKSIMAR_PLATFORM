from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_inspector_binding


def test_proposal_inspector_binding_smoke() -> None:
    binding = build_proposal_inspector_binding()

    assert binding["binding_ready"] is True
    assert binding["missing_surfaces"] == ()
    assert binding["proposal_visible"] is True
    assert binding["proposal_execution_allowed"] is False
    assert binding["code_write_allowed"] is False
