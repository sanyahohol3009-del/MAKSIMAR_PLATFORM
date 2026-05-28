from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_control_policy_contract import (
    ChildScreenControlPolicyContract,
)


@dataclass(frozen=True)
class ChildScreenControlDecision:
    policy_id: str
    screen_view_allowed: bool
    screenshot_allowed: bool
    screen_recording_allowed: bool
    interactive_control_requested: bool
    runtime_execution_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "screen_view_allowed": self.screen_view_allowed,
            "screenshot_allowed": self.screenshot_allowed,
            "screen_recording_allowed": self.screen_recording_allowed,
            "interactive_control_requested": self.interactive_control_requested,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ChildScreenControlPolicyRuntime:
    def evaluate(self, policy: ChildScreenControlPolicyContract) -> ChildScreenControlDecision:
        return ChildScreenControlDecision(
            policy_id=policy.policy_id,
            screen_view_allowed=policy.screen_view_allowed_by_guardian_policy,
            screenshot_allowed=policy.screenshot_allowed_by_guardian_policy,
            screen_recording_allowed=policy.screen_recording_allowed_by_guardian_policy,
            interactive_control_requested=policy.allows_interactive_control(),
            runtime_execution_allowed=False,
            reason="policy_decision_only_no_device_execution_in_batch_4_3",
        )
