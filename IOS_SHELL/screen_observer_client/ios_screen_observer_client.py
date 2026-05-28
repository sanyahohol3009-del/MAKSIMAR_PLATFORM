from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)


@dataclass(frozen=True)
class IOSScreenObserverClient:
    device_id: str
    owner_identity_id: str
    device_type: str
    read_only: bool
    consent_required: bool
    audit_required: bool
    frame_reference_only: bool
    direct_screen_capture_allowed: bool
    screenshot_runtime_allowed: bool
    screen_recording_runtime_allowed: bool
    replaykit_allowed: bool
    accessibility_api_allowed: bool
    remote_control_allowed: bool
    child_control_enabled: bool
    touch_injection_allowed: bool
    keyboard_injection_allowed: bool
    gesture_injection_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("device_id", "owner_identity_id", "device_type"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.device_type != "ios":
            raise ValueError("device_type must be ios")
        if not self.read_only:
            raise ValueError("normal iOS observer must be read-only")
        if not self.consent_required:
            raise ValueError("consent_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.frame_reference_only:
            raise ValueError("frame_reference_only must be True")
        if self.direct_screen_capture_allowed:
            raise ValueError("direct_screen_capture_allowed must be False")
        if self.screenshot_runtime_allowed:
            raise ValueError("screenshot_runtime_allowed must be False")
        if self.screen_recording_runtime_allowed:
            raise ValueError("screen_recording_runtime_allowed must be False")
        if self.replaykit_allowed:
            raise ValueError("replaykit_allowed must be False")
        if self.accessibility_api_allowed:
            raise ValueError("accessibility_api_allowed must be False")
        if self.remote_control_allowed:
            raise ValueError("remote_control_allowed must be False")
        if self.child_control_enabled:
            raise ValueError("normal iOS observer cannot enable child control")
        if self.touch_injection_allowed:
            raise ValueError("touch_injection_allowed must be False")
        if self.keyboard_injection_allowed:
            raise ValueError("keyboard_injection_allowed must be False")
        if self.gesture_injection_allowed:
            raise ValueError("gesture_injection_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    @classmethod
    def default(cls, *, device_id: str, owner_identity_id: str) -> "IOSScreenObserverClient":
        return cls(
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            device_type="ios",
            read_only=True,
            consent_required=True,
            audit_required=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=False,
            screenshot_runtime_allowed=False,
            screen_recording_runtime_allowed=False,
            replaykit_allowed=False,
            accessibility_api_allowed=False,
            remote_control_allowed=False,
            child_control_enabled=False,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            gesture_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )

    def build_session_contract(
        self,
        *,
        session_id: str,
        session_state: str = "consent_required",
    ) -> MobileScreenSessionContract:
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")

        return MobileScreenSessionContract(
            session_id=session_id,
            device_id=self.device_id,
            owner_identity_id=self.owner_identity_id,
            device_type=self.device_type,
            session_state=session_state,
            consent_required=self.consent_required,
            audit_required=self.audit_required,
            read_only=self.read_only,
            frame_reference_only=self.frame_reference_only,
            direct_screen_capture_allowed=self.direct_screen_capture_allowed,
            remote_control_allowed=self.remote_control_allowed,
            touch_injection_allowed=self.touch_injection_allowed,
            keyboard_injection_allowed=self.keyboard_injection_allowed,
            external_network_access_allowed=self.external_network_access_allowed,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            core_write_allowed=self.core_write_allowed,
            source_of_truth_override_allowed=self.source_of_truth_override_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "client": "screen_observer_client",
            "device_id": self.device_id,
            "owner_identity_id": self.owner_identity_id,
            "device_type": self.device_type,
            "read_only": self.read_only,
            "consent_required": self.consent_required,
            "audit_required": self.audit_required,
            "frame_reference_only": self.frame_reference_only,
            "direct_screen_capture_allowed": self.direct_screen_capture_allowed,
            "screenshot_runtime_allowed": self.screenshot_runtime_allowed,
            "screen_recording_runtime_allowed": self.screen_recording_runtime_allowed,
            "replaykit_allowed": self.replaykit_allowed,
            "accessibility_api_allowed": self.accessibility_api_allowed,
            "remote_control_allowed": self.remote_control_allowed,
            "child_control_enabled": self.child_control_enabled,
            "touch_injection_allowed": self.touch_injection_allowed,
            "keyboard_injection_allowed": self.keyboard_injection_allowed,
            "gesture_injection_allowed": self.gesture_injection_allowed,
            "external_network_access_allowed": self.external_network_access_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
