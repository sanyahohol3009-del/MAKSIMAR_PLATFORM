from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_final_closure_preview


def test_final_closure_preview_builder_smoke() -> None:
    preview = build_final_closure_preview()

    assert preview["preview_ready"] is True
    assert preview["final_closure_ready"] is True
    assert preview["roadmap_family"] == "memory_roadmap_v5_1"
    assert preview["closed_phase"] == "PHASE 6.8"
    assert "project_memory_savepoint_next" in preview["preview_path"]
