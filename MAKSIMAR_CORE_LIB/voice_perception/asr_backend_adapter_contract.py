from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_BINDS_TO_EXISTING_SURFACES = (
    "MAKSIMAR_CORE_LIB/real_voice_runtime",
    "VOICE_LAYER",
    "MAKSIMAR_SERVER/VOICE_ROUTING",
)


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
class AsrBackendAdapterContract:
    contract_id: str
    adapter_kind: str
    input_payload_kind: str
    output_payload_kind: str
    transcript_source_metadata_only: bool = True
    audio_candidate_metadata_only: bool = True
    outputs_text_transcript_only: bool = True
    outputs_text_intent_candidate_only: bool = True
    raw_audio_allowed_by_default: bool = False
    microphone_runtime_started: bool = False
    always_listening_allowed: bool = False
    wake_word_allowed: bool = False
    model_download_allowed: bool = False
    shell_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    pc_control_allowed: bool = False
    direct_mobile_control_allowed: bool = False
    action_execution_allowed: bool = False
    proposal_only: bool = True
    binds_to_existing_surfaces: tuple[str, ...] = _BINDS_TO_EXISTING_SURFACES

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.adapter_kind, "adapter_kind")
        _require_non_empty(self.input_payload_kind, "input_payload_kind")
        _require_non_empty(self.output_payload_kind, "output_payload_kind")
        _require_true(self.transcript_source_metadata_only, "transcript_source_metadata_only")
        _require_true(self.audio_candidate_metadata_only, "audio_candidate_metadata_only")
        _require_true(self.outputs_text_transcript_only, "outputs_text_transcript_only")
        _require_true(
            self.outputs_text_intent_candidate_only,
            "outputs_text_intent_candidate_only",
        )
        _require_false(self.raw_audio_allowed_by_default, "raw_audio_allowed_by_default")
        _require_false(self.microphone_runtime_started, "microphone_runtime_started")
        _require_false(self.always_listening_allowed, "always_listening_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.action_execution_allowed, "action_execution_allowed")
        _require_true(self.proposal_only, "proposal_only")
        if self.binds_to_existing_surfaces != _BINDS_TO_EXISTING_SURFACES:
            raise ValueError("binds_to_existing_surfaces must match canonical ASR bindings")
        if self.input_payload_kind != "audio_candidate_metadata_or_transcript_source_metadata":
            raise ValueError("input_payload_kind must remain metadata-only")
        if self.output_payload_kind != "text_transcript_or_text_intent_candidate":
            raise ValueError("output_payload_kind must remain text-only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "adapter_kind": self.adapter_kind,
            "input_payload_kind": self.input_payload_kind,
            "output_payload_kind": self.output_payload_kind,
            "transcript_source_metadata_only": self.transcript_source_metadata_only,
            "audio_candidate_metadata_only": self.audio_candidate_metadata_only,
            "outputs_text_transcript_only": self.outputs_text_transcript_only,
            "outputs_text_intent_candidate_only": self.outputs_text_intent_candidate_only,
            "raw_audio_allowed_by_default": self.raw_audio_allowed_by_default,
            "microphone_runtime_started": self.microphone_runtime_started,
            "always_listening_allowed": self.always_listening_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "model_download_allowed": self.model_download_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "action_execution_allowed": self.action_execution_allowed,
            "proposal_only": self.proposal_only,
            "binds_to_existing_surfaces": self.binds_to_existing_surfaces,
        }


def build_asr_backend_adapter_contract() -> AsrBackendAdapterContract:
    return AsrBackendAdapterContract(
        contract_id="asr_backend_adapter_contract_v0_1",
        adapter_kind="asr_backend_adapter",
        input_payload_kind="audio_candidate_metadata_or_transcript_source_metadata",
        output_payload_kind="text_transcript_or_text_intent_candidate",
    )
