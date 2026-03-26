from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.summary_contract import (
    build_execution_summary,
)
from MAKSIMAR_CORE_LIB.execution_observability.alert_models import (
    ExecutionAlert,
    ExecutionAlertContract,
)


def build_execution_alert_contract() -> ExecutionAlertContract:
    """Build execution alert semantics contract."""
    summary = build_execution_summary()

    alerts = (
        ExecutionAlert(
            alert_name="system_health",
            alert_level="info",
            triggered=summary.overall_status != "ok",
        ),
        ExecutionAlert(
            alert_name="queue_pressure",
            alert_level="warning",
            triggered=False,
        ),
        ExecutionAlert(
            alert_name="execution_failure",
            alert_level="critical",
            triggered=False,
        ),
    )

    return ExecutionAlertContract(
        total_alerts=len(alerts),
        alerts=alerts,
    )
