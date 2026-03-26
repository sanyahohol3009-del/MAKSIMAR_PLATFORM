from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.incident_models import (
    PlatformIncidentRecord,
    PlatformIncidentSnapshot,
)
from MAKSIMAR_CORE_LIB.runtime_observability.metrics_models import RuntimeSnapshot


def build_platform_incident_snapshot(
    snapshot: RuntimeSnapshot,
) -> PlatformIncidentSnapshot:
    """Build unified platform incident snapshot from runtime snapshot."""
    records = [
        PlatformIncidentRecord(
            incident_name="health_failed_domains",
            incident_value=snapshot.health_failed_domains,
            status="ok" if snapshot.health_failed_domains == 0 else "failed",
        ),
        PlatformIncidentRecord(
            incident_name="runtime_documents",
            incident_value=snapshot.runtime_documents,
            status="ok" if snapshot.runtime_documents >= 0 else "failed",
        ),
        PlatformIncidentRecord(
            incident_name="event_records",
            incident_value=snapshot.event_records,
            status="ok" if snapshot.event_records >= 0 else "failed",
        ),
        PlatformIncidentRecord(
            incident_name="self_check_total_items",
            incident_value=snapshot.self_check_total_items,
            status="ok" if snapshot.self_check_total_items > 0 else "failed",
        ),
    ]

    failed_signals = sum(1 for record in records if record.status != "ok")
    overall_status = "ok" if failed_signals == 0 else "failed"

    return PlatformIncidentSnapshot(
        overall_status=overall_status,
        total_incident_signals=len(records),
        failed_signals=failed_signals,
        records=records,
    )
