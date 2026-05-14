from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_no_hidden_autonomy_gate


def test_no_hidden_autonomy_gate_smoke() -> None:
    gate = build_no_hidden_autonomy_gate()

    assert gate["gate_ready"] is True
    assert gate["hidden_autonomy_allowed"] is False
    assert gate["direct_core_write_allowed"] is False
    assert gate["auto_apply_allowed"] is False
    assert gate["runtime_mutation_allowed"] is False
    assert gate["deployment_allowed_now"] is False
    assert gate["sale_ready_claim_allowed"] is True
