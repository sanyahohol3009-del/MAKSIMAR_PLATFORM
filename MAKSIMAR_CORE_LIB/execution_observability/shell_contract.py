from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.alert_contract import (
    build_execution_alert_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.incident_contract import (
    build_execution_incident_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.metrics_contract import (
    build_execution_metrics_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.shell_models import (
    ExecutionObservabilityShellContract,
)
from MAKSIMAR_CORE_LIB.execution_observability.summary_contract import (
    build_execution_summary,
)
from MAKSIMAR_CORE_LIB.execution_observability.trace_contract import (
    build_execution_trace_contract,
)


def build_execution_observability_shell_contract() -> ExecutionObservabilityShellContract:
    """Build final execution observability shell contract."""
    metrics_contract = build_execution_metrics_contract()
    summary = build_execution_summary()
    alert_contract = build_execution_alert_contract()
    incident_contract = build_execution_incident_contract()
    trace_contract = build_execution_trace_contract()

    overall_status = "ok"
    if any(alert.triggered for alert in alert_contract.alerts):
        overall_status = "warning"
    if any(incident.active and incident.severity == "critical" for incident in incident_contract.incidents):
        overall_status = "critical"

    return ExecutionObservabilityShellContract(
        shell_id="execution_observability_shell",
        total_metrics=metrics_contract.total_metrics,
        total_summary_lines=summary.total_lines,
        total_alerts=alert_contract.total_alerts,
        total_incidents=incident_contract.total_incidents,
        total_traces=trace_contract.total_traces,
        overall_status=overall_status,
    )
