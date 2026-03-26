from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


VoiceLatencyIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

VoiceLatencyClass = Literal[
    "near_instant",
]

VoiceLatencyStageId = Literal[
    "voice_input_stage",
    "intent_normalization_stage",
    "voice_routing_stage",
    "display_handoff_stage",
    "execution_handoff_stage",
]

VoiceLatencyPathStatus = Literal[
    "ready",
]


_PATH_ID_PATTERN = re.compile(r"^latencypath_[a-z][a-z0-9_]*$")
_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_STAGE_BINDING_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_ROUTE_ID_PATTERN = re.compile(r"^voiceroute_[a-z][a-z0-9_]*$")
_DISPLAY_HANDOFF_ID_PATTERN = re.compile(r"^voicehandoff_[a-z][a-z0-9_]*$")
_EXEC_HANDOFF_ID_PATTERN = re.compile(r"^voiceexec_[a-z][a-z0-9_]*$")


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
class VoiceLatencyPathEntry:
    """Canonical voice latency path entry."""

    path_id: str
    intent_id: VoiceLatencyIntentId
    latency_class: VoiceLatencyClass
    stage_ids: tuple[VoiceLatencyStageId, ...]
    source_command_id: str
    normalization_binding_id: str
    voice_route_id: str
    display_handoff_id: str
    execution_handoff_id: str
    low_latency_required: bool
    explanation_required: bool
    multilingual_ready: bool
    active: bool
    path_status: VoiceLatencyPathStatus
    description: str

    def __post_init__(self) -> None:
        """Validate voice latency path invariants."""
        if not _PATH_ID_PATTERN.fullmatch(self.path_id):
            raise ValueError(f"Invalid path_id: {self.path_id}")

        if not _INTENT_ID_PATTERN.fullmatch(self.intent_id):
            raise ValueError(f"Invalid intent_id: {self.intent_id}")

        if not _STAGE_BINDING_ID_PATTERN.fullmatch(self.source_command_id):
            raise ValueError(f"Invalid source_command_id: {self.source_command_id}")

        if not _STAGE_BINDING_ID_PATTERN.fullmatch(self.normalization_binding_id):
            raise ValueError(
                f"Invalid normalization_binding_id: {self.normalization_binding_id}"
            )

        if not _ROUTE_ID_PATTERN.fullmatch(self.voice_route_id):
            raise ValueError(f"Invalid voice_route_id: {self.voice_route_id}")

        if not _DISPLAY_HANDOFF_ID_PATTERN.fullmatch(self.display_handoff_id):
            raise ValueError(
                f"Invalid display_handoff_id: {self.display_handoff_id}"
            )

        if not _EXEC_HANDOFF_ID_PATTERN.fullmatch(self.execution_handoff_id):
            raise ValueError(
                f"Invalid execution_handoff_id: {self.execution_handoff_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.path_id}")

        if self.latency_class != "near_instant":
            raise ValueError(
                f"voice latency path must use near_instant class: {self.path_id}"
            )

        expected_stages = (
            "voice_input_stage",
            "intent_normalization_stage",
            "voice_routing_stage",
            "display_handoff_stage",
            "execution_handoff_stage",
        )
        if self.stage_ids != expected_stages:
            raise ValueError(
                f"voice latency path must preserve canonical stage order: {self.path_id}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.stage_ids,
            field_name="stage_ids",
            owner_id=self.path_id,
        )

        if not self.low_latency_required:
            raise ValueError(
                f"voice latency path must require low latency: {self.path_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"voice latency path must require explanation: {self.path_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"voice latency path must be multilingual-ready: {self.path_id}"
            )

        if not self.active:
            raise ValueError(f"voice latency path must be active: {self.path_id}")

        if self.path_status != "ready":
            raise ValueError(
                f"voice latency path must be ready: {self.path_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.source_command_id != "voicecmd_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voicecmd_show_memory_001: {self.path_id}"
                )
            if self.normalization_binding_id != "intent_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use canonical normalization binding: {self.path_id}"
                )
            if self.voice_route_id != "voiceroute_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voiceroute_show_memory_001: {self.path_id}"
                )
            if self.display_handoff_id != "voicehandoff_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voicehandoff_show_memory_001: {self.path_id}"
                )
            if self.execution_handoff_id != "voiceexec_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voiceexec_show_memory_001: {self.path_id}"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.source_command_id != "voicecmd_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voicecmd_show_simulation_001: {self.path_id}"
                )
            if self.normalization_binding_id != "intent_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use canonical normalization binding: {self.path_id}"
                )
            if self.voice_route_id != "voiceroute_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voiceroute_show_simulation_001: {self.path_id}"
                )
            if self.display_handoff_id != "voicehandoff_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voicehandoff_show_simulation_001: {self.path_id}"
                )
            if self.execution_handoff_id != "voiceexec_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voiceexec_show_simulation_001: {self.path_id}"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.source_command_id != "voicecmd_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voicecmd_show_monitoring_001: {self.path_id}"
                )
            if self.normalization_binding_id != "intent_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use canonical normalization binding: {self.path_id}"
                )
            if self.voice_route_id != "voiceroute_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voiceroute_show_monitoring_001: {self.path_id}"
                )
            if self.display_handoff_id != "voicehandoff_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voicehandoff_show_monitoring_001: {self.path_id}"
                )
            if self.execution_handoff_id != "voiceexec_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voiceexec_show_monitoring_001: {self.path_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceLatencyPathContract:
    """Unified voice latency path contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    explanation_required_entries: int
    multilingual_ready_entries: int
    entries: tuple[VoiceLatencyPathEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice latency path contract invariants."""
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

        path_ids = tuple(entry.path_id for entry in self.entries)
        intent_ids = tuple(entry.intent_id for entry in self.entries)

        if len(set(path_ids)) != len(path_ids):
            raise ValueError("Duplicate path_id values detected")

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate intent_id values detected")
