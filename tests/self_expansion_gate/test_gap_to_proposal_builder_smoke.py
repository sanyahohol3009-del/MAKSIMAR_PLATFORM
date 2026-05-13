from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_gap_to_proposal_context


def test_gap_to_proposal_builder_smoke() -> None:
    context = build_gap_to_proposal_context()

    assert context["gap_to_proposal_ready"] is True
    assert context["missing_surfaces"] == ()
    assert context["proposal_package_allowed"] is True
    assert context["auto_resolution_allowed"] is False
    assert context["canonical_truth_change_allowed"] is False
    assert context["direct_core_write_allowed"] is False
