from __future__ import annotations

from dataclasses import dataclass
from typing import Any


VOICE_STATUS_VALUES: tuple[str, ...] = ("disabled", "blocked")
VOICE_COMPONENT_IDS: tuple[str, ...] = (
    "microphone",
    "stt",
    "tts",
    "wake_word",
    "owner_voice_gate",
    "voice_runtime",
)
DEFAULT_DISABLED_REASON = (
    "JARVIS-LIVE voice runtime is disabled until voice gate, approval, audit, "
    "allowlist, and dashboard status batches are ready."
)


@dataclass(frozen=True, slots=True)
class JarvisLiveVoiceRuntimeFlags:
    microphone_runtime_enabled: bool = False
    stt_runtime_enabled: bool = False
    tts_runtime_enabled: bool = False
    wake_word_runtime_enabled: bool = False
    audio_device_open_allowed: bool = False
    voice_runtime_start_allowed: bool = False
    model_download_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        _require_false(self.microphone_runtime_enabled, "microphone_runtime_enabled")
        _require_false(self.stt_runtime_enabled, "stt_runtime_enabled")
        _require_false(self.tts_runtime_enabled, "tts_runtime_enabled")
        _require_false(self.wake_word_runtime_enabled, "wake_word_runtime_enabled")
        _require_false(self.audio_device_open_allowed, "audio_device_open_allowed")
        _require_false(self.voice_runtime_start_allowed, "voice_runtime_start_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")

    def to_read_model(self) -> dict[str, bool]:
        return {
            "microphone_runtime_enabled": self.microphone_runtime_enabled,
            "stt_runtime_enabled": self.stt_runtime_enabled,
            "tts_runtime_enabled": self.tts_runtime_enabled,
            "wake_word_runtime_enabled": self.wake_word_runtime_enabled,
            "audio_device_open_allowed": self.audio_device_open_allowed,
            "voice_runtime_start_allowed": self.voice_runtime_start_allowed,
            "model_download_allowed": self.model_download_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


@dataclass(frozen=True, slots=True)
class JarvisLiveVoiceComponentStatus:
    component_id: str
    status: str = "disabled"
    disabled_reason: str = DEFAULT_DISABLED_REASON
    blocked_reason: str = DEFAULT_DISABLED_REASON

    def __post_init__(self) -> None:
        _require_member(self.component_id, VOICE_COMPONENT_IDS, "component_id")
        _require_member(self.status, VOICE_STATUS_VALUES, "status")
        _require_non_empty(self.disabled_reason, "disabled_reason")
        _require_non_empty(self.blocked_reason, "blocked_reason")

    def to_read_model(self) -> dict[str, str]:
        return {
            "component_id": self.component_id,
            "status": self.status,
            "disabled_reason": self.disabled_reason,
            "blocked_reason": self.blocked_reason,
        }


@dataclass(frozen=True, slots=True)
class JarvisLiveVoiceDisabledStatus:
    status_id: str
    flags: JarvisLiveVoiceRuntimeFlags
    components: tuple[JarvisLiveVoiceComponentStatus, ...]
    owner_voice_gate_ready: bool = False
    voice_allowed: bool = False
    disabled_reason: str = DEFAULT_DISABLED_REASON
    blocked_reason: str = DEFAULT_DISABLED_REASON

    def __post_init__(self) -> None:
        _require_non_empty(self.status_id, "status_id")
        if not self.components:
            raise ValueError("components must not be empty")
        component_ids = tuple(component.component_id for component in self.components)
        if component_ids != VOICE_COMPONENT_IDS:
            raise ValueError("components must cover every voice component in order")
        _require_false(self.owner_voice_gate_ready, "owner_voice_gate_ready")
        _require_false(self.voice_allowed, "voice_allowed")
        _require_non_empty(self.disabled_reason, "disabled_reason")
        _require_non_empty(self.blocked_reason, "blocked_reason")

    def to_read_model(self) -> dict[str, Any]:
        flag_read_model = self.flags.to_read_model()
        return {
            "status_id": self.status_id,
            "components": tuple(component.to_read_model() for component in self.components),
            "microphone": self._component_read_model("microphone"),
            "stt": self._component_read_model("stt"),
            "tts": self._component_read_model("tts"),
            "wake_word": self._component_read_model("wake_word"),
            "owner_voice_gate": self._component_read_model("owner_voice_gate"),
            "voice_runtime": self._component_read_model("voice_runtime"),
            "owner_voice_gate_ready": self.owner_voice_gate_ready,
            "voice_allowed": self.voice_allowed,
            "disabled_reason": self.disabled_reason,
            "blocked_reason": self.blocked_reason,
            **flag_read_model,
        }

    def _component_read_model(self, component_id: str) -> dict[str, str]:
        for component in self.components:
            if component.component_id == component_id:
                return component.to_read_model()
        raise ValueError(f"unknown voice component: {component_id}")


def build_default_jarvis_live_voice_disabled_status() -> JarvisLiveVoiceDisabledStatus:
    return JarvisLiveVoiceDisabledStatus(
        status_id="jarvis_live_voice_disabled_status_v0_1",
        flags=JarvisLiveVoiceRuntimeFlags(),
        components=tuple(
            JarvisLiveVoiceComponentStatus(component_id=component_id)
            for component_id in VOICE_COMPONENT_IDS
        ),
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

