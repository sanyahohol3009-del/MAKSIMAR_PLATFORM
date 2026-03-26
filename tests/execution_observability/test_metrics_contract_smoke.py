from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_metrics_contract,
)


def test_execution_metrics_contract_builds() -> None:
    """Execution metrics contract should build successfully."""
    contract = build_execution_metrics_contract()

    assert contract.total_metrics == 5
    assert len(contract.metrics) == 5


def test_execution_metrics_contract_contains_routes_and_leases() -> None:
    """Execution metrics contract should expose routes and leases."""
    contract = build_execution_metrics_contract()

    metric_names = {metric.metric_name for metric in contract.metrics}

    assert "lease_count" in metric_names
    assert "execution_routes" in metric_names
