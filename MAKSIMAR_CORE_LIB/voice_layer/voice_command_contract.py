from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)


VoiceCommandIntent = Literal[
    "show_memory",
    "show_simulation",
    "show_monitoring",
]

VoiceCommandId = Literal[
    "voicecmd_show_memory_001",
    "voicecmd_show_simulation_001",
    "voicecmd_show_monitoring_001",
]

VoiceUtterancePatternId = Literal[
    "utterance_show_memory_001",
    "utterance_show_simulation_001",
    "utterance_show_monitoring_001",
]

VoiceResponseMode = Literal[
    "voice_plus_display",
]

VoiceLatencyClass = Literal[
    "near_instant",
]

VoiceLanguageCode = Literal[
    "en",
    "ru",
    "uk",
    "de",
]

VoiceScriptName = Literal[
    "Latin",
    "Cyrillic",
]

VoiceTargetViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

VoiceDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]


_COMMAND_ID_PATTERN = re.compile(r"^voicecmd_[a-z][a-z0-9_]*$")
_UTTERANCE_ID_PATTERN = re.compile(r"^utterance_[a-z][a-z0-9_]*$")
_DISPLAY_ROUTE_ID_PATTERN = re.compile(r"^displayroute_[a-z][a-z0-9_]*$")


def _validate_unique_non_empty_str_tuple(
    *,
    values: tuple[str, ...],
    field_name: str,
    owner_id: str,
) -> None:
    """Validate tuple items are non-empty and unique."""
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate values in {field_name} for {owner_id}")

    for value in values:
        if not value.strip():
            raise ValueError(f"{field_name} contains empty value for {owner_id}")


