from __future__ import annotations

from MAKSIMAR_CORE_LIB.event_bus import read_event_journal
from MAKSIMAR_CORE_LIB.platform_integration import (
    build_platform_bootstrap_context,
    build_platform_health_snapshot,
    run_platform_self_check,
)
from MAKSIMAR_CORE_LIB.runtime_base import list_runtime_documents
from MAKSIMAR_CORE_LIB.runtime_observability.metrics_models import (
    RuntimeMetric,
    RuntimeSnapshot,
)


def build_runtime_snapshot() -> RuntimeSnapshot:
    """Build unified runtime observability snapshot."""
    context = build_platform_bootstrap_context()
    health = build_platform_health_snapshot(context)
    self_check = run_platform_self_check()
    runtime_documents = list_runtime_documents("project_runtime")
    event_records = read_event_journal()

    return RuntimeSnapshot(
        runtime_documents=len(runtime_documents),
        event_records=len(event_records),
        health_total_domains=health.total_domains,
        health_loaded_domains=health.loaded_domains,
        health_failed_domains=health.failed_domains,
        self_check_total_items=self_check.total_items,
    )


def build_runtime_metrics(snapshot: RuntimeSnapshot) -> list[RuntimeMetric]:
    """Convert runtime snapshot to metric list."""
    return [
        RuntimeMetric(
            metric_name="runtime_documents",
            metric_value=snapshot.runtime_documents,
            status="ok",
        ),
        RuntimeMetric(
            metric_name="event_records",
            metric_value=snapshot.event_records,
            status="ok",
        ),
        RuntimeMetric(
            metric_name="health_total_domains",
            metric_value=snapshot.health_total_domains,
            status="ok",
        ),
        RuntimeMetric(
            metric_name="health_loaded_domains",
            metric_value=snapshot.health_loaded_domains,
            status="ok",
        ),
        RuntimeMetric(
            metric_name="health_failed_domains",
            metric_value=snapshot.health_failed_domains,
            status="ok" if snapshot.health_failed_domains == 0 else "failed",
        ),
        RuntimeMetric(
            metric_name="self_check_total_items",
            metric_value=snapshot.self_check_total_items,
            status="ok",
        ),
    ]
