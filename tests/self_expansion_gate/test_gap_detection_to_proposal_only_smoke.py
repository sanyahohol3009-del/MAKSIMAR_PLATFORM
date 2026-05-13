from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_gap_to_proposal_context


def test_gap_detection_to_proposal_only_smoke() -> None:
    context = build_gap_to_proposal_context()

    assert context["gap_to_proposal_ready"] is True
    assert context["human_review_required"] is True
    assert context["proposal_package_allowed"] is True
    assert context["auto_apply_allowed"] is False
    assert context["runtime_mutation_allowed"] is False
