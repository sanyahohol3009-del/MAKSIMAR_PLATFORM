from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ObservabilityEventKind = Literal[
    "validation_event",
    "pressure_event",
    "payload_event",
]

ObservabilitySeverity = Literal[
    "info",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class ObservabilityEventShapeEntry:
    """Canonical observability event shape entry."""

    shape_id: str
    event_kind: ObservabilityEventKind
    default_severity: ObservabilitySeverity
    requires_node_id: bool
    requires_trace_id: bool
    requires_timestamp: bool
    supports_alerting: bool
    description: str

    def __post_init__(self) -> None:
        """Validate observability shape invariants."""
        if not self.shape_id.strip():
            raise ValueError("shape_id must not be empty")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.shape_id}")

        if not self.requires_timestamp:
            raise ValueError(
                f"observability shape must require timestamp: {self.shape_id}"
            )

        if not self.requires_trace_id:
            raise ValueError(
                f"observability shape must require trace_id: {self.shape_id}"
            )

        if self.event_kind == "validation_event":
            if self.default_severity not in ("warning", "critical"):
                raise ValueError(
                    "validation_event must default to warning or critical severity"
                )

        if self.event_kind == "pressure_event":
            if self.default_severity not in ("warning", "critical"):
                raise ValueError(
                    "pressure_event must default to warning or critical severity"
                )
            if not self.supports_alerting:
                raise ValueError(
                    "pressure_event must support alerting"
                )

        if self.event_kind == "payload_event":
            if self.default_severity not in ("info", "warning"):
                raise ValueError(
                    "payload_event must default to info or warning severity"
                )


@dataclass(frozen=True, slots=True)
class ObservabilityShapesContract:
    """Unified canonical observability shapes contract."""

    total_shapes: int
    shapes: tuple[ObservabilityEventShapeEntry, ...]


def build_observability_shapes_contract() -> ObservabilityShapesContract:
    """Build canonical observability shapes contract."""
    shapes = (
        ObservabilityEventShapeEntry(
            shape_id="shape_validation_event",
            event_kind="validation_event",
            default_severity="warning",
            requires_node_id=True,
            requires_trace_id=True,
            requires_timestamp=True,
            supports_alerting=True,
            description="Validation event shape for policy, gate, and rejection observability.",
        ),
        ObservabilityEventShapeEntry(
            shape_id="shape_pressure_event",
            event_kind="pressure_event",
            default_severity="warning",
            requires_node_id=True,
            requires_trace_id=True,
            requires_timestamp=True,
            supports_alerting=True,
            description="Pressure event shape for pressure transitions and degraded triggers.",
        ),
        ObservabilityEventShapeEntry(
            shape_id="shape_payload_event",
            event_kind="payload_event",
            default_severity="info",
            requires_node_id=True,
            requires_trace_id=True,
            requires_timestamp=True,
            supports_alerting=False,
            description="Payload event shape for routing, embedding, and data-plane exposure.",
        ),
    )

    shape_ids = tuple(entry.shape_id for entry in shapes)
    event_kinds = tuple(entry.event_kind for entry in shapes)

    if shape_ids != (
        "shape_validation_event",
        "shape_pressure_event",
        "shape_payload_event",
    ):
        raise ValueError("Observability shape order is invalid")

    if event_kinds != (
        "validation_event",
        "pressure_event",
        "payload_event",
    ):
        raise ValueError("Observability event kind order is invalid")

    if len(set(shape_ids)) != len(shape_ids):
        raise ValueError("Duplicate observability shape ids detected")

    if len(set(event_kinds)) != len(event_kinds):
        raise ValueError("Duplicate observability event kinds detected")

    return ObservabilityShapesContract(
        total_shapes=len(shapes),
        shapes=shapes,
    )
