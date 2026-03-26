from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.extended_summary_contract import (
    build_extended_observability_summary,
)
from MAKSIMAR_CORE_LIB.runtime_observability.visual_panel_models import (
    RuntimeObservabilityVisualPanel,
    VisualPanelMetric,
)


def _resolve_severity(metric_name: str, metric_value: int) -> str:
    """Resolve visual severity for one metric."""
    if metric_name == "failed_domains" and metric_value > 0:
        return "warning"
    return "ok"


def build_runtime_observability_visual_panel() -> RuntimeObservabilityVisualPanel:
    """Build visual-ready runtime observability panel contract."""
    summary = build_extended_observability_summary()

    metrics = tuple(
        VisualPanelMetric(
            metric_name=line.metric_name,
            metric_value=line.metric_value,
            metric_unit=line.metric_unit,
            severity=_resolve_severity(line.metric_name, line.metric_value),
        )
        for line in summary.lines
    )

    return RuntimeObservabilityVisualPanel(
        panel_id="panel_runtime_observability",
        overall_status=summary.overall_status,
        total_metrics=len(metrics),
        metrics=metrics,
    )
