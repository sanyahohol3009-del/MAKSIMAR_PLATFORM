from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.execution_views import (
    build_execution_views_contract,
)


def test_execution_views_contract_builds() -> None:
    """Execution views contract should build successfully."""
    contract = build_execution_views_contract()

    assert contract.total_views == 3
    assert contract.aggregated_total_events == 10
    assert contract.aggregated_warning_events == 3
    assert contract.aggregated_critical_events == 1
    assert contract.aggregated_alerting_events == 2


def test_execution_views_contract_contains_expected_views() -> None:
    """Execution views contract should expose expected read-only views."""
    contract = build_execution_views_contract()

    first = contract.views[0]
    second = contract.views[1]
    last = contract.views[-1]

    assert first.view_id == "view_validation_overview"
    assert first.view_kind == "validation_overview"
    assert first.source_metric == "validation_metrics"
    assert first.read_only is True

    assert second.view_id == "view_pressure_overview"
    assert second.view_kind == "pressure_overview"
    assert second.source_metric == "pressure_metrics"
    assert second.read_only is True

    assert last.view_id == "view_payload_overview"
    assert last.view_kind == "payload_overview"
    assert last.source_metric == "payload_metrics"
    assert last.read_only is True


def test_execution_views_contract_preserves_expected_counts() -> None:
    """Execution views should preserve expected metric counts."""
    contract = build_execution_views_contract()

    validation = contract.views[0]
    pressure = contract.views[1]
    payload = contract.views[2]

    assert validation.total_events == 4
    assert validation.warning_events == 1
    assert validation.critical_events == 1
    assert validation.alerting_events == 1

    assert pressure.total_events == 3
    assert pressure.warning_events == 1
    assert pressure.critical_events == 0
    assert pressure.alerting_events == 1

    assert payload.total_events == 3
    assert payload.warning_events == 1
    assert payload.critical_events == 0
    assert payload.alerting_events == 0
