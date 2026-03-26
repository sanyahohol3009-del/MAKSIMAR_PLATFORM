from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_extended_observability_summary,
)


def test_extended_summary_contract_builds() -> None:
    """Extended observability summary should build successfully."""
    summary = build_extended_observability_summary()

    assert summary.total_lines == 5
    assert len(summary.lines) == 5


def test_extended_summary_contains_failed_domains() -> None:
    """Extended observability summary should contain failed_domains metric."""
    summary = build_extended_observability_summary()

    metric_names = {line.metric_name for line in summary.lines}

    assert "failed_domains" in metric_names
    assert summary.overall_status in {"ok", "warning"}
