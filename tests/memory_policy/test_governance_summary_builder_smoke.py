from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import build_governance_summary


def test_governance_summary_builder_smoke() -> None:
    summary = build_governance_summary()

    assert summary["summary_ready"] is True
    assert summary["policy_scope_entries"] >= 1
    assert summary["policy_scope_ready_entries"] == summary["policy_scope_entries"]
    assert summary["governance_ready_bindings"] == summary["governance_binding_entries"]
    assert summary["auto_promotion_allowed_scopes"] == 0
    assert summary["conflict_detected_bindings"] == 0
