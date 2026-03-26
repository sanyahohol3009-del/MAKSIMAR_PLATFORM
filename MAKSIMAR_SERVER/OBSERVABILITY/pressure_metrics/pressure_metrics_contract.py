from __future__ import annotations

from MAKSIMAR_CORE_LIB.observability_contracts import (
    build_observability_shapes_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.pressure_metrics.pressure_metrics_models import (
    PressureMetricEntry,
    PressureMetricsContract,
)
from MAKSIMAR_SERVER.RUNTIME.pressure_state import (
    build_pressure_state_runtime_contract,
)


def _resolve_event_severity(*, pressure_level: str) -> str:
    """Resolve pressure event severity."""
    if pressure_level == "critical":
        return "critical"
    if pressure_level in ("elevated", "high"):
        return "warning"
    return "info"


def build_pressure_metrics_contract() -> PressureMetricsContract:
    """Build server-side pressure metrics contract."""
    shapes_contract = build_observability_shapes_contract()
    pressure_state = build_pressure_state_runtime_contract()

    shape_by_kind = {
        entry.event_kind: entry for entry in shapes_contract.shapes
    }
    pressure_shape = shape_by_kind["pressure_event"]

    events = []
    for index, state_entry in enumerate(pressure_state.entries, start=1):
        event_severity = _resolve_event_severity(
            pressure_level=state_entry.pressure_level,
        )
        alert_emitted = state_entry.pressure_level in ("elevated", "high", "critical")

        events.append(
            PressureMetricEntry(
                shape_id=pressure_shape.shape_id,
                event_kind=pressure_shape.event_kind,
                node_id=state_entry.node_id,
                trace_id=f"trace_pressure_{index:03d}",
                timestamp_utc=f"2026-03-23T00:10:0{index}Z",
                pressure_level=state_entry.pressure_level,
                runtime_state=state_entry.runtime_state,
                primary_signal_kind=state_entry.primary_signal_kind,
                primary_signal_value=state_entry.primary_signal_value,
                event_severity=event_severity,  # type: ignore[arg-type]
                degraded_mode_active=state_entry.degraded_mode_active,
                overload_protection_active=state_entry.overload_protection_active,
                alert_emitted=alert_emitted,
                description=(
                    f"Pressure observability event for node_id={state_entry.node_id} "
                    f"at pressure_level={state_entry.pressure_level}."
                ),
            )
        )

    elevated_or_higher_events = sum(
        1
        for entry in events
        if entry.pressure_level in ("elevated", "high", "critical")
    )
    alerting_events = sum(1 for entry in events if entry.alert_emitted)

    return PressureMetricsContract(
        total_events=len(events),
        elevated_or_higher_events=elevated_or_higher_events,
        alerting_events=alerting_events,
        events=tuple(events),
    )
