from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


VoiceDisplayHandoffIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

VoiceDisplayHandoffViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

VoiceDisplayHandoffDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]

VoiceDisplayHandoffMode = Literal[
    "display_plus_explanation",
]

VoiceDisplayHandoffStatus = Literal[
    "ready",
]


_HANDOFF_ID_PATTERN = re.compile(r"^voicehandoff_[a-z][a-z0-9_]*$")
_VOICE_ROUTE_ID_PATTERN = re.compile(r"^voiceroute_[a-z][a-z0-9_]*$")
_DISPLAY_ROUTE_ID_PATTERN = re.compile(r"^displayroute_[a-z][a-z0-9_]*$")
_EXPLAIN_BINDING_ID_PATTERN = re.compile(r"^explainbind_[a-z][a-z0-9_]*$")
_DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class VoiceDisplayHandoffEntry:
    """Canonical voice display / explanation handoff entry."""

    handoff_id: str
    voice_route_id: str
    intent_id: VoiceDisplayHandoffIntentId
    display_route_id: str
    target_view_id: VoiceDisplayHandoffViewId
    target_display_id: str
    target_display_role: VoiceDisplayHandoffDisplayRole
    target_panel_id: str
    explanation_binding_id: str
    handoff_mode: VoiceDisplayHandoffMode
    low_latency_required: bool
    explanation_text_available: bool
    explanation_payload_available: bool
    multilingual_ready: bool
    active: bool
    handoff_status: VoiceDisplayHandoffStatus
    description: str

    def __post_init__(self) -> None:
        """Validate voice display handoff invariants."""
        if not _HANDOFF_ID_PATTERN.fullmatch(self.handoff_id):
            raise ValueError(f"Invalid handoff_id: {self.handoff_id}")

        if not _VOICE_ROUTE_ID_PATTERN.fullmatch(self.voice_route_id):
            raise ValueError(f"Invalid voice_route_id: {self.voice_route_id}")

        if not _DISPLAY_ROUTE_ID_PATTERN.fullmatch(self.display_route_id):
            raise ValueError(f"Invalid display_route_id: {self.display_route_id}")

        if not _EXPLAIN_BINDING_ID_PATTERN.fullmatch(self.explanation_binding_id):
            raise ValueError(
                f"Invalid explanation_binding_id: {self.explanation_binding_id}"
            )

        if not _DISPLAY_ID_PATTERN.fullmatch(self.target_display_id):
            raise ValueError(f"Invalid target_display_id: {self.target_display_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.target_panel_id):
            raise ValueError(f"Invalid target_panel_id: {self.target_panel_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.handoff_id}")

        if self.handoff_mode != "display_plus_explanation":
            raise ValueError(
                f"voice display handoff must use display_plus_explanation: {self.handoff_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"voice display handoff must require low latency: {self.handoff_id}"
            )

        if not self.explanation_text_available:
            raise ValueError(
                f"voice display handoff must expose explanation text: {self.handoff_id}"
            )

        if not self.explanation_payload_available:
            raise ValueError(
                f"voice display handoff must expose explanation payload: {self.handoff_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"voice display handoff must be multilingual-ready: {self.handoff_id}"
            )

        if not self.active:
            raise ValueError(
                f"voice display handoff must target active bindings: {self.handoff_id}"
            )

        if self.handoff_status != "ready":
            raise ValueError(
                f"voice display handoff must be ready: {self.handoff_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.voice_route_id != "voiceroute_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voiceroute_show_memory_001: {self.handoff_id}"
                )
            if self.display_route_id != "displayroute_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use displayroute_show_memory_001: {self.handoff_id}"
                )
            if self.target_view_id != "view_memory_project_architecture":
                raise ValueError(
                    f"intent_show_memory_001 must resolve to view_memory_project_architecture: {self.handoff_id}"
                )
            if self.target_display_role != "mobile_display_proxy":
                raise ValueError(
                    f"intent_show_memory_001 must route to mobile_display_proxy: {self.handoff_id}"
                )
            if self.target_panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"intent_show_memory_001 must route to panel_memory_project_architecture: {self.handoff_id}"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.voice_route_id != "voiceroute_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voiceroute_show_simulation_001: {self.handoff_id}"
                )
            if self.display_route_id != "displayroute_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use displayroute_show_simulation_001: {self.handoff_id}"
                )
            if self.target_view_id != "view_simulation_skill_overview":
                raise ValueError(
                    f"intent_show_simulation_001 must resolve to view_simulation_skill_overview: {self.handoff_id}"
                )
            if self.target_display_role != "engineering_display":
                raise ValueError(
                    f"intent_show_simulation_001 must route to engineering_display: {self.handoff_id}"
                )
            if self.target_panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"intent_show_simulation_001 must route to panel_simulation_skill_overview: {self.handoff_id}"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.voice_route_id != "voiceroute_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voiceroute_show_monitoring_001: {self.handoff_id}"
                )
            if self.display_route_id != "displayroute_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use displayroute_show_monitoring_001: {self.handoff_id}"
                )
            if self.target_view_id != "view_monitoring_panel":
                raise ValueError(
                    f"intent_show_monitoring_001 must resolve to view_monitoring_panel: {self.handoff_id}"
                )
            if self.target_display_role != "primary_dashboard_display":
                raise ValueError(
                    f"intent_show_monitoring_001 must route to primary_dashboard_display: {self.handoff_id}"
                )
            if self.target_panel_id != "panel_monitoring_panel":
                raise ValueError(
                    f"intent_show_monitoring_001 must route to panel_monitoring_panel: {self.handoff_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceDisplayHandoffContract:
    """Unified voice display / explanation handoff contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    explanation_ready_entries: int
    multilingual_ready_entries: int
    entries: tuple[VoiceDisplayHandoffEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice display handoff contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        low_latency_entries = sum(
            1 for entry in self.entries if entry.low_latency_required
        )
        explanation_ready_entries = sum(
            1
            for entry in self.entries
            if entry.explanation_text_available and entry.explanation_payload_available
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.low_latency_entries != low_latency_entries:
            raise ValueError("low_latency_entries must match computed count")

        if self.explanation_ready_entries != explanation_ready_entries:
            raise ValueError("explanation_ready_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        handoff_ids = tuple(entry.handoff_id for entry in self.entries)
        voice_route_ids = tuple(entry.voice_route_id for entry in self.entries)

        if len(set(handoff_ids)) != len(handoff_ids):
            raise ValueError("Duplicate handoff_id values detected")

        if len(set(voice_route_ids)) != len(voice_route_ids):
            raise ValueError("Duplicate voice_route_id values detected")
