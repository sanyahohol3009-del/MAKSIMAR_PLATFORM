from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.payload_metrics import (
    build_payload_metrics_contract,
)


def test_payload_metrics_contract_builds() -> None:
    """Payload metrics contract should build successfully."""
    contract = build_payload_metrics_contract()

    assert contract.total_events == 3
    assert contract.data_plane_routed_events == 1
    assert contract.oversized_inline_violation_events == 0
    assert contract.warning_events == 1


def test_payload_metrics_contract_contains_expected_event_shapes() -> None:
    """Payload metrics contract should expose expected payload events."""
    contract = build_payload_metrics_contract()

    first = contract.events[0]
    last = contract.events[-1]

    assert first.shape_id == "shape_payload_event"
    assert first.event_kind == "payload_event"
    assert first.request_id == "payload_req_001"
    assert first.event_severity == "info"
    assert first.data_plane_routed is False
    assert first.alert_emitted is False

    assert last.shape_id == "shape_payload_event"
    assert last.event_kind == "payload_event"
    assert last.request_id == "payload_req_003"
    assert last.detected_payload_class == "heavy_artifact"
    assert last.route_target == "data_plane"
    assert last.binding_status == "bound_to_data_plane"
    assert last.event_severity == "warning"
    assert last.data_plane_routed is True
    assert last.alert_emitted is False


def test_payload_metrics_contract_preserves_trace_and_timestamp_requirements() -> None:
    """Payload metrics should preserve trace and timestamp requirements."""
    contract = build_payload_metrics_contract()

    second = contract.events[1]

    assert second.request_id == "payload_req_002"
    assert second.trace_id == "trace_payload_002"
    assert second.timestamp_utc == "2026-03-23T00:20:02Z"
    assert second.detected_payload_class == "medium_contract"
    assert second.route_target == "control_plane"
    assert second.binding_status == "inline_control_route"
