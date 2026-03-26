from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.end_to_end_orchestration_runtime import (
    build_end_to_end_orchestration_runtime_contract,
)
from MAKSIMAR_CORE_LIB.voice_layer import (
    build_voice_command_contract,
)
from MAKSIMAR_SERVER.INTENT_NORMALIZATION import (
    build_intent_normalization_contract,
)
from MAKSIMAR_SERVER.VOICE_DISPLAY_HANDOFF import (
    build_voice_display_handoff_contract,
)
from MAKSIMAR_SERVER.VOICE_EXECUTION_HANDOFF import (
    build_voice_execution_handoff_contract,
)
from MAKSIMAR_SERVER.VOICE_LATENCY_PATH import (
    build_voice_latency_path_contract,
)
from MAKSIMAR_SERVER.VOICE_MULTILINGUAL_BINDING import (
    build_voice_multilingual_binding_contract,
)
from MAKSIMAR_SERVER.VOICE_ROUTING import (
    build_voice_routing_contract,
)


RealVoiceRuntimeEntryId = Literal[
    "realvoice_show_memory_001",
    "realvoice_show_simulation_001",
    "realvoice_show_monitoring_001",
]

VoiceIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

VoiceRuntimeMode = Literal[
    "display_runtime",
    "execution_runtime",
]

VoiceRuntimeStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^realvoice_[a-z][a-z0-9_]*$")
_VOICE_CMD_ID_PATTERN = re.compile(r"^voicecmd_[a-z][a-z0-9_]*$")
_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_ROUTE_ID_PATTERN = re.compile(r"^voiceroute_[a-z][a-z0-9_]*$")
_DISPLAY_HANDOFF_ID_PATTERN = re.compile(r"^voicehandoff_[a-z][a-z0-9_]*$")
_EXEC_HANDOFF_ID_PATTERN = re.compile(r"^voiceexec_[a-z][a-z0-9_]*$")
_LATENCY_ID_PATTERN = re.compile(r"^latencypath_[a-z][a-z0-9_]*$")
_MLANG_ID_PATTERN = re.compile(r"^voicemlang_[a-z][a-z0-9_]*$")
_ORCH_ID_PATTERN = re.compile(r"^orchestration_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class RealVoiceRuntimeEntry:
    """Canonical real voice runtime entry."""

    real_voice_runtime_entry_id: RealVoiceRuntimeEntryId
    linked_voice_command_id: str
    linked_intent_id: VoiceIntentId
    linked_voice_route_id: str
    linked_display_handoff_id: str
    linked_execution_handoff_id: str
    linked_latency_path_id: str
    linked_multilingual_binding_id: str
    linked_orchestration_entry_id: str
    voice_runtime_mode: VoiceRuntimeMode
    low_latency_required: bool
    multilingual_required: bool
    explainable_required: bool
    production_path_allowed: bool
    voice_runtime_status: VoiceRuntimeStatus
    description: str

    def __post_init__(self) -> None:
        """Validate real voice runtime invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.real_voice_runtime_entry_id):
            raise ValueError(
                f"Invalid real_voice_runtime_entry_id: {self.real_voice_runtime_entry_id}"
            )

        if not _VOICE_CMD_ID_PATTERN.fullmatch(self.linked_voice_command_id):
            raise ValueError(
                f"Invalid linked_voice_command_id: {self.linked_voice_command_id}"
            )

        if not _INTENT_ID_PATTERN.fullmatch(self.linked_intent_id):
            raise ValueError(f"Invalid linked_intent_id: {self.linked_intent_id}")

        if not _ROUTE_ID_PATTERN.fullmatch(self.linked_voice_route_id):
            raise ValueError(
                f"Invalid linked_voice_route_id: {self.linked_voice_route_id}"
            )

        if not _DISPLAY_HANDOFF_ID_PATTERN.fullmatch(self.linked_display_handoff_id):
            raise ValueError(
                f"Invalid linked_display_handoff_id: {self.linked_display_handoff_id}"
            )

        if not _EXEC_HANDOFF_ID_PATTERN.fullmatch(self.linked_execution_handoff_id):
            raise ValueError(
                f"Invalid linked_execution_handoff_id: {self.linked_execution_handoff_id}"
            )

        if not _LATENCY_ID_PATTERN.fullmatch(self.linked_latency_path_id):
            raise ValueError(
                f"Invalid linked_latency_path_id: {self.linked_latency_path_id}"
            )

        if not _MLANG_ID_PATTERN.fullmatch(self.linked_multilingual_binding_id):
            raise ValueError(
                f"Invalid linked_multilingual_binding_id: {self.linked_multilingual_binding_id}"
            )

        if not _ORCH_ID_PATTERN.fullmatch(self.linked_orchestration_entry_id):
            raise ValueError(
                f"Invalid linked_orchestration_entry_id: {self.linked_orchestration_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.real_voice_runtime_entry_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"low_latency_required must be True: {self.real_voice_runtime_entry_id}"
            )

        if not self.multilingual_required:
            raise ValueError(
                f"multilingual_required must be True: {self.real_voice_runtime_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.real_voice_runtime_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.real_voice_runtime_entry_id}"
            )

        if self.voice_runtime_status != "active":
            raise ValueError(
                f"voice_runtime_status must be active: {self.real_voice_runtime_entry_id}"
            )

        if self.real_voice_runtime_entry_id == "realvoice_show_memory_001":
            if self.linked_voice_command_id != "voicecmd_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link voicecmd_show_memory_001"
                )
            if self.linked_intent_id != "intent_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link intent_show_memory_001"
                )
            if self.linked_voice_route_id != "voiceroute_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link voiceroute_show_memory_001"
                )
            if self.linked_display_handoff_id != "voicehandoff_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link voicehandoff_show_memory_001"
                )
            if self.linked_execution_handoff_id != "voiceexec_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link voiceexec_show_memory_001"
                )
            if self.linked_latency_path_id != "latencypath_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link latencypath_show_memory_001"
                )
            if self.linked_multilingual_binding_id != "voicemlang_show_memory_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link voicemlang_show_memory_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_mobile_entry_001":
                raise ValueError(
                    "realvoice_show_memory_001 must link orchestration_mobile_entry_001"
                )
            if self.voice_runtime_mode != "display_runtime":
                raise ValueError(
                    "realvoice_show_memory_001 must use display_runtime"
                )

        if self.real_voice_runtime_entry_id == "realvoice_show_simulation_001":
            if self.linked_voice_command_id != "voicecmd_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link voicecmd_show_simulation_001"
                )
            if self.linked_intent_id != "intent_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link intent_show_simulation_001"
                )
            if self.linked_voice_route_id != "voiceroute_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link voiceroute_show_simulation_001"
                )
            if self.linked_display_handoff_id != "voicehandoff_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link voicehandoff_show_simulation_001"
                )
            if self.linked_execution_handoff_id != "voiceexec_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link voiceexec_show_simulation_001"
                )
            if self.linked_latency_path_id != "latencypath_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link latencypath_show_simulation_001"
                )
            if self.linked_multilingual_binding_id != "voicemlang_show_simulation_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link voicemlang_show_simulation_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_heavy_execution_001":
                raise ValueError(
                    "realvoice_show_simulation_001 must link orchestration_heavy_execution_001"
                )
            if self.voice_runtime_mode != "execution_runtime":
                raise ValueError(
                    "realvoice_show_simulation_001 must use execution_runtime"
                )

        if self.real_voice_runtime_entry_id == "realvoice_show_monitoring_001":
            if self.linked_voice_command_id != "voicecmd_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link voicecmd_show_monitoring_001"
                )
            if self.linked_intent_id != "intent_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link intent_show_monitoring_001"
                )
            if self.linked_voice_route_id != "voiceroute_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link voiceroute_show_monitoring_001"
                )
            if self.linked_display_handoff_id != "voicehandoff_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link voicehandoff_show_monitoring_001"
                )
            if self.linked_execution_handoff_id != "voiceexec_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link voiceexec_show_monitoring_001"
                )
            if self.linked_latency_path_id != "latencypath_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link latencypath_show_monitoring_001"
                )
            if self.linked_multilingual_binding_id != "voicemlang_show_monitoring_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link voicemlang_show_monitoring_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_control_plane_001":
                raise ValueError(
                    "realvoice_show_monitoring_001 must link orchestration_control_plane_001"
                )
            if self.voice_runtime_mode != "display_runtime":
                raise ValueError(
                    "realvoice_show_monitoring_001 must use display_runtime"
                )


@dataclass(frozen=True, slots=True)
class RealVoiceRuntimeContract:
    """Unified real voice runtime contract."""

    total_entries: int
    display_runtime_entries: int
    execution_runtime_entries: int
    multilingual_entries: int
    active_entries: int
    entries: tuple[RealVoiceRuntimeEntry, ...]

    def __post_init__(self) -> None:
        """Validate real voice runtime contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        display_runtime_entries = sum(
            1 for entry in self.entries if entry.voice_runtime_mode == "display_runtime"
        )
        execution_runtime_entries = sum(
            1 for entry in self.entries if entry.voice_runtime_mode == "execution_runtime"
        )
        multilingual_entries = sum(
            1 for entry in self.entries if entry.multilingual_required
        )
        active_entries = sum(
            1 for entry in self.entries if entry.voice_runtime_status == "active"
        )

        if self.display_runtime_entries != display_runtime_entries:
            raise ValueError("display_runtime_entries must match computed count")

        if self.execution_runtime_entries != execution_runtime_entries:
            raise ValueError("execution_runtime_entries must match computed count")

        if self.multilingual_entries != multilingual_entries:
            raise ValueError("multilingual_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.real_voice_runtime_entry_id for entry in self.entries)
        intent_ids = tuple(entry.linked_intent_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate real_voice_runtime_entry_id values detected")

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate linked_intent_id values detected")


def build_real_voice_runtime_contract() -> RealVoiceRuntimeContract:
    """Build canonical real voice runtime contract."""
    voice_commands = build_voice_command_contract()
    intents = build_intent_normalization_contract()
    voice_routes = build_voice_routing_contract()
    display_handoffs = build_voice_display_handoff_contract()
    execution_handoffs = build_voice_execution_handoff_contract()
    latency_paths = build_voice_latency_path_contract()
    multilingual_bindings = build_voice_multilingual_binding_contract()
    orchestration = build_end_to_end_orchestration_runtime_contract()

    voice_command_ids = {entry.command_id for entry in voice_commands.entries}
    intent_ids = {entry.intent_id for entry in intents.entries}
    route_ids = {entry.voice_route_id for entry in voice_routes.entries}
    display_handoff_ids = {entry.handoff_id for entry in display_handoffs.entries}
    execution_handoff_ids = {entry.handoff_id for entry in execution_handoffs.entries}
    latency_ids = {entry.path_id for entry in latency_paths.entries}
    multilingual_ids = {entry.binding_id for entry in multilingual_bindings.entries}
    orchestration_ids = {entry.orchestration_entry_id for entry in orchestration.entries}

    required_voice_command_ids = {
        "voicecmd_show_memory_001",
        "voicecmd_show_simulation_001",
        "voicecmd_show_monitoring_001",
    }
    required_intent_ids = {
        "intent_show_memory_001",
        "intent_show_simulation_001",
        "intent_show_monitoring_001",
    }
    required_route_ids = {
        "voiceroute_show_memory_001",
        "voiceroute_show_simulation_001",
        "voiceroute_show_monitoring_001",
    }
    required_display_handoff_ids = {
        "voicehandoff_show_memory_001",
        "voicehandoff_show_simulation_001",
        "voicehandoff_show_monitoring_001",
    }
    required_execution_handoff_ids = {
        "voiceexec_show_memory_001",
        "voiceexec_show_simulation_001",
        "voiceexec_show_monitoring_001",
    }
    required_latency_ids = {
        "latencypath_show_memory_001",
        "latencypath_show_simulation_001",
        "latencypath_show_monitoring_001",
    }
    required_multilingual_ids = {
        "voicemlang_show_memory_001",
        "voicemlang_show_simulation_001",
        "voicemlang_show_monitoring_001",
    }
    required_orchestration_ids = {
        "orchestration_control_plane_001",
        "orchestration_heavy_execution_001",
        "orchestration_mobile_entry_001",
    }

    for label, required, actual in (
        ("voice command ids", required_voice_command_ids, voice_command_ids),
        ("intent ids", required_intent_ids, intent_ids),
        ("route ids", required_route_ids, route_ids),
        ("display handoff ids", required_display_handoff_ids, display_handoff_ids),
        ("execution handoff ids", required_execution_handoff_ids, execution_handoff_ids),
        ("latency ids", required_latency_ids, latency_ids),
        ("multilingual ids", required_multilingual_ids, multilingual_ids),
        ("orchestration ids", required_orchestration_ids, orchestration_ids),
    ):
        missing = required - actual
        if missing:
            raise ValueError(f"Missing {label}: {sorted(missing)}")

    entries = (
        RealVoiceRuntimeEntry(
            real_voice_runtime_entry_id="realvoice_show_memory_001",
            linked_voice_command_id="voicecmd_show_memory_001",
            linked_intent_id="intent_show_memory_001",
            linked_voice_route_id="voiceroute_show_memory_001",
            linked_display_handoff_id="voicehandoff_show_memory_001",
            linked_execution_handoff_id="voiceexec_show_memory_001",
            linked_latency_path_id="latencypath_show_memory_001",
            linked_multilingual_binding_id="voicemlang_show_memory_001",
            linked_orchestration_entry_id="orchestration_mobile_entry_001",
            voice_runtime_mode="display_runtime",
            low_latency_required=True,
            multilingual_required=True,
            explainable_required=True,
            production_path_allowed=True,
            voice_runtime_status="active",
            description="Canonical real voice runtime entry for show memory.",
        ),
        RealVoiceRuntimeEntry(
            real_voice_runtime_entry_id="realvoice_show_simulation_001",
            linked_voice_command_id="voicecmd_show_simulation_001",
            linked_intent_id="intent_show_simulation_001",
            linked_voice_route_id="voiceroute_show_simulation_001",
            linked_display_handoff_id="voicehandoff_show_simulation_001",
            linked_execution_handoff_id="voiceexec_show_simulation_001",
            linked_latency_path_id="latencypath_show_simulation_001",
            linked_multilingual_binding_id="voicemlang_show_simulation_001",
            linked_orchestration_entry_id="orchestration_heavy_execution_001",
            voice_runtime_mode="execution_runtime",
            low_latency_required=True,
            multilingual_required=True,
            explainable_required=True,
            production_path_allowed=True,
            voice_runtime_status="active",
            description="Canonical real voice runtime entry for show simulation.",
        ),
        RealVoiceRuntimeEntry(
            real_voice_runtime_entry_id="realvoice_show_monitoring_001",
            linked_voice_command_id="voicecmd_show_monitoring_001",
            linked_intent_id="intent_show_monitoring_001",
            linked_voice_route_id="voiceroute_show_monitoring_001",
            linked_display_handoff_id="voicehandoff_show_monitoring_001",
            linked_execution_handoff_id="voiceexec_show_monitoring_001",
            linked_latency_path_id="latencypath_show_monitoring_001",
            linked_multilingual_binding_id="voicemlang_show_monitoring_001",
            linked_orchestration_entry_id="orchestration_control_plane_001",
            voice_runtime_mode="display_runtime",
            low_latency_required=True,
            multilingual_required=True,
            explainable_required=True,
            production_path_allowed=True,
            voice_runtime_status="active",
            description="Canonical real voice runtime entry for show monitoring.",
        ),
    )

    display_runtime_entries = sum(
        1 for entry in entries if entry.voice_runtime_mode == "display_runtime"
    )
    execution_runtime_entries = sum(
        1 for entry in entries if entry.voice_runtime_mode == "execution_runtime"
    )
    multilingual_entries = sum(
        1 for entry in entries if entry.multilingual_required
    )
    active_entries = sum(
        1 for entry in entries if entry.voice_runtime_status == "active"
    )

    return RealVoiceRuntimeContract(
        total_entries=len(entries),
        display_runtime_entries=display_runtime_entries,
        execution_runtime_entries=execution_runtime_entries,
        multilingual_entries=multilingual_entries,
        active_entries=active_entries,
        entries=entries,
    )
