from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


IntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

IntentSource = Literal[
    "voice",
    "ui",
    "api",
    "automation",
    "gesture",
    "mobile",
]

IntentKind = Literal[
    "display_request",
]

TargetDomain = Literal[
    "memory",
    "simulation",
    "monitoring",
]

TargetAction = Literal[
    "show",
]

TargetViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

TargetDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]

NormalizedIntentStatus = Literal[
    "normalized",
]

ConfidenceBand = Literal[
    "high",
]


_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_ROUTE_SOURCE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_TEXT_PATTERN = re.compile(r"^[a-z0-9_ ]+$")


@dataclass(frozen=True, slots=True)
class NormalizedIntentEntry:
    """Canonical normalized intent entry."""

    intent_id: IntentId
    intent_source: IntentSource
    source_command_id: str
    intent_kind: IntentKind
    target_domain: TargetDomain
    target_action: TargetAction
    target_view_id: TargetViewId
    target_display_role: TargetDisplayRole
    normalized_text: str
    confidence_band: ConfidenceBand
    low_latency_required: bool
    explanation_required: bool
    multilingual_ready: bool
    active: bool
    normalization_status: NormalizedIntentStatus
    description: str

    def __post_init__(self) -> None:
        """Validate normalized intent invariants."""
        if not _INTENT_ID_PATTERN.fullmatch(self.intent_id):
            raise ValueError(f"Invalid intent_id: {self.intent_id}")

        if not _ROUTE_SOURCE_ID_PATTERN.fullmatch(self.source_command_id):
            raise ValueError(
                f"Invalid source_command_id: {self.source_command_id}"
            )

        if not _TEXT_PATTERN.fullmatch(self.normalized_text):
            raise ValueError(
                f"normalized_text must be lowercase ascii/underscore/space only: {self.intent_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.intent_id}"
            )

        if self.intent_kind != "display_request":
            raise ValueError(
                f"Only display_request is allowed in this step: {self.intent_id}"
            )

        if self.target_action != "show":
            raise ValueError(
                f"Only show action is allowed in this step: {self.intent_id}"
            )

        if self.confidence_band != "high":
            raise ValueError(
                f"Intent confidence must be high at this step: {self.intent_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"Normalized intent must require low latency: {self.intent_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"Normalized intent must require explanation: {self.intent_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"Normalized intent must be multilingual-ready: {self.intent_id}"
            )

        if not self.active:
            raise ValueError(
                f"Normalized intent must be active: {self.intent_id}"
            )

        if self.normalization_status != "normalized":
            raise ValueError(
                f"Normalization status must be normalized: {self.intent_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.intent_source != "voice":
                raise ValueError(
                    "intent_show_memory_001 must originate from voice at this step"
                )
            if self.source_command_id != "voicecmd_show_memory_001":
                raise ValueError(
                    "intent_show_memory_001 must use canonical voice source_command_id"
                )
            if self.target_domain != "memory":
                raise ValueError(
                    "intent_show_memory_001 must target memory domain"
                )
            if self.target_view_id != "view_memory_project_architecture":
                raise ValueError(
                    "intent_show_memory_001 must resolve to view_memory_project_architecture"
                )
            if self.target_display_role != "mobile_display_proxy":
                raise ValueError(
                    "intent_show_memory_001 must target mobile_display_proxy"
                )
            if self.normalized_text != "show memory":
                raise ValueError(
                    "intent_show_memory_001 must normalize to 'show memory'"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.intent_source != "voice":
                raise ValueError(
                    "intent_show_simulation_001 must originate from voice at this step"
                )
            if self.source_command_id != "voicecmd_show_simulation_001":
                raise ValueError(
                    "intent_show_simulation_001 must use canonical voice source_command_id"
                )
            if self.target_domain != "simulation":
                raise ValueError(
                    "intent_show_simulation_001 must target simulation domain"
                )
            if self.target_view_id != "view_simulation_skill_overview":
                raise ValueError(
                    "intent_show_simulation_001 must resolve to view_simulation_skill_overview"
                )
            if self.target_display_role != "engineering_display":
                raise ValueError(
                    "intent_show_simulation_001 must target engineering_display"
                )
            if self.normalized_text != "show simulation":
                raise ValueError(
                    "intent_show_simulation_001 must normalize to 'show simulation'"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.intent_source != "voice":
                raise ValueError(
                    "intent_show_monitoring_001 must originate from voice at this step"
                )
            if self.source_command_id != "voicecmd_show_monitoring_001":
                raise ValueError(
                    "intent_show_monitoring_001 must use canonical voice source_command_id"
                )
            if self.target_domain != "monitoring":
                raise ValueError(
                    "intent_show_monitoring_001 must target monitoring domain"
                )
            if self.target_view_id != "view_monitoring_panel":
                raise ValueError(
                    "intent_show_monitoring_001 must resolve to view_monitoring_panel"
                )
            if self.target_display_role != "primary_dashboard_display":
                raise ValueError(
                    "intent_show_monitoring_001 must target primary_dashboard_display"
                )
            if self.normalized_text != "show monitoring":
                raise ValueError(
                    "intent_show_monitoring_001 must normalize to 'show monitoring'"
                )


@dataclass(frozen=True, slots=True)
class IntentNormalizationContract:
    """Unified canonical intent normalization contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    explanation_required_entries: int
    multilingual_ready_entries: int
    entries: tuple[NormalizedIntentEntry, ...]

    def __post_init__(self) -> None:
        """Validate contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        low_latency_entries = sum(
            1 for entry in self.entries if entry.low_latency_required
        )
        explanation_required_entries = sum(
            1 for entry in self.entries if entry.explanation_required
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.low_latency_entries != low_latency_entries:
            raise ValueError("low_latency_entries must match computed count")

        if self.explanation_required_entries != explanation_required_entries:
            raise ValueError(
                "explanation_required_entries must match computed count"
            )

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError(
                "multilingual_ready_entries must match computed count"
            )

        intent_ids = tuple(entry.intent_id for entry in self.entries)
        source_command_ids = tuple(entry.source_command_id for entry in self.entries)

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate intent_id values detected")

        if len(set(source_command_ids)) != len(source_command_ids):
            raise ValueError("Duplicate source_command_id values detected")
