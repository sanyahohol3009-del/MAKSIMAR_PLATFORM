from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_app_control_policy_contract import (
    ChildAppControlPolicyContract,
)


@dataclass(frozen=True)
class AndroidChildAppControlPolicyBridge:
    policy_id: str
    child_device_id: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    app_blocking_allowed_by_guardian_policy: bool
    install_approval_required: bool
    audit_required: bool
    dashboard_bypass_allowed: bool
    android_platform_api_call_allowed: bool
    app_control_runtime_allowed: bool
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
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.app_control_runtime_allowed:
            raise ValueError("app_control_runtime_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def build_policy_contract(self) -> ChildAppControlPolicyContract:
        return ChildAppControlPolicyContract(
            policy_id=self.policy_id,
            child_device_id=self.child_device_id,
            guardian_authority_verified=self.guardian_authority_verified,
            family_policy_enabled=self.family_policy_enabled,
            app_blocking_allowed_by_guardian_policy=self.app_blocking_allowed_by_guardian_policy,
            install_approval_required=self.install_approval_required,
            audit_required=self.audit_required,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
            runtime_execution_allowed=self.runtime_execution_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "ANDROID_SHELL",
            "bridge": "child_app_control_policy",
            "policy_id": self.policy_id,
            "child_device_id": self.child_device_id,
            "guardian_authority_verified": self.guardian_authority_verified,
            "family_policy_enabled": self.family_policy_enabled,
            "app_blocking_allowed_by_guardian_policy": self.app_blocking_allowed_by_guardian_policy,
            "install_approval_required": self.install_approval_required,
            "audit_required": self.audit_required,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "app_control_runtime_allowed": self.app_control_runtime_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
