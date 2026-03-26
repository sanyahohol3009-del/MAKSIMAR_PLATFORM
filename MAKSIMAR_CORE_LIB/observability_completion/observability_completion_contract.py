from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.observability_contracts import (
    build_observability_shapes_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.execution_views import (
    build_execution_views_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.payload_metrics import (
    build_payload_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.presentation_display_metrics import (
    build_presentation_display_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.pressure_metrics import (
    build_pressure_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.validation_metrics import (
    build_validation_metrics_contract,
)


ObservabilitySeverity = Literal[
    "info",
    "warning",
    "critical",
]

ObservabilityCompletionStatus = Literal[
    "completed",
]

_OBS_COMPLETION_ENTRY_ID_PATTERN = re.compile(
    r"^observabilitycompletion_[a-z][a-z0-9_]*$"
)
_COMPONENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ObservabilityCompletionEntry:
    """Canonical observability completion entry."""

    completion_entry_id: str
    source_component: str
    total_events: int
    warning_events: int
    critical_events: int
    alerting_events: int
    explanation_ready: bool
    active: bool
    highest_severity: ObservabilitySeverity
    completion_valid: bool
    completion_status: ObservabilityCompletionStatus
    description: str

    def __post_init__(self) -> None:
        """Validate observability completion invariants."""
        if not _OBS_COMPLETION_ENTRY_ID_PATTERN.fullmatch(self.completion_entry_id):
            raise ValueError(
                f"Invalid completion_entry_id: {self.completion_entry_id}"
            )

        if not _COMPONENT_NAME_PATTERN.fullmatch(self.source_component):
            raise ValueError(f"Invalid source_component: {self.source_component}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.completion_entry_id}"
            )

        for field_name, value in (
            ("total_events", self.total_events),
            ("warning_events", self.warning_events),
            ("critical_events", self.critical_events),
            ("alerting_events", self.alerting_events),
        ):
            if value < 0:
                raise ValueError(
                    f"{field_name} must be non-negative: {self.completion_entry_id}"
                )

        if self.total_events <= 0:
            raise ValueError(
                f"total_events must be positive: {self.completion_entry_id}"
            )

        if self.warning_events + self.critical_events > self.total_events:
            raise ValueError(
                f"warning+critical exceeds total_events: {self.completion_entry_id}"
            )

        if not self.explanation_ready:
            raise ValueError(
                f"observability completion entry must be explanation-ready: {self.completion_entry_id}"
            )

        if not self.active:
            raise ValueError(
                f"observability completion entry must be active: {self.completion_entry_id}"
            )

        if not self.completion_valid:
            raise ValueError(
                f"observability completion entry must be valid: {self.completion_entry_id}"
            )

        if self.completion_status != "completed":
            raise ValueError(
                f"observability completion entry must be completed: {self.completion_entry_id}"
            )

        if self.critical_events > 0:
            if self.highest_severity != "critical":
                raise ValueError(
                    f"critical_events require highest_severity=critical: {self.completion_entry_id}"
                )
        elif self.warning_events > 0:
            if self.highest_severity != "warning":
                raise ValueError(
                    f"warning_events require highest_severity=warning: {self.completion_entry_id}"
                )
        else:
            if self.highest_severity != "info":
                raise ValueError(
                    f"zero warning/critical requires highest_severity=info: {self.completion_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class ObservabilityCompletionContract:
    """Unified base observability completion contract."""

    total_entries: int
    total_events_across_components: int
    total_alerting_events: int
    critical_components: int
    completed_entries: int
    entries: tuple[ObservabilityCompletionEntry, ...]

    def __post_init__(self) -> None:
        """Validate observability completion contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        total_events_across_components = sum(
            entry.total_events for entry in self.entries
        )
        total_alerting_events = sum(
            entry.alerting_events for entry in self.entries
        )
        critical_components = sum(
            1 for entry in self.entries if entry.highest_severity == "critical"
        )
        completed_entries = sum(
            1 for entry in self.entries if entry.completion_status == "completed"
        )

        if self.total_events_across_components != total_events_across_components:
            raise ValueError(
                "total_events_across_components must match computed count"
            )

        if self.total_alerting_events != total_alerting_events:
            raise ValueError(
                "total_alerting_events must match computed count"
            )

        if self.critical_components != critical_components:
            raise ValueError("critical_components must match computed count")

        if self.completed_entries != completed_entries:
            raise ValueError("completed_entries must match computed count")

        entry_ids = tuple(entry.completion_entry_id for entry in self.entries)
        component_names = tuple(entry.source_component for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate completion_entry_id values detected")

        if len(set(component_names)) != len(component_names):
            raise ValueError("Duplicate source_component values detected")


def build_observability_completion_contract() -> ObservabilityCompletionContract:
    """Build canonical base observability completion contract."""
    shapes_contract = build_observability_shapes_contract()
    validation_metrics = build_validation_metrics_contract()
    pressure_metrics = build_pressure_metrics_contract()
    payload_metrics = build_payload_metrics_contract()
    execution_views = build_execution_views_contract()
    memory_skill_metrics = build_memory_skill_metrics_contract()
    presentation_metrics = build_presentation_display_metrics_contract()

    if shapes_contract.total_shapes < 3:
        raise ValueError("Expected at least 3 observability shapes")

    entries = (
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_validation_metrics_001",
            source_component="validation_metrics",
            total_events=validation_metrics.total_events,
            warning_events=0,
            critical_events=validation_metrics.rejected_events,
            alerting_events=validation_metrics.rejected_events,
            explanation_ready=True,
            active=True,
            highest_severity="critical" if validation_metrics.rejected_events > 0 else "info",
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for validation metrics.",
        ),
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_pressure_metrics_001",
            source_component="pressure_metrics",
            total_events=pressure_metrics.total_events,
            warning_events=pressure_metrics.elevated_or_higher_events,
            critical_events=0,
            alerting_events=pressure_metrics.alerting_events,
            explanation_ready=True,
            active=True,
            highest_severity="warning" if pressure_metrics.elevated_or_higher_events > 0 else "info",
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for pressure metrics.",
        ),
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_payload_metrics_001",
            source_component="payload_metrics",
            total_events=payload_metrics.total_events,
            warning_events=payload_metrics.warning_events,
            critical_events=0,
            alerting_events=0,
            explanation_ready=True,
            active=True,
            highest_severity="warning" if payload_metrics.warning_events > 0 else "info",
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for payload metrics.",
        ),
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_execution_views_001",
            source_component="execution_views",
            total_events=execution_views.aggregated_total_events,
            warning_events=execution_views.aggregated_warning_events,
            critical_events=execution_views.aggregated_critical_events,
            alerting_events=execution_views.aggregated_alerting_events,
            explanation_ready=True,
            active=True,
            highest_severity=(
                "critical"
                if execution_views.aggregated_critical_events > 0
                else "warning"
                if execution_views.aggregated_warning_events > 0
                else "info"
            ),
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for execution views.",
        ),
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_memory_skill_metrics_001",
            source_component="memory_skill_metrics",
            total_events=memory_skill_metrics.total_entries,
            warning_events=0,
            critical_events=0,
            alerting_events=0,
            explanation_ready=True,
            active=True,
            highest_severity="info",
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for memory/skill metrics.",
        ),
        ObservabilityCompletionEntry(
            completion_entry_id="observabilitycompletion_presentation_display_metrics_001",
            source_component="presentation_display_metrics",
            total_events=presentation_metrics.total_entries,
            warning_events=0,
            critical_events=0,
            alerting_events=0,
            explanation_ready=True,
            active=True,
            highest_severity="info",
            completion_valid=True,
            completion_status="completed",
            description="Completed observability binding for presentation/display metrics.",
        ),
    )

    total_events_across_components = sum(entry.total_events for entry in entries)
    total_alerting_events = sum(entry.alerting_events for entry in entries)
    critical_components = sum(
        1 for entry in entries if entry.highest_severity == "critical"
    )
    completed_entries = sum(
        1 for entry in entries if entry.completion_status == "completed"
    )

    return ObservabilityCompletionContract(
        total_entries=len(entries),
        total_events_across_components=total_events_across_components,
        total_alerting_events=total_alerting_events,
        critical_components=critical_components,
        completed_entries=completed_entries,
        entries=entries,
    )
