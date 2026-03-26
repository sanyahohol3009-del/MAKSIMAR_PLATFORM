from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.execution_views.execution_views_models import (
    ExecutionViewEntry,
    ExecutionViewsContract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.payload_metrics import (
    build_payload_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.pressure_metrics import (
    build_pressure_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.validation_metrics import (
    build_validation_metrics_contract,
)


def build_execution_views_contract() -> ExecutionViewsContract:
    """Build read-only execution views contract."""
    validation_metrics = build_validation_metrics_contract()
    pressure_metrics = build_pressure_metrics_contract()
    payload_metrics = build_payload_metrics_contract()

    validation_warning_events = sum(
        1 for entry in validation_metrics.events if entry.event_severity == "warning"
    )
    validation_critical_events = sum(
        1 for entry in validation_metrics.events if entry.event_severity == "critical"
    )

    pressure_warning_events = sum(
        1 for entry in pressure_metrics.events if entry.event_severity == "warning"
    )
    pressure_critical_events = sum(
        1 for entry in pressure_metrics.events if entry.event_severity == "critical"
    )

    payload_warning_events = sum(
        1 for entry in payload_metrics.events if entry.event_severity == "warning"
    )
    payload_critical_events = sum(
        1 for entry in payload_metrics.events if entry.event_severity == "critical"
    )

    views = (
        ExecutionViewEntry(
            view_id="view_validation_overview",
            view_kind="validation_overview",
            source_metric="validation_metrics",
            total_events=validation_metrics.total_events,
            warning_events=validation_warning_events,
            critical_events=validation_critical_events,
            alerting_events=validation_metrics.rejected_events,
            read_only=True,
            description="Read-only validation overview derived from validation metrics.",
        ),
        ExecutionViewEntry(
            view_id="view_pressure_overview",
            view_kind="pressure_overview",
            source_metric="pressure_metrics",
            total_events=pressure_metrics.total_events,
            warning_events=pressure_warning_events,
            critical_events=pressure_critical_events,
            alerting_events=pressure_metrics.alerting_events,
            read_only=True,
            description="Read-only pressure overview derived from pressure metrics.",
        ),
        ExecutionViewEntry(
            view_id="view_payload_overview",
            view_kind="payload_overview",
            source_metric="payload_metrics",
            total_events=payload_metrics.total_events,
            warning_events=payload_warning_events,
            critical_events=payload_critical_events,
            alerting_events=0,
            read_only=True,
            description="Read-only payload overview derived from payload metrics.",
        ),
    )

    aggregated_total_events = sum(entry.total_events for entry in views)
    aggregated_warning_events = sum(entry.warning_events for entry in views)
    aggregated_critical_events = sum(entry.critical_events for entry in views)
    aggregated_alerting_events = sum(entry.alerting_events for entry in views)

    return ExecutionViewsContract(
        total_views=len(views),
        aggregated_total_events=aggregated_total_events,
        aggregated_warning_events=aggregated_warning_events,
        aggregated_critical_events=aggregated_critical_events,
        aggregated_alerting_events=aggregated_alerting_events,
        views=views,
    )
