from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_control_policy_contract import (
    ChildScreenControlPolicyContract,
)


@dataclass(frozen=True)
class AndroidChildScreenControlPolicyBridge:
    policy_id: str
    device_profile: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    audit_required: bool
    visible_child_device_status_required: bool
    dashboard_bypass_allowed: bool
    screen_view_allowed_by_guardian_policy: bool
    screenshot_allowed_by_guardian_policy: bool
    screen_recording_allowed_by_guardian_policy: bool
    touch_control_allowed_by_guardian_policy: bool
    keyboard_input_allowed_by_guardian_policy: bool
    android_platform_api_call_allowed: bool
    screen_capture_runtime_allowed: bool
    touch_execution_allowed: bool
    keyboard_execution_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("policy_id", "device_profile"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.device_profile != "child_managed_device":
            raise ValueError("device_profile must be child_managed_device")
        if not self.guardian_authority_verified:
            raise ValueError("guardian_authority_verified must be True")
        if not self.family_policy_enabled:
            raise ValueError("family_policy_enabled must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.visible_child_device_status_required:
            raise ValueError("visible_child_device_status_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.screen_capture_runtime_allowed:
            raise ValueError("screen_capture_runtime_allowed must be False")
        if self.touch_execution_allowed:
            raise ValueError("touch_execution_allowed must be False")
        if self.keyboard_execution_allowed:
            raise ValueError("keyboard_execution_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def build_policy_contract(self) -> ChildScreenControlPolicyContract:
        return ChildScreenControlPolicyContract(
            policy_id=self.policy_id,
            device_profile=self.device_profile,
            guardian_authority_verified=self.guardian_authority_verified,
            family_policy_enabled=self.family_policy_enabled,
            audit_required=self.audit_required,
            visible_child_device_status_required=self.visible_child_device_status_required,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
            screen_view_allowed_by_guardian_policy=self.screen_view_allowed_by_guardian_policy,
            screenshot_allowed_by_guardian_policy=self.screenshot_allowed_by_guardian_policy,
            screen_recording_allowed_by_guardian_policy=self.screen_recording_allowed_by_guardian_policy,
            touch_control_allowed_by_guardian_policy=self.touch_control_allowed_by_guardian_policy,
            keyboard_input_allowed_by_guardian_policy=self.keyboard_input_allowed_by_guardian_policy,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "ANDROID_SHELL",
            "bridge": "child_screen_control_policy",
            "policy_id": self.policy_id,
            "device_profile": self.device_profile,
            "guardian_authority_verified": self.guardian_authority_verified,
            "family_policy_enabled": self.family_policy_enabled,
            "audit_required": self.audit_required,
            "visible_child_device_status_required": self.visible_child_device_status_required,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "screen_view_allowed_by_guardian_policy": self.screen_view_allowed_by_guardian_policy,
            "screenshot_allowed_by_guardian_policy": self.screenshot_allowed_by_guardian_policy,
            "screen_recording_allowed_by_guardian_policy": self.screen_recording_allowed_by_guardian_policy,
            "touch_control_allowed_by_guardian_policy": self.touch_control_allowed_by_guardian_policy,
            "keyboard_input_allowed_by_guardian_policy": self.keyboard_input_allowed_by_guardian_policy,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "screen_capture_runtime_allowed": self.screen_capture_runtime_allowed,
            "touch_execution_allowed": self.touch_execution_allowed,
            "keyboard_execution_allowed": self.keyboard_execution_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
