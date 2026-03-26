from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_pressure_metrics_contract,
)


def test_pressure_metrics_contract_builds() -> None:
    """Pressure metrics contract should build successfully."""
    contract = build_pressure_metrics_contract()

    assert contract.total_metrics == 3
    assert len(contract.metrics) == 3


def test_pressure_metrics_contract_contains_active_queue_pressure() -> None:
    """Pressure metrics contract should expose active queue pressure."""
    contract = build_pressure_metrics_contract()

    names = {metric.metric_name for metric in contract.metrics}
    assert "queue_pressure" in names
    assert any(metric.trigger_active for metric in contract.metrics)
