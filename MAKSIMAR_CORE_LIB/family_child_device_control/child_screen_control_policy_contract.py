from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChildScreenControlPolicyContract:
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

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
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

    def allows_interactive_control(self) -> bool:
        return self.touch_control_allowed_by_guardian_policy or self.keyboard_input_allowed_by_guardian_policy
