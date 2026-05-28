from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_time_policy_contract import (
    ChildScreenTimePolicyContract,
)


@dataclass(frozen=True)
class IOSChildScreenTimePolicyBridge:
    policy_id: str
    child_device_id: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    daily_limit_minutes: int
    emergency_lock_allowed_by_guardian_policy: bool
    audit_required: bool
    dashboard_bypass_allowed: bool
    ios_platform_api_call_allowed: bool
    screen_time_enforcement_runtime_allowed: bool
    emergency_lock_runtime_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("policy_id", "child_device_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not self.guardian_authority_verified:
            raise ValueError("guardian_authority_verified must be True")
        if not self.family_policy_enabled:
            raise ValueError("family_policy_enabled must be True")
        if not isinstance(self.daily_limit_minutes, int) or self.daily_limit_minutes < 0:
            raise ValueError("daily_limit_minutes must be a non-negative integer")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.ios_platform_api_call_allowed:
            raise ValueError("ios_platform_api_call_allowed must be False")
        if self.screen_time_enforcement_runtime_allowed:
            raise ValueError("screen_time_enforcement_runtime_allowed must be False")
        if self.emergency_lock_runtime_allowed:
            raise ValueError("emergency_lock_runtime_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def build_policy_contract(self) -> ChildScreenTimePolicyContract:
        return ChildScreenTimePolicyContract(
            policy_id=self.policy_id,
            child_device_id=self.child_device_id,
            guardian_authority_verified=self.guardian_authority_verified,
            family_policy_enabled=self.family_policy_enabled,
            daily_limit_minutes=self.daily_limit_minutes,
            emergency_lock_allowed_by_guardian_policy=self.emergency_lock_allowed_by_guardian_policy,
            audit_required=self.audit_required,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
            runtime_execution_allowed=self.runtime_execution_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "bridge": "child_screen_time_policy",
            "policy_id": self.policy_id,
            "child_device_id": self.child_device_id,
            "guardian_authority_verified": self.guardian_authority_verified,
            "family_policy_enabled": self.family_policy_enabled,
            "daily_limit_minutes": self.daily_limit_minutes,
            "emergency_lock_allowed_by_guardian_policy": self.emergency_lock_allowed_by_guardian_policy,
            "audit_required": self.audit_required,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "ios_platform_api_call_allowed": self.ios_platform_api_call_allowed,
            "screen_time_enforcement_runtime_allowed": self.screen_time_enforcement_runtime_allowed,
            "emergency_lock_runtime_allowed": self.emergency_lock_runtime_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
