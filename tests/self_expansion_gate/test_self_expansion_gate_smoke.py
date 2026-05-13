from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_gate


def test_self_expansion_gate_smoke() -> None:
    gate = build_self_expansion_gate()

    assert gate["gate_ready"] is True
    assert "gap_to_proposal_context" in gate["gate_flow"]
    assert "human_approval_required" in gate["gate_flow"]
    assert gate["proposal_only_self_expansion_allowed"] is True
    assert gate["autonomous_self_expansion_allowed"] is False
    assert gate["client_metrics_learning_allowed_next"] is True
