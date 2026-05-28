from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_time_policy_contract import (
    ChildScreenTimePolicyContract,
)


@dataclass(frozen=True)
class ChildScreenTimeDecision:
    policy_id: str
    daily_limit_minutes: int
    screen_time_limited: bool
    emergency_lock_policy_allowed: bool
    runtime_execution_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "daily_limit_minutes": self.daily_limit_minutes,
            "screen_time_limited": self.screen_time_limited,
            "emergency_lock_policy_allowed": self.emergency_lock_policy_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ChildScreenTimePolicyRuntime:
    def evaluate(self, policy: ChildScreenTimePolicyContract) -> ChildScreenTimeDecision:
        if policy.runtime_execution_allowed:
            raise ValueError("screen-time runtime execution is forbidden in BATCH 4.3")
        return ChildScreenTimeDecision(
            policy_id=policy.policy_id,
            daily_limit_minutes=policy.daily_limit_minutes,
            screen_time_limited=policy.is_screen_time_limited(),
            emergency_lock_policy_allowed=policy.emergency_lock_allowed_by_guardian_policy,
            runtime_execution_allowed=False,
            reason="screen_time_policy_decision_only",
        )
