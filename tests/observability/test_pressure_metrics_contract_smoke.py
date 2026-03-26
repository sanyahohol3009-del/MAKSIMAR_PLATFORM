from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.pressure_metrics import (
    build_pressure_metrics_contract,
)


def test_pressure_metrics_contract_builds() -> None:
    """Pressure metrics contract should build successfully."""
    contract = build_pressure_metrics_contract()

    assert contract.total_events == 3
    assert contract.elevated_or_higher_events == 1
    assert contract.alerting_events == 1


def test_pressure_metrics_contract_contains_expected_event_shapes() -> None:
    """Pressure metrics contract should expose expected pressure events."""
    contract = build_pressure_metrics_contract()

    first = contract.events[0]
    last = contract.events[-1]

    assert first.shape_id == "shape_pressure_event"
    assert first.event_kind == "pressure_event"
    assert first.node_id == "mobile_001"
    assert first.event_severity == "info"
    assert first.alert_emitted is False

    assert last.shape_id == "shape_pressure_event"
    assert last.event_kind == "pressure_event"
    assert last.node_id == "home_001"
    assert last.pressure_level == "elevated"
    assert last.runtime_state == "throttled"
    assert last.event_severity == "warning"
    assert last.alert_emitted is True


def test_pressure_metrics_contract_preserves_trace_and_timestamp_requirements() -> None:
    """Pressure metrics should preserve trace and timestamp requirements."""
    contract = build_pressure_metrics_contract()

    second = contract.events[1]

    assert second.node_id == "dev_001"
    assert second.trace_id == "trace_pressure_002"
    assert second.timestamp_utc == "2026-03-23T00:10:02Z"
    assert second.pressure_level == "normal"
    assert second.runtime_state == "open"
