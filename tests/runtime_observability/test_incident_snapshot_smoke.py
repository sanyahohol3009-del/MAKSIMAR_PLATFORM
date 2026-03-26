from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_platform_incident_snapshot,
    build_runtime_snapshot,
)


def test_platform_incident_snapshot_builds() -> None:
    """Platform incident snapshot should build successfully."""
    snapshot = build_runtime_snapshot()
    incident = build_platform_incident_snapshot(snapshot)

    assert incident.overall_status == "ok"
    assert incident.total_incident_signals == 4
    assert incident.failed_signals == 0
    assert len(incident.records) == 4


def test_platform_incident_snapshot_contains_health_signal() -> None:
    """Platform incident snapshot should contain health_failed_domains signal."""
    snapshot = build_runtime_snapshot()
    incident = build_platform_incident_snapshot(snapshot)

    assert any(record.incident_name == "health_failed_domains" for record in incident.records)
    assert any(record.incident_name == "self_check_total_items" for record in incident.records)
