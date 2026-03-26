from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_alert_contract,
)


def test_execution_alert_contract_builds() -> None:
    contract = build_execution_alert_contract()

    assert contract.total_alerts == 3
    assert len(contract.alerts) == 3


def test_execution_alert_contract_contains_levels() -> None:
    contract = build_execution_alert_contract()

    levels = {a.alert_level for a in contract.alerts}

    assert "info" in levels
    assert "warning" in levels
    assert "critical" in levels
