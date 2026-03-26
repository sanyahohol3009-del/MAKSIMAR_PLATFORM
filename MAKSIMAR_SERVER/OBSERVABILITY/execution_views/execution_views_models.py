from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExecutionViewKind = Literal[
    "validation_overview",
    "pressure_overview",
    "payload_overview",
]

ExecutionMetricSource = Literal[
    "validation_metrics",
    "pressure_metrics",
    "payload_metrics",
]


@dataclass(frozen=True, slots=True)
class ExecutionViewEntry:
    """Read-only execution observability view entry."""

    view_id: str
    view_kind: ExecutionViewKind
    source_metric: ExecutionMetricSource
    total_events: int
    warning_events: int
    critical_events: int
    alerting_events: int
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        """Validate execution view invariants."""
        if not self.view_id.strip():
            raise ValueError("view_id must not be empty")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.view_id}")

        if self.total_events < 0:
            raise ValueError(f"total_events must be non-negative for {self.view_id}")

        if self.warning_events < 0:
            raise ValueError(
                f"warning_events must be non-negative for {self.view_id}"
            )

        if self.critical_events < 0:
            raise ValueError(
                f"critical_events must be non-negative for {self.view_id}"
            )

        if self.alerting_events < 0:
            raise ValueError(
                f"alerting_events must be non-negative for {self.view_id}"
            )

        if self.warning_events > self.total_events:
            raise ValueError(
                f"warning_events must not exceed total_events for {self.view_id}"
            )

        if self.critical_events > self.total_events:
            raise ValueError(
                f"critical_events must not exceed total_events for {self.view_id}"
            )

        if self.alerting_events > self.total_events:
            raise ValueError(
                f"alerting_events must not exceed total_events for {self.view_id}"
            )

        if self.warning_events + self.critical_events > self.total_events:
            raise ValueError(
                f"warning_events + critical_events must not exceed total_events for {self.view_id}"
            )

        if not self.read_only:
            raise ValueError(f"execution view must be read-only: {self.view_id}")

        if self.view_kind == "validation_overview":
            if self.source_metric != "validation_metrics":
                raise ValueError(
                    "validation_overview must use source_metric='validation_metrics'"
                )

        if self.view_kind == "pressure_overview":
            if self.source_metric != "pressure_metrics":
                raise ValueError(
                    "pressure_overview must use source_metric='pressure_metrics'"
                )

        if self.view_kind == "payload_overview":
            if self.source_metric != "payload_metrics":
                raise ValueError(
                    "payload_overview must use source_metric='payload_metrics'"
                )


@dataclass(frozen=True, slots=True)
class ExecutionViewsContract:
    """Unified read-only execution views contract."""

    total_views: int
    aggregated_total_events: int
    aggregated_warning_events: int
    aggregated_critical_events: int
    aggregated_alerting_events: int
    views: tuple[ExecutionViewEntry, ...]

    def __post_init__(self) -> None:
        """Validate execution views contract invariants."""
        if self.total_views != len(self.views):
            raise ValueError("total_views must match views length")

        aggregated_total_events = sum(entry.total_events for entry in self.views)
        aggregated_warning_events = sum(entry.warning_events for entry in self.views)
        aggregated_critical_events = sum(entry.critical_events for entry in self.views)
        aggregated_alerting_events = sum(entry.alerting_events for entry in self.views)

        if self.aggregated_total_events != aggregated_total_events:
            raise ValueError(
                "aggregated_total_events must match computed event count"
            )

        if self.aggregated_warning_events != aggregated_warning_events:
            raise ValueError(
                "aggregated_warning_events must match computed warning count"
            )

        if self.aggregated_critical_events != aggregated_critical_events:
            raise ValueError(
                "aggregated_critical_events must match computed critical count"
            )

        if self.aggregated_alerting_events != aggregated_alerting_events:
            raise ValueError(
                "aggregated_alerting_events must match computed alert count"
            )

        view_ids = tuple(entry.view_id for entry in self.views)
        view_kinds = tuple(entry.view_kind for entry in self.views)

        if len(set(view_ids)) != len(view_ids):
            raise ValueError("Duplicate execution view ids detected")

        if len(set(view_kinds)) != len(view_kinds):
            raise ValueError("Duplicate execution view kinds detected")
