from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_legal_precedence_resolver_preview


def test_legal_precedence_resolver_smoke() -> None:
    preview = build_legal_precedence_resolver_preview()

    assert preview["preview_ready"] is True
    assert preview["source_count"] >= 3
    assert preview["precedence_entry_count"] >= 3
    assert preview["source_version_required"] is True
    assert preview["effective_date_required"] is True
    assert preview["precedence_required"] is True
    assert preview["human_review_required"] is True
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
