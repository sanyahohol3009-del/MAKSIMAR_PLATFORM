from __future__ import annotations

from MAKSIMAR_CORE_LIB.source_of_truth import (
    build_unified_consistency_report,
)


def test_unified_consistency_report_build() -> None:
    """Unified consistency report should build correctly."""
    report = build_unified_consistency_report()

    assert report.total_checks >= 1
    assert report.total_lines >= 1
    assert isinstance(report.overall_consistent, bool)
