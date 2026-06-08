from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisLiveVoiceReplyContract:
    contract_id: str = "jarvis_live_voice_reply_v0_1"
    voice_profile_id: str = "silero_eugene_deep_01"
    default_reply_text: str = "Александр, я тебя слышу. JARVIS Live готов."
    local_tts_reply_allowed: bool = True
    voice_sample_playback_allowed: bool = True
    reply_state_required: bool = True
    owner_addressing_required: bool = True
    audible_confirmation_required: bool = True
    cloud_tts_allowed: bool = False
    hidden_audio_allowed: bool = False
    pc_control_allowed: bool = False
    network_stream_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.voice_profile_id, "voice_profile_id")
        _require_non_empty(self.default_reply_text, "default_reply_text")
        if "Александр" not in self.default_reply_text:
            raise ValueError("default_reply_text must address the owner")
        for field_name in (
            "local_tts_reply_allowed",
            "voice_sample_playback_allowed",
            "reply_state_required",
            "owner_addressing_required",
            "audible_confirmation_required",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "cloud_tts_allowed",
            "hidden_audio_allowed",
            "pc_control_allowed",
            "network_stream_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "voice_profile_id": self.voice_profile_id,
            "default_reply_text": self.default_reply_text,
            "local_tts_reply_allowed": self.local_tts_reply_allowed,
            "voice_sample_playback_allowed": self.voice_sample_playback_allowed,
            "reply_state_required": self.reply_state_required,
            "owner_addressing_required": self.owner_addressing_required,
            "audible_confirmation_required": self.audible_confirmation_required,
            "cloud_tts_allowed": self.cloud_tts_allowed,
            "hidden_audio_allowed": self.hidden_audio_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "network_stream_allowed": self.network_stream_allowed,
        }


def build_jarvis_live_voice_reply_contract() -> JarvisLiveVoiceReplyContract:
    return JarvisLiveVoiceReplyContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")
