from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


VoiceRoutingIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

VoiceRoutingIntentSource = Literal[
    "voice",
]

VoiceRoutingIntent = Literal[
    "show_memory",
    "show_simulation",
    "show_monitoring",
]

VoiceRoutingViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

VoiceRoutingDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]

VoiceRoutingMode = Literal[
    "normalized_intent_to_display_route",
]

VoiceRoutingStatus = Literal[
    "bound",
]


_VOICE_ROUTE_ID_PATTERN = re.compile(r"^voiceroute_[a-z][a-z0-9_]*$")
_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_SOURCE_COMMAND_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_DISPLAY_ROUTE_ID_PATTERN = re.compile(r"^displayroute_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class VoiceRoutingEntry:
    """Canonical voice routing / intent binding entry."""

    voice_route_id: str
    intent_id: VoiceRoutingIntentId
    intent_source: VoiceRoutingIntentSource
    source_command_id: str
    command_intent: VoiceRoutingIntent
    target_display_route_id: str
    target_view_id: VoiceRoutingViewId
    target_display_role: VoiceRoutingDisplayRole
    target_panel_id: str
    routing_mode: VoiceRoutingMode
    low_latency_required: bool
    explanation_required: bool
    multilingual_ready: bool
    active: bool
    route_status: VoiceRoutingStatus
    description: str

    def __post_init__(self) -> None:
        """Validate voice routing invariants."""
        if not _VOICE_ROUTE_ID_PATTERN.fullmatch(self.voice_route_id):
            raise ValueError(f"Invalid voice_route_id: {self.voice_route_id}")

        if not _INTENT_ID_PATTERN.fullmatch(self.intent_id):
            raise ValueError(f"Invalid intent_id: {self.intent_id}")

        if self.intent_source != "voice":
            raise ValueError(
                f"VOICE_ROUTING at this step only supports voice intents: {self.voice_route_id}"
            )

        if not _SOURCE_COMMAND_ID_PATTERN.fullmatch(self.source_command_id):
            raise ValueError(f"Invalid source_command_id: {self.source_command_id}")

        if not _DISPLAY_ROUTE_ID_PATTERN.fullmatch(self.target_display_route_id):
            raise ValueError(
                f"Invalid target_display_route_id: {self.target_display_route_id}"
            )

        if not _PANEL_ID_PATTERN.fullmatch(self.target_panel_id):
            raise ValueError(f"Invalid target_panel_id: {self.target_panel_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.voice_route_id}"
            )

        if self.routing_mode != "normalized_intent_to_display_route":
            raise ValueError(
                f"voice routing must use normalized_intent_to_display_route mode: {self.voice_route_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"voice routing must require low latency: {self.voice_route_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"voice routing must require explanation: {self.voice_route_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"voice routing must be multilingual-ready: {self.voice_route_id}"
            )

        if not self.active:
            raise ValueError(
                f"voice routing must target active bindings: {self.voice_route_id}"
            )

        if self.route_status != "bound":
            raise ValueError(
                f"voice routing entry must be bound: {self.voice_route_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.source_command_id != "voicecmd_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use canonical source_command_id: {self.voice_route_id}"
                )
            if self.command_intent != "show_memory":
                raise ValueError(
                    f"intent_show_memory_001 must map to show_memory: {self.voice_route_id}"
                )
            if self.target_display_route_id != "displayroute_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use canonical display route: {self.voice_route_id}"
                )
            if self.target_view_id != "view_memory_project_architecture":
                raise ValueError(
                    f"intent_show_memory_001 must resolve to view_memory_project_architecture: {self.voice_route_id}"
                )
            if self.target_display_role != "mobile_display_proxy":
                raise ValueError(
                    f"intent_show_memory_001 must route to mobile_display_proxy: {self.voice_route_id}"
                )
            if self.target_panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"intent_show_memory_001 must route to panel_memory_project_architecture: {self.voice_route_id}"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.source_command_id != "voicecmd_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use canonical source_command_id: {self.voice_route_id}"
                )
            if self.command_intent != "show_simulation":
                raise ValueError(
                    f"intent_show_simulation_001 must map to show_simulation: {self.voice_route_id}"
                )
            if self.target_display_route_id != "displayroute_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use canonical display route: {self.voice_route_id}"
                )
            if self.target_view_id != "view_simulation_skill_overview":
                raise ValueError(
                    f"intent_show_simulation_001 must resolve to view_simulation_skill_overview: {self.voice_route_id}"
                )
            if self.target_display_role != "engineering_display":
                raise ValueError(
                    f"intent_show_simulation_001 must route to engineering_display: {self.voice_route_id}"
                )
            if self.target_panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"intent_show_simulation_001 must route to panel_simulation_skill_overview: {self.voice_route_id}"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.source_command_id != "voicecmd_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use canonical source_command_id: {self.voice_route_id}"
                )
            if self.command_intent != "show_monitoring":
                raise ValueError(
                    f"intent_show_monitoring_001 must map to show_monitoring: {self.voice_route_id}"
                )
            if self.target_display_route_id != "displayroute_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use canonical display route: {self.voice_route_id}"
                )
            if self.target_view_id != "view_monitoring_panel":
                raise ValueError(
                    f"intent_show_monitoring_001 must resolve to view_monitoring_panel: {self.voice_route_id}"
                )
            if self.target_display_role != "primary_dashboard_display":
                raise ValueError(
                    f"intent_show_monitoring_001 must route to primary_dashboard_display: {self.voice_route_id}"
                )
            if self.target_panel_id != "panel_monitoring_panel":
                raise ValueError(
                    f"intent_show_monitoring_001 must route to panel_monitoring_panel: {self.voice_route_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceRoutingContract:
    """Unified voice routing / intent binding contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    explanation_required_entries: int
    multilingual_ready_entries: int
    entries: tuple[VoiceRoutingEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice routing contract invariants."""
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
            raise ValueError("multilingual_ready_entries must match computed count")

        voice_route_ids = tuple(entry.voice_route_id for entry in self.entries)
        intent_ids = tuple(entry.intent_id for entry in self.entries)
        display_route_ids = tuple(entry.target_display_route_id for entry in self.entries)

        if len(set(voice_route_ids)) != len(voice_route_ids):
            raise ValueError("Duplicate voice_route_id values detected")

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate intent_id values detected")

        if len(set(display_route_ids)) != len(display_route_ids):
            raise ValueError("Duplicate target_display_route_id values detected")