@dataclass(frozen=True, slots=True)
class VoiceCommandEntry:
    """Canonical voice command contract entry."""

    command_id: VoiceCommandId
    utterance_pattern_id: VoiceUtterancePatternId
    command_intent: VoiceCommandIntent
    target_view_id: VoiceTargetViewId
    target_display_route_id: str
    target_display_role: VoiceDisplayRole
    response_mode: VoiceResponseMode
    latency_class: VoiceLatencyClass
    low_latency_required: bool
    explanation_required: bool
    multilingual_ready: bool
    supported_languages: tuple[VoiceLanguageCode, ...]
    supported_scripts: tuple[VoiceScriptName, ...]
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate voice command invariants."""
        if not _COMMAND_ID_PATTERN.fullmatch(self.command_id):
            raise ValueError(f"Invalid command_id: {self.command_id}")

        if not _UTTERANCE_ID_PATTERN.fullmatch(self.utterance_pattern_id):
            raise ValueError(
                f"Invalid utterance_pattern_id: {self.utterance_pattern_id}"
            )

        if not _DISPLAY_ROUTE_ID_PATTERN.fullmatch(self.target_display_route_id):
            raise ValueError(
                f"Invalid target_display_route_id: {self.target_display_route_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.command_id}")

        if self.response_mode != "voice_plus_display":
            raise ValueError(
                f"voice command must use voice_plus_display: {self.command_id}"
            )

        if self.latency_class != "near_instant":
            raise ValueError(
                f"voice command must use near_instant latency: {self.command_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"voice command must require low latency: {self.command_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"voice command must require explanation: {self.command_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"voice command must be multilingual-ready: {self.command_id}"
            )

        if not self.active:
            raise ValueError(f"voice command must be active: {self.command_id}")

        _validate_unique_non_empty_str_tuple(
            values=self.supported_languages,
            field_name="supported_languages",
            owner_id=self.command_id,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.supported_scripts,
            field_name="supported_scripts",
            owner_id=self.command_id,
        )

        required_languages = ("en", "ru", "uk", "de")
        required_scripts = ("Latin", "Cyrillic")

        if self.supported_languages != required_languages:
            raise ValueError(
                f"voice command must preserve canonical language set: {self.command_id}"
            )

        if self.supported_scripts != required_scripts:
            raise ValueError(
                f"voice command must preserve canonical script set: {self.command_id}"
            )

        if self.command_intent == "show_memory":
            if self.command_id != "voicecmd_show_memory_001":
                raise ValueError(
                    f"show_memory must use canonical command_id: {self.command_id}"
                )
            if self.utterance_pattern_id != "utterance_show_memory_001":
                raise ValueError(
                    f"show_memory must use canonical utterance pattern: {self.command_id}"
                )
            if self.target_view_id != "view_memory_project_architecture":
                raise ValueError(
                    f"show_memory must resolve to view_memory_project_architecture: {self.command_id}"
                )
            if self.target_display_role != "mobile_display_proxy":
                raise ValueError(
                    f"show_memory must route to mobile_display_proxy: {self.command_id}"
                )

        if self.command_intent == "show_simulation":
            if self.command_id != "voicecmd_show_simulation_001":
                raise ValueError(
                    f"show_simulation must use canonical command_id: {self.command_id}"
                )
            if self.utterance_pattern_id != "utterance_show_simulation_001":
                raise ValueError(
                    f"show_simulation must use canonical utterance pattern: {self.command_id}"
                )
            if self.target_view_id != "view_simulation_skill_overview":
                raise ValueError(
                    f"show_simulation must resolve to view_simulation_skill_overview: {self.command_id}"
                )
            if self.target_display_role != "engineering_display":
                raise ValueError(
                    f"show_simulation must route to engineering_display: {self.command_id}"
                )

        if self.command_intent == "show_monitoring":
            if self.command_id != "voicecmd_show_monitoring_001":
                raise ValueError(
                    f"show_monitoring must use canonical command_id: {self.command_id}"
                )
            if self.utterance_pattern_id != "utterance_show_monitoring_001":
                raise ValueError(
                    f"show_monitoring must use canonical utterance pattern: {self.command_id}"
                )
            if self.target_view_id != "view_monitoring_panel":
                raise ValueError(
                    f"show_monitoring must resolve to view_monitoring_panel: {self.command_id}"
                )
            if self.target_display_role != "primary_dashboard_display":
                raise ValueError(
                    f"show_monitoring must route to primary_dashboard_display: {self.command_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceCommandContract:
    """Unified voice command contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    multilingual_ready_entries: int
    entries: tuple[VoiceCommandEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice command contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        low_latency_entries = sum(
            1 for entry in self.entries if entry.low_latency_required
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.low_latency_entries != low_latency_entries:
            raise ValueError("low_latency_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        command_ids = tuple(entry.command_id for entry in self.entries)
        utterance_ids = tuple(entry.utterance_pattern_id for entry in self.entries)
        display_route_ids = tuple(entry.target_display_route_id for entry in self.entries)

        if len(set(command_ids)) != len(command_ids):
            raise ValueError("Duplicate command_id values detected")

        if len(set(utterance_ids)) != len(utterance_ids):
            raise ValueError("Duplicate utterance_pattern_id values detected")

        if len(set(display_route_ids)) != len(display_route_ids):
            raise ValueError("Duplicate target_display_route_id values detected")


def build_voice_command_contract() -> VoiceCommandContract:
    """Build canonical voice command contract."""
    display_orchestration = build_display_orchestration_contract()
    explainable_binding = build_explainable_view_binding_contract()

    explainable_by_view_id = {
        entry.view_id: entry for entry in explainable_binding.entries
    }

    entries = []
    for orchestration_entry in display_orchestration.entries:
        explainable_entry = explainable_by_view_id[orchestration_entry.resolved_view_id]

        command_id_map = {
            "show_memory": "voicecmd_show_memory_001",
            "show_simulation": "voicecmd_show_simulation_001",
            "show_monitoring": "voicecmd_show_monitoring_001",
        }
        utterance_id_map = {
            "show_memory": "utterance_show_memory_001",
            "show_simulation": "utterance_show_simulation_001",
            "show_monitoring": "utterance_show_monitoring_001",
        }

        entries.append(
            VoiceCommandEntry(
                command_id=command_id_map[orchestration_entry.command_intent],  # type: ignore[arg-type]
                utterance_pattern_id=utterance_id_map[orchestration_entry.command_intent],  # type: ignore[arg-type]
                command_intent=orchestration_entry.command_intent,
                target_view_id=orchestration_entry.resolved_view_id,
                target_display_route_id=orchestration_entry.route_request_id,
                target_display_role=orchestration_entry.selected_display_role,
                response_mode="voice_plus_display",
                latency_class="near_instant",
                low_latency_required=True,
                explanation_required=orchestration_entry.explanation_required,
                multilingual_ready=(
                    orchestration_entry.multilingual_ready
                    and explainable_entry.multilingual_ready
                ),
                supported_languages=("en", "ru", "uk", "de"),
                supported_scripts=("Latin", "Cyrillic"),
                active=True,
                description=(
                    f"Voice command contract for {orchestration_entry.command_intent} "
                    f"routed to {orchestration_entry.selected_display_role}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    low_latency_entries = sum(1 for entry in entries if entry.low_latency_required)
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )

    return VoiceCommandContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )
