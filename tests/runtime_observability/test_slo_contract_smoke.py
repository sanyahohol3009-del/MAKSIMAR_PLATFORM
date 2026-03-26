from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_slo_alert_semantics_contract,
)


def test_slo_contract_builds() -> None:
    """SLO / alert semantics contract should build successfully."""
    contract = build_slo_alert_semantics_contract()

    assert contract.total_indicators == 3
    assert len(contract.indicators) == 3


def test_slo_contract_contains_critical_indicator() -> None:
    """SLO contract should contain critical indicator."""
    contract = build_slo_alert_semantics_contract()

    levels = {indicator.alert_level for indicator in contract.indicators}

    assert "info" in levels
    assert "warning" in levels
    assert "critical" in levels
