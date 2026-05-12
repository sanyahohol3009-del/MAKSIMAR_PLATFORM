from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_operator_review_package


def test_memory_operator_review_builder_smoke() -> None:
    review = build_memory_operator_review_package()

    assert review["review_ready"] is True
    assert review["operator_approval_required"] is True
    assert review["operator_approval_granted"] is False
    assert review["risk_summary_required"] is True
    assert review["diff_preview_required"] is True
    assert len(review["review_items"]) >= 6
