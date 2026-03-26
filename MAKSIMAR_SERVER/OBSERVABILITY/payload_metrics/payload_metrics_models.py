from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId
from MAKSIMAR_CORE_LIB.observability_contracts import (
    ObservabilityEventKind,
    ObservabilitySeverity,
)
from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
    PayloadDirection,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.artifact_routing_models import (
    ArtifactRoutingBindingStatus,
)


@dataclass(frozen=True, slots=True)
class PayloadMetricEntry:
    """Server-side payload observability metric entry."""

    shape_id: str
    event_kind: ObservabilityEventKind
    request_id: str
    node_id: CanonicalNodeId
    trace_id: str
    timestamp_utc: str
    detected_payload_class: PayloadClass
    route_target: PayloadDirection
    binding_status: ArtifactRoutingBindingStatus
    event_severity: ObservabilitySeverity
    data_plane_routed: bool
    oversized_inline_violation: bool
    alert_emitted: bool
    description: str

    def __post_init__(self) -> None:
        """Validate payload metric invariants."""
        if self.shape_id != "shape_payload_event":
            raise ValueError(
                f"payload metric must use shape_payload_event: {self.request_id}"
            )

        if self.event_kind != "payload_event":
            raise ValueError(
                f"payload metric must use event_kind='payload_event': {self.request_id}"
            )

        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")

        if not self.trace_id.strip():
            raise ValueError(f"trace_id must not be empty for {self.request_id}")

        if not self.timestamp_utc.strip():
            raise ValueError(f"timestamp_utc must not be empty for {self.request_id}")

        if "T" not in self.timestamp_utc:
            raise ValueError(
                f"timestamp_utc must look like ISO datetime for {self.request_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.request_id}")

        if self.alert_emitted:
            raise ValueError(
                f"payload metrics must not emit alerts via payload_event shape: {self.request_id}"
            )

        if self.binding_status == "inline_control_route":
            if self.route_target != "control_plane":
                raise ValueError(
                    f"inline_control_route must use control_plane: {self.request_id}"
                )
            if self.data_plane_routed:
                raise ValueError(
                    f"inline_control_route must not mark data_plane_routed: {self.request_id}"
                )
            if self.event_severity != "info":
                raise ValueError(
                    f"inline_control_route must use severity='info': {self.request_id}"
                )

        if self.binding_status == "bound_to_data_plane":
            if self.route_target != "data_plane":
                raise ValueError(
                    f"bound_to_data_plane must use data_plane: {self.request_id}"
                )
            if not self.data_plane_routed:
                raise ValueError(
                    f"bound_to_data_plane must mark data_plane_routed: {self.request_id}"
                )
            if self.event_severity != "warning":
                raise ValueError(
                    f"bound_to_data_plane must use severity='warning': {self.request_id}"
                )

        if self.binding_status == "rejected":
            if self.event_severity != "warning":
                raise ValueError(
                    f"rejected payload metric must use severity='warning': {self.request_id}"
                )
            if self.route_target == "data_plane" and self.data_plane_routed:
                raise ValueError(
                    f"rejected payload metric must not mark data_plane_routed: {self.request_id}"
                )


@dataclass(frozen=True, slots=True)
class PayloadMetricsContract:
    """Unified server-side payload metrics contract."""

    total_events: int
    data_plane_routed_events: int
    oversized_inline_violation_events: int
    warning_events: int
    events: tuple[PayloadMetricEntry, ...]

    def __post_init__(self) -> None:
        """Validate payload metrics contract invariants."""
        if self.total_events != len(self.events):
            raise ValueError("total_events must match events length")

        data_plane_routed_events = sum(
            1 for entry in self.events if entry.data_plane_routed
        )
        oversized_inline_violation_events = sum(
            1 for entry in self.events if entry.oversized_inline_violation
        )
        warning_events = sum(
            1 for entry in self.events if entry.event_severity == "warning"
        )

        if self.data_plane_routed_events != data_plane_routed_events:
            raise ValueError(
                "data_plane_routed_events must match computed routed count"
            )

        if self.oversized_inline_violation_events != oversized_inline_violation_events:
            raise ValueError(
                "oversized_inline_violation_events must match computed violation count"
            )

        if self.warning_events != warning_events:
            raise ValueError("warning_events must match computed warning count")

        request_ids = tuple(entry.request_id for entry in self.events)
        trace_ids = tuple(entry.trace_id for entry in self.events)

        if len(set(request_ids)) != len(request_ids):
            raise ValueError("Duplicate payload metric request_ids detected")

        if len(set(trace_ids)) != len(trace_ids):
            raise ValueError("Duplicate payload metric trace_ids detected")
