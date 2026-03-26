from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ExplainableViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

ExplainableDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]

ExplainableSummaryMode = Literal[
    "summary_available",
]

ExplainableReasoningMode = Literal[
    "reasoning_payload_available",
]

ExplainableSafetyMode = Literal[
    "safety_note_available",
]

ExplainableBindingStatus = Literal[
    "bound",
]


_BINDING_ID_PATTERN = re.compile(r"^explainbind_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ExplainableViewBindingEntry:
    """Canonical explainable view binding entry."""

    binding_id: str
    view_id: ExplainableViewId
    panel_id: str
    display_id: str
    display_role: ExplainableDisplayRole
    summary_mode: ExplainableSummaryMode
    reasoning_mode: ExplainableReasoningMode
    safety_mode: ExplainableSafetyMode
    multilingual_ready: bool
    explanation_text_available: bool
    explanation_payload_available: bool
    binding_status: ExplainableBindingStatus
    description: str

    def __post_init__(self) -> None:
        """Validate explainable view binding invariants."""
        if not _BINDING_ID_PATTERN.fullmatch(self.binding_id):
            raise ValueError(f"Invalid binding_id: {self.binding_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.panel_id):
            raise ValueError(f"Invalid panel_id: {self.panel_id}")

        if not _DISPLAY_ID_PATTERN.fullmatch(self.display_id):
            raise ValueError(f"Invalid display_id: {self.display_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.binding_id}")

        if self.summary_mode != "summary_available":
            raise ValueError(
                f"explainable binding must expose summary_available: {self.binding_id}"
            )

        if self.reasoning_mode != "reasoning_payload_available":
            raise ValueError(
                f"explainable binding must expose reasoning_payload_available: {self.binding_id}"
            )

        if self.safety_mode != "safety_note_available":
            raise ValueError(
                f"explainable binding must expose safety_note_available: {self.binding_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"explainable binding must be multilingual-ready: {self.binding_id}"
            )

        if not self.explanation_text_available:
            raise ValueError(
                f"explainable binding must expose explanation text: {self.binding_id}"
            )

        if not self.explanation_payload_available:
            raise ValueError(
                f"explainable binding must expose explanation payload: {self.binding_id}"
            )

        if self.binding_status != "bound":
            raise ValueError(
                f"explainable binding must be bound: {self.binding_id}"
            )

        if self.view_id == "view_memory_project_architecture":
            if self.panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"view_memory_project_architecture must bind to panel_memory_project_architecture: {self.binding_id}"
                )
            if self.display_role != "mobile_display_proxy":
                raise ValueError(
                    f"view_memory_project_architecture must bind to mobile_display_proxy: {self.binding_id}"
                )

        if self.view_id == "view_simulation_skill_overview":
            if self.panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"view_simulation_skill_overview must bind to panel_simulation_skill_overview: {self.binding_id}"
                )
            if self.display_role != "engineering_display":
                raise ValueError(
                    f"view_simulation_skill_overview must bind to engineering_display: {self.binding_id}"
                )

        if self.view_id == "view_monitoring_panel":
            if self.panel_id != "panel_monitoring_panel":
                raise ValueError(
                    f"view_monitoring_panel must bind to panel_monitoring_panel: {self.binding_id}"
                )
            if self.display_role != "primary_dashboard_display":
                raise ValueError(
                    f"view_monitoring_panel must bind to primary_dashboard_display: {self.binding_id}"
                )


@dataclass(frozen=True, slots=True)
class ExplainableViewBindingContract:
    """Unified explainable view binding contract."""

    total_entries: int
    multilingual_ready_entries: int
    explanation_text_entries: int
    explanation_payload_entries: int
    entries: tuple[ExplainableViewBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate explainable view binding contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )
        explanation_text_entries = sum(
            1 for entry in self.entries if entry.explanation_text_available
        )
        explanation_payload_entries = sum(
            1 for entry in self.entries if entry.explanation_payload_available
        )

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError(
                "multilingual_ready_entries must match computed count"
            )

        if self.explanation_text_entries != explanation_text_entries:
            raise ValueError(
                "explanation_text_entries must match computed count"
            )

        if self.explanation_payload_entries != explanation_payload_entries:
            raise ValueError(
                "explanation_payload_entries must match computed count"
            )

        binding_ids = tuple(entry.binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("Duplicate binding_id values detected")
