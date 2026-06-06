from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisLiveReadinessFlags:
    voice_gate_ready: bool
    owner_identity_gate_ready: bool
    action_allowlist_ready: bool
    approval_binding_ready: bool
    audit_binding_ready: bool
    dashboard_status_ready: bool
    model_storage_boundary_ready: bool
    runtime_vendor_boundary_ready: bool

    @property
    def all_ready(self) -> bool:
        return all(
            (
                self.voice_gate_ready,
                self.owner_identity_gate_ready,
                self.action_allowlist_ready,
                self.approval_binding_ready,
                self.audit_binding_ready,
                self.dashboard_status_ready,
                self.model_storage_boundary_ready,
                self.runtime_vendor_boundary_ready,
            )
        )

    @property
    def missing_gate_names(self) -> tuple[str, ...]:
        missing: list[str] = []
        for field_name in (
            "voice_gate_ready",
            "owner_identity_gate_ready",
            "action_allowlist_ready",
            "approval_binding_ready",
            "audit_binding_ready",
            "dashboard_status_ready",
            "model_storage_boundary_ready",
            "runtime_vendor_boundary_ready",
        ):
            if getattr(self, field_name) is not True:
                missing.append(field_name)
        return tuple(missing)

    def to_read_model(self) -> dict[str, object]:
        return {
            "voice_gate_ready": self.voice_gate_ready,
            "owner_identity_gate_ready": self.owner_identity_gate_ready,
            "action_allowlist_ready": self.action_allowlist_ready,
            "approval_binding_ready": self.approval_binding_ready,
            "audit_binding_ready": self.audit_binding_ready,
            "dashboard_status_ready": self.dashboard_status_ready,
            "model_storage_boundary_ready": self.model_storage_boundary_ready,
            "runtime_vendor_boundary_ready": self.runtime_vendor_boundary_ready,
            "all_ready": self.all_ready,
            "missing_gate_names": self.missing_gate_names,
        }


@dataclass(frozen=True, slots=True)
class JarvisLiveDisabledGateContract:
    gate_id: str
    readiness: JarvisLiveReadinessFlags
    jarvis_live_enabled: bool
    microphone_enabled: bool
    stt_runtime_enabled: bool
    tts_playback_enabled: bool
    wake_word_enabled: bool
    pc_control_enabled: bool
    model_download_allowed: bool
    network_access_allowed: bool
    runtime_start_allowed: bool
    denied_reasons: tuple[str, ...]
    dashboard_safe: bool
    read_only: bool

    def __post_init__(self) -> None:
        _validate_non_empty("gate_id", self.gate_id)
        if not isinstance(self.readiness, JarvisLiveReadinessFlags):
            raise TypeError("readiness must be JarvisLiveReadinessFlags")
        _validate_false("jarvis_live_enabled", self.jarvis_live_enabled)
        _validate_false("microphone_enabled", self.microphone_enabled)
        _validate_false("stt_runtime_enabled", self.stt_runtime_enabled)
        _validate_false("tts_playback_enabled", self.tts_playback_enabled)
        _validate_false("wake_word_enabled", self.wake_word_enabled)
        _validate_false("pc_control_enabled", self.pc_control_enabled)
        _validate_false("model_download_allowed", self.model_download_allowed)
        _validate_false("network_access_allowed", self.network_access_allowed)
        _validate_false("runtime_start_allowed", self.runtime_start_allowed)
        _validate_non_empty_tuple("denied_reasons", self.denied_reasons)
        for missing_gate in self.readiness.missing_gate_names:
            if missing_gate not in self.denied_reasons:
                raise ValueError(f"denied_reasons must include missing gate: {missing_gate}")
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)

    @property
    def live_runtime_ready(self) -> bool:
        return (
            self.readiness.all_ready
            and not self.jarvis_live_enabled
            and not self.microphone_enabled
            and not self.stt_runtime_enabled
            and not self.tts_playback_enabled
            and not self.wake_word_enabled
            and not self.pc_control_enabled
            and not self.model_download_allowed
            and not self.network_access_allowed
            and not self.runtime_start_allowed
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "readiness": self.readiness.to_read_model(),
            "jarvis_live_enabled": self.jarvis_live_enabled,
            "microphone_enabled": self.microphone_enabled,
            "stt_runtime_enabled": self.stt_runtime_enabled,
            "tts_playback_enabled": self.tts_playback_enabled,
            "wake_word_enabled": self.wake_word_enabled,
            "pc_control_enabled": self.pc_control_enabled,
            "model_download_allowed": self.model_download_allowed,
            "network_access_allowed": self.network_access_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "live_runtime_ready": self.live_runtime_ready,
            "denied_reasons": self.denied_reasons,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
        }


def build_jarvis_live_disabled_gate_contract() -> JarvisLiveDisabledGateContract:
    readiness = JarvisLiveReadinessFlags(
        voice_gate_ready=False,
        owner_identity_gate_ready=False,
        action_allowlist_ready=False,
        approval_binding_ready=False,
        audit_binding_ready=False,
        dashboard_status_ready=False,
        model_storage_boundary_ready=False,
        runtime_vendor_boundary_ready=False,
    )

    return JarvisLiveDisabledGateContract(
        gate_id="jarvis_live_disabled_gate_contract_v1",
        readiness=readiness,
        jarvis_live_enabled=False,
        microphone_enabled=False,
        stt_runtime_enabled=False,
        tts_playback_enabled=False,
        wake_word_enabled=False,
        pc_control_enabled=False,
        model_download_allowed=False,
        network_access_allowed=False,
        runtime_start_allowed=False,
        denied_reasons=(
            "voice_gate_ready",
            "owner_identity_gate_ready",
            "action_allowlist_ready",
            "approval_binding_ready",
            "audit_binding_ready",
            "dashboard_status_ready",
            "model_storage_boundary_ready",
            "runtime_vendor_boundary_ready",
            "jarvis_live_disabled_by_default",
        ),
        dashboard_safe=True,
        read_only=True,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
