from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_update_approval_gate_preview


def test_regulatory_update_approval_gate_smoke() -> None:
    preview = build_regulatory_update_approval_gate_preview()

    assert preview["preview_ready"] is True
    assert preview["proposal_count"] >= 2
    assert preview["approval_gate_required"] is True
    assert preview["approval_required"] is True
    assert preview["approval_granted"] is False
    assert preview["proposal_only"] is True
    assert preview["diff_required"] is True
    assert preview["operator_review_required"] is True
    assert preview["auto_apply_allowed"] is False
