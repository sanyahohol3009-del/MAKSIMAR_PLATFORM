from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_drift_preview


def test_regulatory_drift_detector_smoke() -> None:
    preview = build_regulatory_drift_preview()

    assert preview["preview_ready"] is True
    assert preview["signal_count"] >= 3
    assert "draft_source_pending_review" in preview["drift_kinds"]
    assert "jurisdiction_precedence_recheck_required" in preview["drift_kinds"]
    assert preview["human_review_required"] is True
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
