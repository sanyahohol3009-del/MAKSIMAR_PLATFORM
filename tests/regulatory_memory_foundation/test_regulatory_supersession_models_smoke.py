from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_supersession_preview


def test_regulatory_supersession_models_smoke() -> None:
    preview = build_regulatory_supersession_preview()

    assert preview["preview_ready"] is True
    assert preview["candidate_count"] >= 1
    assert preview["approval_required"] is True
    assert preview["human_review_required"] is True
    assert preview["supersession_applied"] is False
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
