from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_final_acceptance_index_preview


def test_final_acceptance_index_smoke() -> None:
    preview = build_final_acceptance_index_preview()

    assert preview["preview_ready"] is True
    assert preview["roadmap_family"] == "memory_roadmap_v5_1"
    assert preview["closed_phase"] == "PHASE 6.8"
    assert preview["acceptance_doc_count"] >= 11
    assert preview["missing_acceptance_docs"] == ()
    assert preview["final_closure_allowed"] is True
