from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_runtime_metrics,
    build_runtime_observability_summary,
    build_runtime_snapshot,
)


def test_runtime_observability_summary_builds() -> None:
    """Runtime observability summary should build successfully."""
    snapshot = build_runtime_snapshot()
    metrics = build_runtime_metrics(snapshot)
    summary = build_runtime_observability_summary(snapshot, metrics)

    assert summary.overall_status == "ok"
    assert summary.total_metrics == 6
    assert summary.failed_metrics == 0
    assert len(summary.lines) == 6


def test_runtime_observability_summary_contains_runtime_documents() -> None:
    """Runtime observability summary should contain runtime_documents metric."""
    snapshot = build_runtime_snapshot()
    metrics = build_runtime_metrics(snapshot)
    summary = build_runtime_observability_summary(snapshot, metrics)

    assert any(line.metric_name == "runtime_documents" for line in summary.lines)
    assert any(line.metric_name == "self_check_total_items" for line in summary.lines)
