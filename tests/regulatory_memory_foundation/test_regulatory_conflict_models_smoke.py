from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_conflict_registry


def test_regulatory_conflict_models_smoke() -> None:
    registry = build_regulatory_conflict_registry()

    assert registry.conflict_detection_ready is True
    assert len(registry.candidates) >= 2
    assert registry.source_version_precedence_ready is True
    assert registry.human_review_required is True
    assert registry.automatic_resolution_allowed is False
    assert registry.canonical_truth_update_allowed is False
    assert registry.runtime_mutation_allowed is False
