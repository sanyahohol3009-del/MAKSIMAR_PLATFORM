from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import (
    build_evaluation_registry_summary,
)


def test_evaluation_registry_summary_builds() -> None:
    """Evaluation registry summary should build successfully."""
    summary = build_evaluation_registry_summary()

    assert summary.total_evaluations >= 1
    assert len(summary.records) == summary.total_evaluations


def test_evaluation_registry_summary_contains_codegen_eval() -> None:
    """Evaluation registry summary should contain codegen_eval."""
    summary = build_evaluation_registry_summary()

    assert any(
        record.evaluation_id == "codegen_eval"
        for record in summary.records
    )
