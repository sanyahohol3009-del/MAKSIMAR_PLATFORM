from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_release_candidate


def test_memory_release_candidate_builder_smoke() -> None:
    candidate = build_memory_release_candidate()

    assert candidate["release_candidate_ready"] is True
    assert candidate["release_type"] == "memory_product_ready_candidate"
    assert candidate["release_allowed_without_operator_approval"] is False
    assert candidate["canonical_promotion_allowed"] is False
    assert candidate["release_preview_required"] is True
    assert candidate["rollback_reference_required"] is True
