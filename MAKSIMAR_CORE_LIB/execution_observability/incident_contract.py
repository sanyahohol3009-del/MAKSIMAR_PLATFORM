from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.incident_models import (
    ExecutionIncident,
    ExecutionIncidentContract,
)
from MAKSIMAR_CORE_LIB.execution_observability.summary_contract import (
    build_execution_summary,
)


def build_execution_incident_contract() -> ExecutionIncidentContract:
    """Build unified execution incident contract."""
    summary = build_execution_summary()

    incidents = (
        ExecutionIncident(
            incident_name="queue_pressure_incident",
            severity="warning",
            active=summary.overall_status != "ok",
        ),
        ExecutionIncident(
            incident_name="lease_conflict_incident",
            severity="critical",
            active=False,
        ),
        ExecutionIncident(
            incident_name="scheduler_state_incident",
            severity="info",
            active=False,
        ),
    )

    return ExecutionIncidentContract(
        total_incidents=len(incidents),
        incidents=incidents,
    )
