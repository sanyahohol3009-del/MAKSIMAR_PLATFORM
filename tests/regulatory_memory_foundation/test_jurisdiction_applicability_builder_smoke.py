from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_jurisdiction_applicability_preview


def test_jurisdiction_applicability_builder_smoke() -> None:
    preview = build_jurisdiction_applicability_preview()

    assert preview["preview_ready"] is True
    assert preview["jurisdiction_count"] >= 5
    assert preview["applicability_pair_count"] >= 5
    assert preview["applicability_scope_required"] is True
    assert preview["source_bound_required"] is True
    assert preview["effective_date_required"] is True
    assert preview["cross_jurisdiction_merge_allowed"] is False
