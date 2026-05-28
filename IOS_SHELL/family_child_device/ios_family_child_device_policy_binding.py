from __future__ import annotations

from dataclasses import dataclass

from IOS_SHELL.family_child_device.ios_child_app_control_policy_bridge import (
    IOSChildAppControlPolicyBridge,
)
from IOS_SHELL.family_child_device.ios_child_device_audit_bridge import (
    IOSChildDeviceAuditBridge,
)
from IOS_SHELL.family_child_device.ios_child_device_profile_bridge import (
    IOSChildDeviceProfileBridge,
)
from IOS_SHELL.family_child_device.ios_child_remote_control_intent_bridge import (
    IOSChildRemoteControlIntentBridge,
)
from IOS_SHELL.family_child_device.ios_child_screen_control_policy_bridge import (
    IOSChildScreenControlPolicyBridge,
)
from IOS_SHELL.family_child_device.ios_child_screen_time_policy_bridge import (
    IOSChildScreenTimePolicyBridge,
)
from IOS_SHELL.family_child_device.ios_guardian_authority_bridge import (
    IOSGuardianAuthorityBridge,
)


@dataclass(frozen=True)
class IOSFamilyChildDevicePolicyBinding:
    profile_bridge: IOSChildDeviceProfileBridge
    guardian_authority_bridge: IOSGuardianAuthorityBridge
    screen_control_policy_bridge: IOSChildScreenControlPolicyBridge
    remote_control_intent_bridge: IOSChildRemoteControlIntentBridge
    audit_bridge: IOSChildDeviceAuditBridge
    app_control_policy_bridge: IOSChildAppControlPolicyBridge
    screen_time_policy_bridge: IOSChildScreenTimePolicyBridge
    dashboard_section: str
    policy_projection_only: bool
    ios_platform_api_call_allowed: bool
    runtime_execution_allowed: bool
    dashboard_bypass_allowed: bool
    normal_observer_client_allowed: bool

    def __post_init__(self) -> None:
        if self.dashboard_section != "Family / Children":
            raise ValueError("dashboard_section must be Family / Children")
        if not self.policy_projection_only:
            raise ValueError("policy_projection_only must be True")
        if self.ios_platform_api_call_allowed:
            raise ValueError("ios_platform_api_call_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.normal_observer_client_allowed:
            raise ValueError("normal_observer_client_allowed must be False")

        child_device_id = self.profile_bridge.child_device_id
        child_profile_id = self.profile_bridge.child_profile_id
        guardian_id = self.guardian_authority_bridge.guardian_id

        if self.guardian_authority_bridge.child_profile_id != child_profile_id:
            raise ValueError("guardian authority child_profile_id mismatch")
        if self.remote_control_intent_bridge.child_device_id != child_device_id:
            raise ValueError("remote control intent child_device_id mismatch")
        if self.remote_control_intent_bridge.guardian_id != guardian_id:
            raise ValueError("remote control intent guardian_id mismatch")
        if self.audit_bridge.child_device_id != child_device_id:
            raise ValueError("audit child_device_id mismatch")
        if self.audit_bridge.guardian_id != guardian_id:
            raise ValueError("audit guardian_id mismatch")
        if self.app_control_policy_bridge.child_device_id != child_device_id:
            raise ValueError("app control policy child_device_id mismatch")
        if self.screen_time_policy_bridge.child_device_id != child_device_id:
            raise ValueError("screen time policy child_device_id mismatch")

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "binding": "family_child_device_policy",
            "dashboard_section": self.dashboard_section,
            "policy_projection_only": self.policy_projection_only,
            "ios_platform_api_call_allowed": self.ios_platform_api_call_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "normal_observer_client_allowed": self.normal_observer_client_allowed,
            "profile": self.profile_bridge.to_read_model(),
            "guardian_authority": self.guardian_authority_bridge.to_read_model(),
            "screen_control_policy": self.screen_control_policy_bridge.to_read_model(),
            "remote_control_intent": self.remote_control_intent_bridge.to_read_model(),
            "audit": self.audit_bridge.to_read_model(),
            "app_control_policy": self.app_control_policy_bridge.to_read_model(),
            "screen_time_policy": self.screen_time_policy_bridge.to_read_model(),
        }
