from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_effective_date_precedence_matrix


def test_effective_date_precedence_models_smoke() -> None:
    matrix = build_effective_date_precedence_matrix()

    assert matrix.matrix_ready is True
    assert len(matrix.entries) >= 3
    assert matrix.source_version_required is True
    assert matrix.effective_date_required is True
    assert matrix.precedence_required is True
    assert matrix.automatic_resolution_allowed is False
    assert matrix.canonical_truth_update_allowed is False
    assert matrix.runtime_mutation_allowed is False
