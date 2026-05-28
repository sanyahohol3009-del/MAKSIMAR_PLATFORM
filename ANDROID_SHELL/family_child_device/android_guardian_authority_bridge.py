from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)


@dataclass(frozen=True)
class AndroidGuardianAuthorityBridge:
    guardian_id: str
    child_profile_id: str
    guardian_authority_verified: bool
    authority_scope: str
    audit_required: bool
    expires_epoch_ms: int
    dashboard_bypass_allowed: bool
    android_platform_api_call_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("guardian_id", "child_profile_id", "authority_scope"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not self.guardian_authority_verified:
            raise ValueError("guardian_authority_verified must be True")
        if self.authority_scope != "family_child_device_control":
            raise ValueError("authority_scope must be family_child_device_control")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not isinstance(self.expires_epoch_ms, int) or self.expires_epoch_ms <= 0:
            raise ValueError("expires_epoch_ms must be a positive integer")
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

    def build_authority_contract(self) -> GuardianAuthorityContract:
        return GuardianAuthorityContract(
            guardian_id=self.guardian_id,
            child_profile_id=self.child_profile_id,
            guardian_authority_verified=self.guardian_authority_verified,
            authority_scope=self.authority_scope,
            audit_required=self.audit_required,
            expires_epoch_ms=self.expires_epoch_ms,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "ANDROID_SHELL",
            "bridge": "guardian_authority",
            "guardian_id": self.guardian_id,
            "child_profile_id": self.child_profile_id,
            "guardian_authority_verified": self.guardian_authority_verified,
            "authority_scope": self.authority_scope,
            "audit_required": self.audit_required,
            "expires_epoch_ms": self.expires_epoch_ms,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
