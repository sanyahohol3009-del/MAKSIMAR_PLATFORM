from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration import run_platform_self_check
from MAKSIMAR_CORE_LIB.runtime_observability.extended_metrics_models import (
    ExtendedRuntimeMetric,
    ExtendedRuntimeMetricsContract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.snapshot_loader import (
    build_runtime_snapshot,
)


def build_extended_runtime_metrics_contract() -> ExtendedRuntimeMetricsContract:
    """Build extended runtime metrics contract."""
    snapshot = build_runtime_snapshot()
    self_check = run_platform_self_check()

    metrics = (
        ExtendedRuntimeMetric(
            metric_name="health_depth",
            metric_value=snapshot.health_total_domains,
            metric_unit="domains",
        ),
        ExtendedRuntimeMetric(
            metric_name="failed_domains",
            metric_value=snapshot.health_failed_domains,
            metric_unit="domains",
        ),
        ExtendedRuntimeMetric(
            metric_name="self_check_items",
            metric_value=self_check.total_items,
            metric_unit="items",
        ),
        ExtendedRuntimeMetric(
            metric_name="runtime_documents",
            metric_value=snapshot.runtime_documents,
            metric_unit="documents",
        ),
        ExtendedRuntimeMetric(
            metric_name="event_records",
            metric_value=snapshot.event_records,
            metric_unit="records",
        ),
    )

    return ExtendedRuntimeMetricsContract(
        total_metrics=len(metrics),
        metrics=metrics,
    )
