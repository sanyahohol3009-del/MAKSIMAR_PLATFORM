from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChildScreenTimePolicyContract:
    policy_id: str
    child_device_id: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    daily_limit_minutes: int
    emergency_lock_allowed_by_guardian_policy: bool
    audit_required: bool
    dashboard_bypass_allowed: bool
    runtime_execution_allowed: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if not self.child_device_id.strip():
            raise ValueError("child_device_id must be non-empty")
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
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False in BATCH 4.2")

    def is_screen_time_limited(self) -> bool:
        return self.daily_limit_minutes > 0
