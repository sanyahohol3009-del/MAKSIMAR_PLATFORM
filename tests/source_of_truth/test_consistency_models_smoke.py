from __future__ import annotations

from MAKSIMAR_CORE_LIB.source_of_truth import (
    ConsistencyCheckLine,
    ConsistencyCheckResult,
)


def test_consistency_models_build() -> None:
    """Consistency models should build successfully."""
    line = ConsistencyCheckLine(
        check_name="snapshot_vs_metrics",
        expected_value=4,
        actual_value=4,
        consistent=True,
    )

    result = ConsistencyCheckResult(
        check_scope="runtime_observability",
        overall_consistent=True,
        total_lines=1,
        lines=[line],
    )

    assert result.check_scope == "runtime_observability"
    assert result.overall_consistent is True
    assert result.total_lines == 1
    assert result.lines[0].check_name == "snapshot_vs_metrics"
