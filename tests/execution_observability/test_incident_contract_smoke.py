from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_incident_contract,
)


def test_execution_incident_contract_builds() -> None:
    contract = build_execution_incident_contract()

    assert contract.total_incidents == 3
    assert len(contract.incidents) == 3


def test_execution_incident_contract_contains_severities() -> None:
    contract = build_execution_incident_contract()

    severities = {incident.severity for incident in contract.incidents}

    assert "info" in severities
    assert "warning" in severities
    assert "critical" in severities
