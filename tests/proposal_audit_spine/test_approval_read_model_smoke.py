from __future__ import annotations

from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_approval_read_model


def test_approval_read_model_smoke() -> None:
    model = build_approval_read_model()

    assert model["approval_read_model_ready"] is True
    assert model["missing_surfaces"] == ()
    assert model["approval_visible"] is True
    assert model["operator_approval_required"] is True
    assert model["operator_approval_granted"] is False
    assert model["approval_granted_by_default"] is False
