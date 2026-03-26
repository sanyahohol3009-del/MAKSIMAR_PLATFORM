from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId
from MAKSIMAR_CORE_LIB.observability_contracts import (
    ObservabilityEventKind,
    ObservabilitySeverity,
)
from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
    ValidationTier,
)


ValidationMetricStatus = Literal[
    "passed",
    "rejected",
]


@dataclass(frozen=True, slots=True)
class ValidationMetricEntry:
    """Server-side validation observability metric entry."""

    shape_id: str
    event_kind: ObservabilityEventKind
    request_id: str
    node_id: CanonicalNodeId
    trace_id: str
    timestamp_utc: str
    resolved_validation_tier: ValidationTier
    final_status: ValidationMetricStatus
    blocking_error_code: ValidationErrorCode | str
    event_severity: ObservabilitySeverity
    rejection_event: bool
    alert_emitted: bool
    description: str

    def __post_init__(self) -> None:
        """Validate validation metric invariants."""
        if self.shape_id != "shape_validation_event":
            raise ValueError(
                f"validation metric must use shape_validation_event: {self.request_id}"
            )

        if self.event_kind != "validation_event":
            raise ValueError(
                f"validation metric must use event_kind='validation_event': {self.request_id}"
            )

        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")

        if not self.trace_id.strip():
            raise ValueError(f"trace_id must not be empty for {self.request_id}")

        if not self.timestamp_utc.strip():
            raise ValueError(
                f"timestamp_utc must not be empty for {self.request_id}"
            )

        if "T" not in self.timestamp_utc:
            raise ValueError(
                f"timestamp_utc must look like ISO datetime for {self.request_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.request_id}"
            )

        if self.final_status == "passed":
            if self.blocking_error_code != "":
                raise ValueError(
                    f"passed validation metric must not have blocking_error_code: {self.request_id}"
                )
            if self.rejection_event:
                raise ValueError(
                    f"passed validation metric must not mark rejection_event: {self.request_id}"
                )
            if self.alert_emitted:
                raise ValueError(
                    f"passed validation metric must not emit alert: {self.request_id}"
                )
            if self.event_severity not in ("info", "warning"):
                raise ValueError(
                    f"passed validation metric must use info/warning severity: {self.request_id}"
                )

        if self.final_status == "rejected":
            if self.blocking_error_code == "":
                raise ValueError(
                    f"rejected validation metric must have blocking_error_code: {self.request_id}"
                )
            if not self.rejection_event:
                raise ValueError(
                    f"rejected validation metric must mark rejection_event: {self.request_id}"
                )
            if not self.alert_emitted:
                raise ValueError(
                    f"rejected validation metric must emit alert: {self.request_id}"
                )
            if self.event_severity not in ("warning", "critical"):
                raise ValueError(
                    f"rejected validation metric must use warning/critical severity: {self.request_id}"
                )


@dataclass(frozen=True, slots=True)
class ValidationMetricsContract:
    """Unified server-side validation metrics contract."""

    total_events: int
    passed_events: int
    rejected_events: int
    events: tuple[ValidationMetricEntry, ...]

    def __post_init__(self) -> None:
        """Validate validation metrics contract invariants."""
        if self.total_events != len(self.events):
            raise ValueError("total_events must match events length")

        passed_events = sum(1 for entry in self.events if entry.final_status == "passed")
        rejected_events = sum(
            1 for entry in self.events if entry.final_status == "rejected"
        )

        if self.passed_events != passed_events:
            raise ValueError("passed_events must match passed entries count")

        if self.rejected_events != rejected_events:
            raise ValueError("rejected_events must match rejected entries count")

        request_ids = tuple(entry.request_id for entry in self.events)
        trace_ids = tuple(entry.trace_id for entry in self.events)

        if len(set(request_ids)) != len(request_ids):
            raise ValueError("Duplicate validation metric request_ids detected")

        if len(set(trace_ids)) != len(trace_ids):
            raise ValueError("Duplicate validation metric trace_ids detected")
