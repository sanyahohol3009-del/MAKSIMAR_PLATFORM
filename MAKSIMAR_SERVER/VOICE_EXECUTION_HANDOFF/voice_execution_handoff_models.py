from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


VoiceExecutionIntentId = Literal[
    "intent_show_memory_001",
    "intent_show_simulation_001",
    "intent_show_monitoring_001",
]

VoiceExecutionIntentKind = Literal[
    "display_request",
]

VoiceExecutionTaskClass = Literal[
    "chat_request",
    "simulation_request",
]

VoiceExecutionPayloadClass = Literal[
    "small_control",
]

VoiceExecutionValidationTier = Literal[
    "L1_HEADER",
    "L3_DEEP",
]

VoiceExecutionAdmissionDecision = Literal[
    "accept",
]

VoiceExecutionPressureLevel = Literal[
    "normal",
]

VoiceExecutionHandoffMode = Literal[
    "validation_policy_admission_handoff",
]

VoiceExecutionHandoffStatus = Literal[
    "ready",
]


_HANDOFF_ID_PATTERN = re.compile(r"^voiceexec_[a-z][a-z0-9_]*$")
_INTENT_ID_PATTERN = re.compile(r"^intent_[a-z][a-z0-9_]*$")
_DISPLAY_HANDOFF_ID_PATTERN = re.compile(r"^voicehandoff_[a-z][a-z0-9_]*$")
_POLICY_RULE_ID_PATTERN = re.compile(r"^policy_[a-z][a-z0-9_]*$")
_VALIDATION_REQUEST_ID_PATTERN = re.compile(r"^valreq_[a-z][a-z0-9_]*$")
_PRESSURE_ENTRY_ID_PATTERN = re.compile(r"^pressureentry_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class VoiceExecutionHandoffEntry:
    """Canonical voice execution handoff entry."""

    handoff_id: str
    intent_id: VoiceExecutionIntentId
    display_handoff_id: str
    intent_kind: VoiceExecutionIntentKind
    task_class: VoiceExecutionTaskClass
    payload_class: VoiceExecutionPayloadClass
    policy_rule_id: str
    validation_request_id: str
    resolved_validation_tier: VoiceExecutionValidationTier
    admission_decision: VoiceExecutionAdmissionDecision
    pressure_level: VoiceExecutionPressureLevel
    pressure_entry_id: str
    low_latency_required: bool
    explanation_required: bool
    policy_compatible: bool
    active: bool
    handoff_mode: VoiceExecutionHandoffMode
    handoff_status: VoiceExecutionHandoffStatus
    description: str

    def __post_init__(self) -> None:
        """Validate voice execution handoff invariants."""
        if not _HANDOFF_ID_PATTERN.fullmatch(self.handoff_id):
            raise ValueError(f"Invalid handoff_id: {self.handoff_id}")

        if not _INTENT_ID_PATTERN.fullmatch(self.intent_id):
            raise ValueError(f"Invalid intent_id: {self.intent_id}")

        if not _DISPLAY_HANDOFF_ID_PATTERN.fullmatch(self.display_handoff_id):
            raise ValueError(
                f"Invalid display_handoff_id: {self.display_handoff_id}"
            )

        if not _POLICY_RULE_ID_PATTERN.fullmatch(self.policy_rule_id):
            raise ValueError(f"Invalid policy_rule_id: {self.policy_rule_id}")

        if not _VALIDATION_REQUEST_ID_PATTERN.fullmatch(self.validation_request_id):
            raise ValueError(
                f"Invalid validation_request_id: {self.validation_request_id}"
            )

        if not _PRESSURE_ENTRY_ID_PATTERN.fullmatch(self.pressure_entry_id):
            raise ValueError(f"Invalid pressure_entry_id: {self.pressure_entry_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.handoff_id}")

        if self.intent_kind != "display_request":
            raise ValueError(
                f"voice execution handoff only supports display_request here: {self.handoff_id}"
            )

        if self.payload_class != "small_control":
            raise ValueError(
                f"voice execution handoff must use small_control payload: {self.handoff_id}"
            )

        if self.admission_decision != "accept":
            raise ValueError(
                f"voice execution handoff must be admissible: {self.handoff_id}"
            )

        if self.pressure_level != "normal":
            raise ValueError(
                f"voice execution handoff must remain on normal pressure in this step: {self.handoff_id}"
            )

        if not self.low_latency_required:
            raise ValueError(
                f"voice execution handoff must require low latency: {self.handoff_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"voice execution handoff must require explanation: {self.handoff_id}"
            )

        if not self.policy_compatible:
            raise ValueError(
                f"voice execution handoff must be policy-compatible: {self.handoff_id}"
            )

        if not self.active:
            raise ValueError(
                f"voice execution handoff must target active routes: {self.handoff_id}"
            )

        if self.handoff_mode != "validation_policy_admission_handoff":
            raise ValueError(
                f"voice execution handoff must use validation_policy_admission_handoff: {self.handoff_id}"
            )

        if self.handoff_status != "ready":
            raise ValueError(
                f"voice execution handoff must be ready: {self.handoff_id}"
            )

        if self.intent_id == "intent_show_memory_001":
            if self.display_handoff_id != "voicehandoff_show_memory_001":
                raise ValueError(
                    f"intent_show_memory_001 must use voicehandoff_show_memory_001: {self.handoff_id}"
                )
            if self.task_class != "chat_request":
                raise ValueError(
                    f"intent_show_memory_001 must map to chat_request: {self.handoff_id}"
                )
            if self.policy_rule_id != "policy_chat_request_small_control":
                raise ValueError(
                    f"intent_show_memory_001 must use policy_chat_request_small_control: {self.handoff_id}"
                )
            if self.resolved_validation_tier != "L1_HEADER":
                raise ValueError(
                    f"intent_show_memory_001 must use L1_HEADER: {self.handoff_id}"
                )

        if self.intent_id == "intent_show_simulation_001":
            if self.display_handoff_id != "voicehandoff_show_simulation_001":
                raise ValueError(
                    f"intent_show_simulation_001 must use voicehandoff_show_simulation_001: {self.handoff_id}"
                )
            if self.task_class != "simulation_request":
                raise ValueError(
                    f"intent_show_simulation_001 must map to simulation_request: {self.handoff_id}"
                )
            if self.policy_rule_id != "policy_simulation_request_small_control":
                raise ValueError(
                    f"intent_show_simulation_001 must use policy_simulation_request_small_control: {self.handoff_id}"
                )
            if self.resolved_validation_tier != "L1_HEADER":
                raise ValueError(
                    f"intent_show_simulation_001 must use L1_HEADER: {self.handoff_id}"
                )

        if self.intent_id == "intent_show_monitoring_001":
            if self.display_handoff_id != "voicehandoff_show_monitoring_001":
                raise ValueError(
                    f"intent_show_monitoring_001 must use voicehandoff_show_monitoring_001: {self.handoff_id}"
                )
            if self.task_class != "chat_request":
                raise ValueError(
                    f"intent_show_monitoring_001 must map to chat_request: {self.handoff_id}"
                )
            if self.policy_rule_id != "policy_chat_request_small_control":
                raise ValueError(
                    f"intent_show_monitoring_001 must use policy_chat_request_small_control: {self.handoff_id}"
                )
            if self.resolved_validation_tier != "L1_HEADER":
                raise ValueError(
                    f"intent_show_monitoring_001 must use L1_HEADER: {self.handoff_id}"
                )


@dataclass(frozen=True, slots=True)
class VoiceExecutionHandoffContract:
    """Unified voice execution handoff contract."""

    total_entries: int
    active_entries: int
    low_latency_entries: int
    policy_compatible_entries: int
    ready_entries: int
    entries: tuple[VoiceExecutionHandoffEntry, ...]

    def __post_init__(self) -> None:
        """Validate voice execution handoff contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        low_latency_entries = sum(
            1 for entry in self.entries if entry.low_latency_required
        )
        policy_compatible_entries = sum(
            1 for entry in self.entries if entry.policy_compatible
        )
        ready_entries = sum(
            1 for entry in self.entries if entry.handoff_status == "ready"
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.low_latency_entries != low_latency_entries:
            raise ValueError("low_latency_entries must match computed count")

        if self.policy_compatible_entries != policy_compatible_entries:
            raise ValueError("policy_compatible_entries must match computed count")

        if self.ready_entries != ready_entries:
            raise ValueError("ready_entries must match computed count")

        handoff_ids = tuple(entry.handoff_id for entry in self.entries)
        intent_ids = tuple(entry.intent_id for entry in self.entries)
        validation_request_ids = tuple(
            entry.validation_request_id for entry in self.entries
        )

        if len(set(handoff_ids)) != len(handoff_ids):
            raise ValueError("Duplicate handoff_id values detected")

        if len(set(intent_ids)) != len(intent_ids):
            raise ValueError("Duplicate intent_id values detected")

        if len(set(validation_request_ids)) != len(validation_request_ids):
            raise ValueError("Duplicate validation_request_id values detected")
