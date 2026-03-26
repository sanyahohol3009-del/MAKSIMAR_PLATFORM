from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_runtime_metrics,
    build_runtime_snapshot,
)


def test_runtime_snapshot_builds() -> None:
    """Runtime snapshot should build successfully."""
    snapshot = build_runtime_snapshot()

    assert snapshot.health_total_domains == 13
    assert snapshot.health_loaded_domains == 13
    assert snapshot.health_failed_domains == 0
    assert snapshot.self_check_total_items >= 1


def test_runtime_metrics_build() -> None:
    """Runtime metrics list should build successfully."""
    snapshot = build_runtime_snapshot()
    metrics = build_runtime_metrics(snapshot)

    assert len(metrics) == 6
    assert any(metric.metric_name == "runtime_documents" for metric in metrics)
    assert any(metric.metric_name == "self_check_total_items" for metric in metrics)
