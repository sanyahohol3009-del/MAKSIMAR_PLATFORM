from __future__ import annotations

from MAKSIMAR_CORE_LIB.observability_contracts import (
    build_observability_shapes_contract,
)
from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_error_entry,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate import (
    build_server_validation_gate_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.validation_metrics.validation_metrics_models import (
    ValidationMetricEntry,
    ValidationMetricsContract,
)


def _resolve_event_severity(
    *,
    final_status: str,
    blocking_error_code: str,
    resolved_validation_tier: str,
) -> str:
    """Resolve validation event severity."""
    if final_status == "rejected":
        if blocking_error_code in ("deep_validation_failed", "policy_rule_not_found"):
            return "critical"
        return "warning"

    if resolved_validation_tier == "L3_DEEP":
        return "warning"

    return "info"


def build_validation_metrics_contract() -> ValidationMetricsContract:
    """Build server-side validation metrics contract."""
    shapes_contract = build_observability_shapes_contract()
    validation_gate = build_server_validation_gate_contract()

    shape_by_kind = {
        entry.event_kind: entry for entry in shapes_contract.shapes
    }
    validation_shape = shape_by_kind["validation_event"]

    node_map = {
        "val_req_001": "mobile_001",
        "val_req_002": "home_001",
        "val_req_003": "home_001",
        "val_req_004": "dev_001",
    }

    events = []
    for index, gate_entry in enumerate(validation_gate.entries, start=1):
        if gate_entry.final_status == "rejected":
            build_validation_error_entry(
                error_code=gate_entry.blocking_error_code,  # type: ignore[arg-type]
            )

        event_severity = _resolve_event_severity(
            final_status=gate_entry.final_status,
            blocking_error_code=gate_entry.blocking_error_code,
            resolved_validation_tier=gate_entry.resolved_validation_tier,
        )

        rejection_event = gate_entry.final_status == "rejected"
        alert_emitted = (
            validation_shape.supports_alerting and rejection_event
        )

        events.append(
            ValidationMetricEntry(
                shape_id=validation_shape.shape_id,
                event_kind=validation_shape.event_kind,
                request_id=gate_entry.request_id,
                node_id=node_map[gate_entry.request_id],  # type: ignore[arg-type]
                trace_id=f"trace_validation_{index:03d}",
                timestamp_utc=f"2026-03-23T00:00:0{index}Z",
                resolved_validation_tier=gate_entry.resolved_validation_tier,
                final_status=gate_entry.final_status,
                blocking_error_code=gate_entry.blocking_error_code,
                event_severity=event_severity,  # type: ignore[arg-type]
                rejection_event=rejection_event,
                alert_emitted=alert_emitted,
                description=(
                    f"Validation observability event for request_id={gate_entry.request_id} "
                    f"at tier={gate_entry.resolved_validation_tier}."
                ),
            )
        )

    passed_events = sum(1 for entry in events if entry.final_status == "passed")
    rejected_events = sum(1 for entry in events if entry.final_status == "rejected")

    return ValidationMetricsContract(
        total_events=len(events),
        passed_events=passed_events,
        rejected_events=rejected_events,
        events=tuple(events),
    )
