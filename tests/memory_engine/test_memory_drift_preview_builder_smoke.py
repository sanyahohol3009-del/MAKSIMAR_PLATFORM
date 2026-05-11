from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_drift_preview


def test_memory_drift_preview_builder_smoke() -> None:
    preview = build_memory_drift_preview()

    assert preview["preview_ready"] is True
    assert preview["total_signals"] == 1
    assert preview["total_candidates"] == 1
    assert preview["human_review_required"] is True
    assert preview["canonical_truth_change_allowed"] is False
    assert preview["auto_resolution_allowed"] is False
