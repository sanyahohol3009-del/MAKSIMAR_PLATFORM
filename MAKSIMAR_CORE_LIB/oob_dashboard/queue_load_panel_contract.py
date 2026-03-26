from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_metrics_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.queue_load_panel_models import (
    QueueLoadPanelContract,
    QueueLoadPanelEntry,
)


def build_queue_load_panel_contract() -> QueueLoadPanelContract:
    """Build unified read-only queue/load panel contract."""
    metrics_contract = build_execution_metrics_contract()

    entries = tuple(
        QueueLoadPanelEntry(
            metric_name=metric.metric_name,
            metric_value=metric.metric_value,
            metric_unit=metric.metric_unit,
        )
        for metric in metrics_contract.metrics
    )

    return QueueLoadPanelContract(
        panel_id="panel_queue_load",
        total_entries=len(entries),
        entries=entries,
    )
