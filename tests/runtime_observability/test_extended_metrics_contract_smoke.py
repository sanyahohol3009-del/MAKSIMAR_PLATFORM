from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_extended_runtime_metrics_contract,
)


def test_extended_metrics_contract_builds() -> None:
    """Extended metrics contract should build successfully."""
    contract = build_extended_runtime_metrics_contract()

    assert contract.total_metrics == 5
    assert len(contract.metrics) == 5


def test_extended_metrics_contains_health_depth() -> None:
    """Extended metrics contract should contain health_depth metric."""
    contract = build_extended_runtime_metrics_contract()

    metric_names = {metric.metric_name for metric in contract.metrics}

    assert "health_depth" in metric_names
    assert "failed_domains" in metric_names
