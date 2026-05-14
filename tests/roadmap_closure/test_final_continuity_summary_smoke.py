from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_final_continuity_preview


def test_final_continuity_summary_smoke() -> None:
    preview = build_final_continuity_preview()

    assert preview["preview_ready"] is True
    assert preview["closed_block_count"] >= 10
    assert "PHASE 6.8 Productization / Sale-Ready Sovereign AI" in preview["closed_blocks"]
    assert preview["deployment_allowed_now"] is False
    assert preview["external_release_allowed_now"] is False
