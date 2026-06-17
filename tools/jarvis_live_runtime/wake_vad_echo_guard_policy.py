from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WakeVadEchoGuardPolicy:
    always_listening_required_for_final: bool
    push_to_talk_allowed_as_final: bool
    wake_word_required: bool
    vad_required: bool
    echo_suppression_required: bool
    raw_audio_storage_allowed: bool
    raw_audio_to_core_allowed: bool

    def __post_init__(self) -> None:
        if not self.always_listening_required_for_final:
            raise ValueError("final voice mode must be always-listening")
        if self.push_to_talk_allowed_as_final:
            raise ValueError("push-to-talk is not allowed as final mode")
        if not self.wake_word_required:
            raise ValueError("wake word gate is required")
        if not self.vad_required:
            raise ValueError("VAD is required")
        if not self.echo_suppression_required:
            raise ValueError("echo suppression is required")
        if self.raw_audio_storage_allowed:
            raise ValueError("raw audio storage must remain false")
        if self.raw_audio_to_core_allowed:
            raise ValueError("raw audio to core must remain false")

    def to_read_model(self) -> dict[str, object]:
        return {
            "always_listening_required_for_final": self.always_listening_required_for_final,
            "push_to_talk_allowed_as_final": self.push_to_talk_allowed_as_final,
            "wake_word_required": self.wake_word_required,
            "vad_required": self.vad_required,
            "echo_suppression_required": self.echo_suppression_required,
            "raw_audio_storage_allowed": self.raw_audio_storage_allowed,
            "raw_audio_to_core_allowed": self.raw_audio_to_core_allowed,
        }


def build_default_wake_vad_echo_guard_policy() -> WakeVadEchoGuardPolicy:
    return WakeVadEchoGuardPolicy(
        always_listening_required_for_final=True,
        push_to_talk_allowed_as_final=False,
        wake_word_required=True,
        vad_required=True,
        echo_suppression_required=True,
        raw_audio_storage_allowed=False,
        raw_audio_to_core_allowed=False,
    )
