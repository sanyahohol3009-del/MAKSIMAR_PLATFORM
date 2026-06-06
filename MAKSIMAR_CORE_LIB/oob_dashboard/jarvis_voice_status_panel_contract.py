from __future__ import annotations

from dataclasses import dataclass
from typing import Any


BLOCKED_VOICE_PANEL_ACTIONS: tuple[str, ...] = (
    "microphone",
    "stt",
    "tts",
    "wake_word",
    "pc_control",
)


@dataclass(frozen=True, slots=True)
class JarvisVoiceStatusPanelContract:
    panel_id: str
    panel_title: str
    blocked_actions: tuple[str, ...]
    blocked_reason: str
    read_only: bool = True
    dashboard_safe: bool = True
    voice_runtime_enabled: bool = False
    audio_runtime_enabled: bool = False
    dashboard_execution_allowed: bool = False
    microphone_toggle_allowed: bool = False
    stt_toggle_allowed: bool = False
    tts_toggle_allowed: bool = False
    wake_word_toggle_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.panel_title, "panel_title")
        _require_non_empty_tuple(self.blocked_actions, "blocked_actions")
        if self.blocked_actions != BLOCKED_VOICE_PANEL_ACTIONS:
            raise ValueError("blocked_actions must include all voice and pc_control actions")
        _require_non_empty(self.blocked_reason, "blocked_reason")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.voice_runtime_enabled, "voice_runtime_enabled")
        _require_false(self.audio_runtime_enabled, "audio_runtime_enabled")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.microphone_toggle_allowed, "microphone_toggle_allowed")
        _require_false(self.stt_toggle_allowed, "stt_toggle_allowed")
        _require_false(self.tts_toggle_allowed, "tts_toggle_allowed")
        _require_false(self.wake_word_toggle_allowed, "wake_word_toggle_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "panel_title": self.panel_title,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "voice_runtime_enabled": self.voice_runtime_enabled,
            "audio_runtime_enabled": self.audio_runtime_enabled,
            "blocked_actions": self.blocked_actions,
            "blocked_reason": self.blocked_reason,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "microphone_toggle_allowed": self.microphone_toggle_allowed,
            "stt_toggle_allowed": self.stt_toggle_allowed,
            "tts_toggle_allowed": self.tts_toggle_allowed,
            "wake_word_toggle_allowed": self.wake_word_toggle_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


def build_jarvis_voice_status_panel_contract(
    voice_status_payload: dict[str, Any],
) -> JarvisVoiceStatusPanelContract:
    blocked_reason = str(
        voice_status_payload.get(
            "blocked_reason",
            "JARVIS-LIVE voice runtime is disabled.",
        )
    )
    return JarvisVoiceStatusPanelContract(
        panel_id="jarvis_voice_status_panel",
        panel_title="JARVIS-LIVE Voice Status",
        blocked_actions=BLOCKED_VOICE_PANEL_ACTIONS,
        blocked_reason=blocked_reason,
    )


def build_jarvis_voice_status_panel_read_model(
    voice_status_payload: dict[str, Any],
) -> dict[str, Any]:
    return build_jarvis_voice_status_panel_contract(voice_status_payload).to_read_model()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    for item in value:
        _require_non_empty(item, field_name)


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

