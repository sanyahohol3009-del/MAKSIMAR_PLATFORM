from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_current_state_handoff_preview


def test_current_state_handoff_smoke() -> None:
    preview = build_current_state_handoff_preview()

    assert preview["preview_ready"] is True
    assert preview["state_item_count"] >= 10
    assert "current_closed_phase=PHASE_6_8" in preview["state_items"]
    assert "direct_core_write_allowed=False" in preview["state_items"]
    assert "deployment_allowed_now=False" in preview["state_items"]
