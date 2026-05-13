from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_gate


def test_no_autonomous_self_expansion_smoke() -> None:
    gate = build_self_expansion_gate()

    assert gate["autonomous_self_expansion_allowed"] is False
    assert gate["direct_core_write_allowed"] is False
    assert gate["auto_apply_allowed"] is False
    assert gate["deployment_allowed"] is False
    assert gate["runtime_mutation_allowed"] is False
    assert gate["productization_allowed_now"] is False
