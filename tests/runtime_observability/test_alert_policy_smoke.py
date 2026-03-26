from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_platform_incident_snapshot,
    build_runtime_snapshot,
    evaluate_alert_policy,
)


def test_alert_policy_builds() -> None:
    """Alert policy evaluation should build successfully."""
    snapshot = build_runtime_snapshot()
    incident = build_platform_incident_snapshot(snapshot)
    result = evaluate_alert_policy(incident)

    assert result.overall_level == "info"
    assert result.total_signals == 4
    assert result.critical_signals == 0
    assert result.warning_signals == 0
    assert result.info_signals == 4


def test_alert_policy_contains_health_signal() -> None:
    """Alert policy result should contain health_failed_domains signal."""
    snapshot = build_runtime_snapshot()
    incident = build_platform_incident_snapshot(snapshot)
    result = evaluate_alert_policy(incident)

    assert any(signal.incident_name == "health_failed_domains" for signal in result.signals)
    assert any(signal.incident_name == "self_check_total_items" for signal in result.signals)
