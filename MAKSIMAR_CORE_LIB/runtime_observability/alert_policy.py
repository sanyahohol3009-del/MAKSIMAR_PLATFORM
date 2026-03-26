from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.alert_models import (
    AlertPolicyResult,
    AlertSignal,
)
from MAKSIMAR_CORE_LIB.runtime_observability.incident_models import (
    PlatformIncidentSnapshot,
    PlatformIncidentRecord,
)


def _classify_record(record: PlatformIncidentRecord) -> AlertSignal:
    """Classify one incident record into alert signal."""
    if record.status != "ok":
        return AlertSignal(
            incident_name=record.incident_name,
            incident_value=record.incident_value,
            level="critical",
            status=record.status,
        )

    if record.incident_name == "health_failed_domains" and record.incident_value == 0:
        level = "info"
    elif record.incident_name == "self_check_total_items" and record.incident_value > 0:
        level = "info"
    else:
        level = "info"

    return AlertSignal(
        incident_name=record.incident_name,
        incident_value=record.incident_value,
        level=level,
        status=record.status,
    )


def evaluate_alert_policy(
    incident_snapshot: PlatformIncidentSnapshot,
) -> AlertPolicyResult:
    """Evaluate alert policy from incident snapshot."""
    signals = [_classify_record(record) for record in incident_snapshot.records]

    critical_signals = sum(1 for signal in signals if signal.level == "critical")
    warning_signals = sum(1 for signal in signals if signal.level == "warning")
    info_signals = sum(1 for signal in signals if signal.level == "info")

    if critical_signals > 0:
        overall_level = "critical"
    elif warning_signals > 0:
        overall_level = "warning"
    else:
        overall_level = "info"

    return AlertPolicyResult(
        overall_level=overall_level,
        total_signals=len(signals),
        critical_signals=critical_signals,
        warning_signals=warning_signals,
        info_signals=info_signals,
        signals=signals,
    )
