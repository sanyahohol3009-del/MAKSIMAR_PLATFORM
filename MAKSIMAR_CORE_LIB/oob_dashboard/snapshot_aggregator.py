from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_models import (
    DashboardStateLine,
    DashboardStateSnapshot,
)
from MAKSIMAR_CORE_LIB.platform_integration import run_platform_self_check
from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_platform_incident_snapshot,
    build_runtime_observability_summary,
    build_runtime_metrics,
    build_runtime_snapshot,
    evaluate_alert_policy,
)


def build_dashboard_state_snapshot() -> DashboardStateSnapshot:
    """Build unified read-only dashboard snapshot."""
    runtime_snapshot = build_runtime_snapshot()
    runtime_metrics = build_runtime_metrics(runtime_snapshot)
    observability_summary = build_runtime_observability_summary(
        runtime_snapshot,
        runtime_metrics,
    )
    incident_snapshot = build_platform_incident_snapshot(runtime_snapshot)
    alert_policy = evaluate_alert_policy(incident_snapshot)
    self_check = run_platform_self_check()

    lines = [
        DashboardStateLine(
            source_name="platform_self_check",
            status=self_check.overall_status,
            detail_value=self_check.total_items,
        ),
        DashboardStateLine(
            source_name="runtime_observability",
            status=observability_summary.overall_status,
            detail_value=observability_summary.total_metrics,
        ),
        DashboardStateLine(
            source_name="incident_snapshot",
            status=incident_snapshot.overall_status,
            detail_value=incident_snapshot.total_incident_signals,
        ),
        DashboardStateLine(
            source_name="alert_policy",
            status=alert_policy.overall_level,
            detail_value=alert_policy.total_signals,
        ),
    ]

    status_values = {line.status for line in lines}
    if "critical" in status_values or "failed" in status_values:
        overall_status = "critical"
    elif "warning" in status_values:
        overall_status = "warning"
    else:
        overall_status = "ok"

    return DashboardStateSnapshot(
        overall_status=overall_status,
        total_lines=len(lines),
        lines=lines,
    )
