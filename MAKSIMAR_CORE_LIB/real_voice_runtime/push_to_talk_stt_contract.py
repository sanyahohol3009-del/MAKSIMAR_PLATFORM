from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PushToTalkSttContract:
    contract_id: str
    read_only: bool = True
    dashboard_safe: bool = True
    push_to_talk_allowed: bool = True
    microphone_permission_required: bool = True
    owner_command_required: bool = True
    manual_activation_required: bool = True
    physical_mic_kill_switch_supported: bool = True
    stt_candidate_required: bool = True
    transcript_read_model_required: bool = True
    always_listening_allowed: bool = False
    wake_word_allowed: bool = False
    background_recording_allowed: bool = False
    hidden_recording_allowed: bool = False
    autonomous_voice_loop_allowed: bool = False
    voice_command_execution_allowed: bool = False
    runtime_start_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False
    shell_allowed: bool = False
    file_edit_allowed: bool = False
    git_allowed: bool = False
    future_always_listening_requested: bool = True
    future_always_listening_requires_owner_voice_gate: bool = True
    future_always_listening_requires_local_vad: bool = True
    future_always_listening_requires_visible_status: bool = True
    future_always_listening_requires_physical_kill_switch: bool = True
    future_always_listening_requires_audit: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_true(self.push_to_talk_allowed, "push_to_talk_allowed")
        _require_true(self.microphone_permission_required, "microphone_permission_required")
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.manual_activation_required, "manual_activation_required")
        _require_true(
            self.physical_mic_kill_switch_supported,
            "physical_mic_kill_switch_supported",
        )
        _require_true(self.stt_candidate_required, "stt_candidate_required")
        _require_true(self.transcript_read_model_required, "transcript_read_model_required")
        _require_false(self.always_listening_allowed, "always_listening_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_false(self.background_recording_allowed, "background_recording_allowed")
        _require_false(self.hidden_recording_allowed, "hidden_recording_allowed")
        _require_false(self.autonomous_voice_loop_allowed, "autonomous_voice_loop_allowed")
        _require_false(
            self.voice_command_execution_allowed,
            "voice_command_execution_allowed",
        )
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.shell_allowed, "shell_allowed")
        _require_false(self.file_edit_allowed, "file_edit_allowed")
        _require_false(self.git_allowed, "git_allowed")
        _require_true(
            self.future_always_listening_requested,
            "future_always_listening_requested",
        )
        _require_true(
            self.future_always_listening_requires_owner_voice_gate,
            "future_always_listening_requires_owner_voice_gate",
        )
        _require_true(
            self.future_always_listening_requires_local_vad,
            "future_always_listening_requires_local_vad",
        )
        _require_true(
            self.future_always_listening_requires_visible_status,
            "future_always_listening_requires_visible_status",
        )
        _require_true(
            self.future_always_listening_requires_physical_kill_switch,
            "future_always_listening_requires_physical_kill_switch",
        )
        _require_true(
            self.future_always_listening_requires_audit,
            "future_always_listening_requires_audit",
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "push_to_talk_allowed": self.push_to_talk_allowed,
            "microphone_permission_required": self.microphone_permission_required,
            "owner_command_required": self.owner_command_required,
            "manual_activation_required": self.manual_activation_required,
            "physical_mic_kill_switch_supported": self.physical_mic_kill_switch_supported,
            "stt_candidate_required": self.stt_candidate_required,
            "transcript_read_model_required": self.transcript_read_model_required,
            "always_listening_allowed": self.always_listening_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "background_recording_allowed": self.background_recording_allowed,
            "hidden_recording_allowed": self.hidden_recording_allowed,
            "autonomous_voice_loop_allowed": self.autonomous_voice_loop_allowed,
            "voice_command_execution_allowed": self.voice_command_execution_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "shell_allowed": self.shell_allowed,
            "file_edit_allowed": self.file_edit_allowed,
            "git_allowed": self.git_allowed,
            "future_always_listening_requested": self.future_always_listening_requested,
            "future_always_listening_requires_owner_voice_gate": (
                self.future_always_listening_requires_owner_voice_gate
            ),
            "future_always_listening_requires_local_vad": (
                self.future_always_listening_requires_local_vad
            ),
            "future_always_listening_requires_visible_status": (
                self.future_always_listening_requires_visible_status
            ),
            "future_always_listening_requires_physical_kill_switch": (
                self.future_always_listening_requires_physical_kill_switch
            ),
            "future_always_listening_requires_audit": (
                self.future_always_listening_requires_audit
            ),
        }


def build_push_to_talk_stt_contract() -> PushToTalkSttContract:
    return PushToTalkSttContract(contract_id="push_to_talk_stt_contract_v0_1")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

