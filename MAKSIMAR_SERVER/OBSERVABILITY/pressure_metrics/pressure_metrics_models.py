from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.execution_pressure import (
    PressureLevel,
    PressureSignalKind,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId
from MAKSIMAR_CORE_LIB.observability_contracts import (
    ObservabilityEventKind,
    ObservabilitySeverity,
)
from MAKSIMAR_SERVER.RUNTIME.pressure_state import (
    PressureRuntimeState,
)


@dataclass(frozen=True, slots=True)
class PressureMetricEntry:
    """Server-side pressure observability metric entry."""

    shape_id: str
    event_kind: ObservabilityEventKind
    node_id: CanonicalNodeId
    trace_id: str
    timestamp_utc: str
    pressure_level: PressureLevel
    runtime_state: PressureRuntimeState
    primary_signal_kind: PressureSignalKind
    primary_signal_value: int
    event_severity: ObservabilitySeverity
    degraded_mode_active: bool
    overload_protection_active: bool
    alert_emitted: bool
    description: str

    def __post_init__(self) -> None:
        """Validate pressure metric invariants."""
        if self.shape_id != "shape_pressure_event":
            raise ValueError(
                f"pressure metric must use shape_pressure_event: {self.node_id}"
            )

        if self.event_kind != "pressure_event":
            raise ValueError(
                f"pressure metric must use event_kind='pressure_event': {self.node_id}"
            )

        if not self.trace_id.strip():
            raise ValueError(f"trace_id must not be empty for {self.node_id}")

        if not self.timestamp_utc.strip():
            raise ValueError(f"timestamp_utc must not be empty for {self.node_id}")

        if "T" not in self.timestamp_utc:
            raise ValueError(
                f"timestamp_utc must look like ISO datetime for {self.node_id}"
            )

        if self.primary_signal_value < 0:
            raise ValueError(
                f"primary_signal_value must be non-negative for {self.node_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.node_id}")

        if self.pressure_level == "normal":
            if self.runtime_state != "open":
                raise ValueError("normal pressure metric must use runtime_state='open'")
            if self.event_severity != "info":
                raise ValueError("normal pressure metric must use severity='info'")
            if self.degraded_mode_active:
                raise ValueError("normal pressure metric must not enable degraded mode")
            if self.overload_protection_active:
                raise ValueError(
                    "normal pressure metric must not enable overload protection"
                )
            if self.alert_emitted:
                raise ValueError("normal pressure metric must not emit alert")

        if self.pressure_level == "elevated":
            if self.runtime_state != "throttled":
                raise ValueError(
                    "elevated pressure metric must use runtime_state='throttled'"
                )
            if self.event_severity != "warning":
                raise ValueError(
                    "elevated pressure metric must use severity='warning'"
                )
            if self.degraded_mode_active:
                raise ValueError(
                    "elevated pressure metric must not enable degraded mode"
                )
            if self.overload_protection_active:
                raise ValueError(
                    "elevated pressure metric must not enable overload protection"
                )
            if not self.alert_emitted:
                raise ValueError("elevated pressure metric must emit alert")

        if self.pressure_level == "high":
            if self.runtime_state != "degraded":
                raise ValueError(
                    "high pressure metric must use runtime_state='degraded'"
                )
            if self.event_severity != "warning":
                raise ValueError("high pressure metric must use severity='warning'")
            if not self.degraded_mode_active:
                raise ValueError("high pressure metric must enable degraded mode")
            if not self.overload_protection_active:
                raise ValueError(
                    "high pressure metric must enable overload protection"
                )
            if not self.alert_emitted:
                raise ValueError("high pressure metric must emit alert")

        if self.pressure_level == "critical":
            if self.runtime_state != "protected":
                raise ValueError(
                    "critical pressure metric must use runtime_state='protected'"
                )
            if self.event_severity != "critical":
                raise ValueError(
                    "critical pressure metric must use severity='critical'"
                )
            if not self.degraded_mode_active:
                raise ValueError("critical pressure metric must enable degraded mode")
            if not self.overload_protection_active:
                raise ValueError(
                    "critical pressure metric must enable overload protection"
                )
            if not self.alert_emitted:
                raise ValueError("critical pressure metric must emit alert")


@dataclass(frozen=True, slots=True)
class PressureMetricsContract:
    """Unified server-side pressure metrics contract."""

    total_events: int
    elevated_or_higher_events: int
    alerting_events: int
    events: tuple[PressureMetricEntry, ...]

    def __post_init__(self) -> None:
        """Validate pressure metrics contract invariants."""
        if self.total_events != len(self.events):
            raise ValueError("total_events must match events length")

        elevated_or_higher_events = sum(
            1
            for entry in self.events
            if entry.pressure_level in ("elevated", "high", "critical")
        )
        alerting_events = sum(1 for entry in self.events if entry.alert_emitted)

        if self.elevated_or_higher_events != elevated_or_higher_events:
            raise ValueError(
                "elevated_or_higher_events must match computed event count"
            )

        if self.alerting_events != alerting_events:
            raise ValueError("alerting_events must match computed alert count")

        node_ids = tuple(entry.node_id for entry in self.events)
        trace_ids = tuple(entry.trace_id for entry in self.events)

        if len(set(node_ids)) != len(node_ids):
            raise ValueError("Duplicate pressure metric node_ids detected")

        if len(set(trace_ids)) != len(trace_ids):
            raise ValueError("Duplicate pressure metric trace_ids detected")
