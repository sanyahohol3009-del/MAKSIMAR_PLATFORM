from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


VoiceMultilingualIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
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

VoiceCanonicalText = Literal[
    "show memory",
    "show simulation",
    "show monitoring",
]

VoiceBindingStatus = Literal[
    "bound",
]


_BINDING_ID_PATTERN = re.compile(r"^voicemlang_[a-z][a-z0-9_]*$")
_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_ROUTE_ID_PATTERN = re.compile(r"^voiceroute_[a-z][a-z0-9_]*$")
_PATH_ID_PATTERN = re.compile(r"^latencypath_[a-z][a-z0-9_]*$")


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
class VoiceMultilingualBindingEntry:
    """Canonical voice multilingual / multiscript binding entry."""

    binding_id: str
    intent_id: VoiceMultilingualIntentId
    voice_route_id: str
    latency_path_id: str
    canonical_text: VoiceCanonicalText
    supported_languages: tuple[VoiceLanguageCode, ...]
    supported_scripts: tuple[VoiceScriptName, ...]
    localized_texts: tuple[str, ...]
    low_latency_required: bool
    explanation_required: bool
    multilingual_ready: bool
    multiscript_ready: bool
    active: bool
    binding_status: VoiceBindingStatus
    description: str

    def __post_init__(self) -> None:
        """Validate voice multilingual binding invariants."""
        if not _BINDING_ID_PATTERN.fullmatch(self.binding_id):
            raise ValueError(f"Invalid binding_id: {self.binding_id}")

        if not _INTENT_ID_PATTERN.fullmatch(self.intent_id):
            raise ValueError(f"Invalid intent_id: {self.intent_id}")

        if not _ROUTE_ID_PATTERN.fullmatch(self.voice_route_id):
            raise ValueError(f"Invalid voice_route_id: {self.voice_route_id}")

        if not _PATH_ID_PATTERN.fullmatch(self.latency_path_id):
            raise ValueError(f"Invalid latency_path_id: {self.latency_path_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.binding_id}")

        _validate_unique_non_empty_str_tuple(
            values=self.supported_languages,
            field_name="supported_languages",
            owner_id=self.binding_id,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.supported_scripts,
            field_name="supported_scripts",
            owner_id=self.binding_id,
        )
        _validate_unique_non_empty_str_tuple(
            values=self.localized_texts,
            field_name="localized_texts",
            owner_id=self.binding_id,
        )

        required_languages = ("en", "ru", "uk", "de")
        required_scripts = ("Latin", "Cyrillic")

        if self.supported_languages != required_languages:
            raise ValueError(
                f"voice multilingual binding must preserve canonical language set: {self.binding_id}"
            )

        if self.supported_scripts != required_scripts:
            raise ValueError(
                f"voice multilingual binding must preserve canonical script set: {self.binding_id}"
            )

        if len(self.localized_texts) != 4:
            raise ValueError(
                f"voice multilingual binding must provide 4 localized texts: {self.binding_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"voice multilingual binding must require low latency: {self.binding_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"voice multilingual binding must require explanation: {self.binding_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"voice multilingual binding must be multilingual-ready: {self.binding_id}"
            )

        if not self.multiscript_ready:
            raise ValueError(
                f"voice multilingual binding must be multiscript-ready: {self.binding_id}"
            )

        if not self.active:
            raise ValueError(
                f"voice multilingual binding must be active: {self.binding_id}"
            )

        if self.binding_status != "bound":
            raise ValueError(
                f"voice multilingual binding must be bound: {self.binding_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.voice_route_id != "voiceroute_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voiceroute_show_memory_001: {self.binding_id}"
                )
            if self.latency_path_id != "latencypath_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use latencypath_show_memory_001: {self.binding_id}"
                )
            if self.canonical_text != "show memory":
                raise ValueError(
                    f"intent_show_memory_001 must use canonical text 'show memory': {self.binding_id}"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.voice_route_id != "voiceroute_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voiceroute_show_simulation_001: {self.binding_id}"
                )
            if self.latency_path_id != "latencypath_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use latencypath_show_simulation_001: {self.binding_id}"
                )
            if self.canonical_text != "show simulation":
                raise ValueError(
                    f"intent_show_simulation_001 must use canonical text 'show simulation': {self.binding_id}"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.voice_route_id != "voiceroute_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voiceroute_show_monitoring_001: {self.binding_id}"
                )
            if self.latency_path_id != "latencypath_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use latencypath_show_monitoring_001: {self.binding_id}"
                )
            if self.canonical_text != "show monitoring":
                raise ValueError(
                    f"intent_show_monitoring_001 must use canonical text 'show monitoring': {self.binding_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceMultilingualBindingContract:
    """Unified voice multilingual / multiscript binding contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    multilingual_ready_entries: int
    multiscript_ready_entries: int
    entries: tuple[VoiceMultilingualBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice multilingual binding contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        low_latency_entries = sum(
            1 for entry in self.entries if entry.low_latency_required
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )
        multiscript_ready_entries = sum(
            1 for entry in self.entries if entry.multiscript_ready
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.low_latency_entries != low_latency_entries:
            raise ValueError("low_latency_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        if self.multiscript_ready_entries != multiscript_ready_entries:
            raise ValueError("multiscript_ready_entries must match computed count")

        binding_ids = tuple(entry.binding_id for entry in self.entries)
        intent_ids = tuple(entry.intent_id for entry in self.entries)

        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("Duplicate binding_id values detected")

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate intent_id values detected")
