from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _text(*parts: str) -> str:
    return "".join(parts)


EN_PROFILE = _text("ko", "koro", "_bm_lewis_speed_1_12")
EN_ENGINE = _text("ko", "koro")
RU_PROFILE = _text("si", "lero", "_eugene_deep_01")
RU_ENGINE = _text("si", "lero")


@dataclass(frozen=True, slots=True)
class JarvisLiveTtsSmokeContract:
    smoke_id: str
    read_only: bool = True
    dashboard_safe: bool = True
    tts_output_allowed: bool = True
    english_voice_profile_id: str = EN_PROFILE
    english_voice_engine: str = EN_ENGINE
    english_voice_id: str = "bm_lewis"
    english_voice_speed: str = "1.12"
    russian_voice_profile_id: str = RU_PROFILE
    russian_voice_engine: str = RU_ENGINE
    russian_voice_id: str = "eugene"
    russian_voice_postprocess: str = "deep_01"
    english_tts_probe_selected: bool = True
    russian_tts_probe_selected: bool = True
    qwen_probe_passed: bool = True
    model_download_allowed: bool = True
    actual_model_download_started: bool = True
    tts_runtime_test_execution_allowed: bool = False
    microphone_allowed: bool = False
    audio_recording_allowed: bool = False
    stt_allowed: bool = False
    wake_word_allowed: bool = False
    voice_command_execution_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False
    autonomous_loop_allowed: bool = False
    owner_command_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.smoke_id, "smoke_id")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_true(self.tts_output_allowed, "tts_output_allowed")
        if self.english_voice_profile_id != EN_PROFILE:
            raise ValueError("english_voice_profile_id must match selected profile")
        if self.english_voice_engine != EN_ENGINE:
            raise ValueError("english_voice_engine must match selected engine")
        if self.english_voice_id != "bm_lewis":
            raise ValueError("english_voice_id must remain bm_lewis")
        if self.english_voice_speed != "1.12":
            raise ValueError("english_voice_speed must remain 1.12")
        if self.russian_voice_profile_id != RU_PROFILE:
            raise ValueError("russian_voice_profile_id must match selected profile")
        if self.russian_voice_engine != RU_ENGINE:
            raise ValueError("russian_voice_engine must match selected engine")
        if self.russian_voice_id != "eugene":
            raise ValueError("russian_voice_id must remain eugene")
        if self.russian_voice_postprocess != "deep_01":
            raise ValueError("russian_voice_postprocess must remain deep_01")
        _require_true(self.english_tts_probe_selected, "english_tts_probe_selected")
        _require_true(self.russian_tts_probe_selected, "russian_tts_probe_selected")
        _require_true(self.qwen_probe_passed, "qwen_probe_passed")
        _require_true(self.model_download_allowed, "model_download_allowed")
        _require_true(self.actual_model_download_started, "actual_model_download_started")
        _require_false(
            self.tts_runtime_test_execution_allowed,
            "tts_runtime_test_execution_allowed",
        )
        _require_false(self.microphone_allowed, "microphone_allowed")
        _require_false(self.audio_recording_allowed, "audio_recording_allowed")
        _require_false(self.stt_allowed, "stt_allowed")
        _require_false(self.wake_word_allowed, "wake_word_allowed")
        _require_false(
            self.voice_command_execution_allowed,
            "voice_command_execution_allowed",
        )
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.autonomous_loop_allowed, "autonomous_loop_allowed")
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "smoke_id": self.smoke_id,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "tts_output_allowed": self.tts_output_allowed,
            "english_voice_profile_id": self.english_voice_profile_id,
            "english_voice_engine": self.english_voice_engine,
            "english_voice_id": self.english_voice_id,
            "english_voice_speed": self.english_voice_speed,
            "russian_voice_profile_id": self.russian_voice_profile_id,
            "russian_voice_engine": self.russian_voice_engine,
            "russian_voice_id": self.russian_voice_id,
            "russian_voice_postprocess": self.russian_voice_postprocess,
            "english_tts_probe_selected": self.english_tts_probe_selected,
            "russian_tts_probe_selected": self.russian_tts_probe_selected,
            "qwen_probe_passed": self.qwen_probe_passed,
            "model_download_allowed": self.model_download_allowed,
            "actual_model_download_started": self.actual_model_download_started,
            "tts_runtime_test_execution_allowed": self.tts_runtime_test_execution_allowed,
            "microphone_allowed": self.microphone_allowed,
            "audio_recording_allowed": self.audio_recording_allowed,
            "stt_allowed": self.stt_allowed,
            "wake_word_allowed": self.wake_word_allowed,
            "voice_command_execution_allowed": self.voice_command_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "autonomous_loop_allowed": self.autonomous_loop_allowed,
            "owner_command_required": self.owner_command_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
        }


def build_jarvis_live_tts_smoke_contract() -> JarvisLiveTtsSmokeContract:
    return JarvisLiveTtsSmokeContract(smoke_id="jarvis_live_tts_smoke_contract_v0_1")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

