from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import build_promotion_summary


def test_promotion_summary_builder_smoke() -> None:
    summary = build_promotion_summary()

    assert summary["summary_ready"] is True
    assert summary["promotion_binding_entries"] >= 1
    assert summary["promotion_ready_bindings"] == summary["promotion_binding_entries"]
    assert summary["auto_promotion_allowed_bindings"] == 0
    assert summary["approval_required_bindings"] == summary["promotion_binding_entries"]
