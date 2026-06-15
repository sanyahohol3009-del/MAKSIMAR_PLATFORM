from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")


@dataclass(frozen=True, slots=True)
class MoonshineAndroidAdapterContract:
    contract_id: str
    adapter_kind: str
    local_asr_candidate: bool = True
    transcript_output_only: bool = True
    text_intent_output_only: bool = True
    raw_audio_stream_allowed: bool = False
    raw_audio_persistence_allowed: bool = False
    microphone_runtime_started: bool = False
    always_listening_allowed: bool = False
    wake_word_allowed: bool = False
    model_download_allowed: bool = False
    local_model_runtime_enabled: bool = False
    junior_ai_runtime_enabled: bool = False
    shell_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    pc_control_allowed: bool = False
    direct_mobile_control_allowed: bool = False
    action_execution_allowed: bool = False
    proposal_only: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.adapter_kind, "adapter_kind")
        _require_true(self.local_asr_candidate, "local_asr_candidate")
        _require_true(self.transcript_output_only, "transcript_output_only")
        _require_true(self.text_intent_output_only, "text_intent_output_only")
        _require_false(self.raw_audio_stream_allowed, "raw_audio_stream_allowed")
        _require_false(
            self.raw_audio_persistence_allowed,
            "raw_audio_persistence_allowed",
        )
        _require_false(self.microphone_runtime_started, "microphone_runtime_started")
        _require_false(self.always_listening_allowed, "always_listening_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(
            self.local_model_runtime_enabled,
            "local_model_runtime_enabled",
        )
        _require_false(self.junior_ai_runtime_enabled, "junior_ai_runtime_enabled")
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.action_execution_allowed, "action_execution_allowed")
        _require_true(self.proposal_only, "proposal_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "adapter_kind": self.adapter_kind,
            "local_asr_candidate": self.local_asr_candidate,
            "transcript_output_only": self.transcript_output_only,
            "text_intent_output_only": self.text_intent_output_only,
            "raw_audio_stream_allowed": self.raw_audio_stream_allowed,
            "raw_audio_persistence_allowed": self.raw_audio_persistence_allowed,
            "microphone_runtime_started": self.microphone_runtime_started,
            "always_listening_allowed": self.always_listening_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "model_download_allowed": self.model_download_allowed,
            "local_model_runtime_enabled": self.local_model_runtime_enabled,
            "junior_ai_runtime_enabled": self.junior_ai_runtime_enabled,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "action_execution_allowed": self.action_execution_allowed,
            "proposal_only": self.proposal_only,
        }


def build_moonshine_android_adapter_contract() -> MoonshineAndroidAdapterContract:
    return MoonshineAndroidAdapterContract(
        contract_id="moonshine_android_adapter_contract_v0_1",
        adapter_kind="moonshine_android_local_asr_candidate",
    )
