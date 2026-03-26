from __future__ import annotations

from MAKSIMAR_CORE_LIB.source_of_truth import (
    build_snapshot_metrics_consistency_check,
)


def test_snapshot_metrics_consistency_build() -> None:
    """Snapshot ↔ metrics consistency check should build."""
    result = build_snapshot_metrics_consistency_check()

    assert result.check_scope == "snapshot_metrics"
    assert result.total_lines >= 1
    assert isinstance(result.overall_consistent, bool)
