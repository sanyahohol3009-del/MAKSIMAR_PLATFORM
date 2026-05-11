from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_contradiction_candidate_sample


def test_memory_contradiction_candidate_models_smoke() -> None:
    candidate = build_memory_contradiction_candidate_sample()

    assert candidate.candidate_ready is True
    assert candidate.status == "candidate_only"
    assert candidate.human_review_required is True
    assert candidate.auto_resolution_allowed is False
    assert candidate.canonical_truth_change_allowed is False
