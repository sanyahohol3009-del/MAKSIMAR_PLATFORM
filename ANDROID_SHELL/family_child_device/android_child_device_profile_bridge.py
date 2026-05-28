from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)


@dataclass(frozen=True)
class AndroidChildDeviceProfileBridge:
    child_device_id: str
    child_profile_id: str
    device_profile: str
    family_policy_enabled: bool
    visible_child_device_status_required: bool
    audit_required: bool
    dashboard_bypass_allowed: bool
    android_platform_api_call_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("child_device_id", "child_profile_id", "device_profile"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.device_profile != "child_managed_device":
            raise ValueError("device_profile must be child_managed_device")
        if not self.family_policy_enabled:
            raise ValueError("family_policy_enabled must be True")
        if not self.visible_child_device_status_required:
            raise ValueError("visible_child_device_status_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")

    @classmethod
    def default(
        cls,
        *,
        child_device_id: str,
        child_profile_id: str,
    ) -> "AndroidChildDeviceProfileBridge":
        return cls(
            child_device_id=child_device_id,
            child_profile_id=child_profile_id,
            device_profile="child_managed_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )

    def build_profile_contract(self) -> ChildDeviceProfileContract:
        return ChildDeviceProfileContract(
            child_device_id=self.child_device_id,
            child_profile_id=self.child_profile_id,
            device_profile=self.device_profile,
            family_policy_enabled=self.family_policy_enabled,
            visible_child_device_status_required=self.visible_child_device_status_required,
            audit_required=self.audit_required,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "ANDROID_SHELL",
            "bridge": "family_child_device_profile",
            "dashboard_section": "Family / Children",
            "child_device_id": self.child_device_id,
            "child_profile_id": self.child_profile_id,
            "device_profile": self.device_profile,
            "family_policy_enabled": self.family_policy_enabled,
            "visible_child_device_status_required": self.visible_child_device_status_required,
            "audit_required": self.audit_required,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
        }
