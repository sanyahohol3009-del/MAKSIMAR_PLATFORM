from __future__ import annotations

from MAKSIMAR_CORE_LIB.observability_contracts import (
    build_observability_shapes_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.payload_classification import (
    build_server_payload_classification_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_artifact_routing_binding_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.payload_metrics.payload_metrics_models import (
    PayloadMetricEntry,
    PayloadMetricsContract,
)


def _resolve_event_severity(
    *,
    binding_status: str,
    route_target: str,
) -> str:
    """Resolve payload event severity."""
    if binding_status in ("bound_to_data_plane", "rejected"):
        return "warning"
    if route_target == "data_plane":
        return "warning"
    return "info"


def build_payload_metrics_contract() -> PayloadMetricsContract:
    """Build server-side payload metrics contract."""
    shapes_contract = build_observability_shapes_contract()
    payload_classification = build_server_payload_classification_contract()
    artifact_routing = build_artifact_routing_binding_contract()

    shape_by_kind = {
        entry.event_kind: entry for entry in shapes_contract.shapes
    }
    payload_shape = shape_by_kind["payload_event"]

    classification_by_request = {
        entry.request_id: entry for entry in payload_classification.entries
    }

    node_map = {
        "payload_req_001": "mobile_001",
        "payload_req_002": "dev_001",
        "payload_req_003": "home_001",
    }

    events = []
    for index, routing_entry in enumerate(artifact_routing.entries, start=1):
        classification_entry = classification_by_request[routing_entry.request_id]

        oversized_inline_violation = (
            routing_entry.binding_status == "rejected"
            and classification_entry.route_target == "control_plane"
        )
        data_plane_routed = routing_entry.binding_status == "bound_to_data_plane"
        event_severity = _resolve_event_severity(
            binding_status=routing_entry.binding_status,
            route_target=routing_entry.route_target,
        )

        events.append(
            PayloadMetricEntry(
                shape_id=payload_shape.shape_id,
                event_kind=payload_shape.event_kind,
                request_id=routing_entry.request_id,
                node_id=node_map[routing_entry.request_id],  # type: ignore[arg-type]
                trace_id=f"trace_payload_{index:03d}",
                timestamp_utc=f"2026-03-23T00:20:0{index}Z",
                detected_payload_class=routing_entry.detected_payload_class,
                route_target=routing_entry.route_target,
                binding_status=routing_entry.binding_status,
                event_severity=event_severity,  # type: ignore[arg-type]
                data_plane_routed=data_plane_routed,
                oversized_inline_violation=oversized_inline_violation,
                alert_emitted=False,
                description=(
                    f"Payload observability event for request_id={routing_entry.request_id} "
                    f"with binding_status={routing_entry.binding_status}."
                ),
            )
        )

    data_plane_routed_events = sum(1 for entry in events if entry.data_plane_routed)
    oversized_inline_violation_events = sum(
        1 for entry in events if entry.oversized_inline_violation
    )
    warning_events = sum(1 for entry in events if entry.event_severity == "warning")

    return PayloadMetricsContract(
        total_events=len(events),
        data_plane_routed_events=data_plane_routed_events,
        oversized_inline_violation_events=oversized_inline_violation_events,
        warning_events=warning_events,
        events=tuple(events),
    )
