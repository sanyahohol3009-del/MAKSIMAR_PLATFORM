from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_BINDS_TO_EXISTING_SURFACES = (
    "MAKSIMAR_CORE_LIB/real_voice_runtime",
    "VOICE_LAYER",
    "MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF",
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
class VoiceCloneBackendAdapterContract:
    contract_id: str
    adapter_kind: str
    input_payload_kind: str
    output_payload_kind: str
    safe_text_response_candidate_only: bool = True
    speech_response_candidate_metadata_only: bool = True
    playback_runtime_started: bool = False
    voice_clone_runtime_enabled: bool = False
    raw_audio_output_allowed_by_default: bool = False
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
        _require_true(
            self.safe_text_response_candidate_only,
            "safe_text_response_candidate_only",
        )
        _require_true(
            self.speech_response_candidate_metadata_only,
            "speech_response_candidate_metadata_only",
        )
        _require_false(self.playback_runtime_started, "playback_runtime_started")
        _require_false(self.voice_clone_runtime_enabled, "voice_clone_runtime_enabled")
        _require_false(
            self.raw_audio_output_allowed_by_default,
            "raw_audio_output_allowed_by_default",
        )
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
            raise ValueError(
                "binds_to_existing_surfaces must match canonical voice clone bindings"
            )
        if self.input_payload_kind != "safe_text_response_candidate":
            raise ValueError("input_payload_kind must remain safe_text_response_candidate")
        if self.output_payload_kind != "speech_audio_response_candidate_metadata":
            raise ValueError(
                "output_payload_kind must remain speech_audio_response_candidate_metadata"
            )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "adapter_kind": self.adapter_kind,
            "input_payload_kind": self.input_payload_kind,
            "output_payload_kind": self.output_payload_kind,
            "safe_text_response_candidate_only": self.safe_text_response_candidate_only,
            "speech_response_candidate_metadata_only": self.speech_response_candidate_metadata_only,
            "playback_runtime_started": self.playback_runtime_started,
            "voice_clone_runtime_enabled": self.voice_clone_runtime_enabled,
            "raw_audio_output_allowed_by_default": self.raw_audio_output_allowed_by_default,
            "model_download_allowed": self.model_download_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "action_execution_allowed": self.action_execution_allowed,
            "proposal_only": self.proposal_only,
            "binds_to_existing_surfaces": self.binds_to_existing_surfaces,
        }


def build_voice_clone_backend_adapter_contract() -> VoiceCloneBackendAdapterContract:
    return VoiceCloneBackendAdapterContract(
        contract_id="voice_clone_backend_adapter_contract_v0_1",
        adapter_kind="voice_clone_backend_adapter",
        input_payload_kind="safe_text_response_candidate",
        output_payload_kind="speech_audio_response_candidate_metadata",
    )
