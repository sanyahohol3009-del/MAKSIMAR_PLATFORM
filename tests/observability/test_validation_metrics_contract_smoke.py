from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.validation_metrics import (
    build_validation_metrics_contract,
)


def test_validation_metrics_contract_builds() -> None:
    """Validation metrics contract should build successfully."""
    contract = build_validation_metrics_contract()

    assert contract.total_events == 4
    assert contract.passed_events == 3
    assert contract.rejected_events == 1


def test_validation_metrics_contract_contains_expected_event_shapes() -> None:
    """Validation metrics contract should expose expected validation events."""
    contract = build_validation_metrics_contract()

    first = contract.events[0]
    last = contract.events[-1]

    assert first.shape_id == "shape_validation_event"
    assert first.event_kind == "validation_event"
    assert first.request_id == "val_req_001"
    assert first.event_severity == "info"
    assert first.alert_emitted is False

    assert last.shape_id == "shape_validation_event"
    assert last.event_kind == "validation_event"
    assert last.request_id == "val_req_004"
    assert last.final_status == "rejected"
    assert last.blocking_error_code == "deep_validation_failed"
    assert last.event_severity == "critical"
    assert last.alert_emitted is True


def test_validation_metrics_contract_preserves_trace_and_timestamp_requirements() -> None:
    """Validation metrics should preserve trace and timestamp requirements."""
    contract = build_validation_metrics_contract()

    third = contract.events[2]

    assert third.request_id == "val_req_003"
    assert third.trace_id == "trace_validation_003"
    assert third.timestamp_utc == "2026-03-23T00:00:03Z"
    assert third.resolved_validation_tier == "L3_DEEP"
    assert third.event_severity == "warning"
