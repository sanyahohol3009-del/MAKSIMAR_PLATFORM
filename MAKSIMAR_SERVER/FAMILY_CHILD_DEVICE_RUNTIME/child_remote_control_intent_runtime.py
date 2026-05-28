from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)


@dataclass(frozen=True)
class ChildRemoteControlIntentDecision:
    intent_id: str
    child_device_id: str
    policy_intent_accepted: bool
    runtime_execution_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "intent_id": self.intent_id,
            "child_device_id": self.child_device_id,
            "policy_intent_accepted": self.policy_intent_accepted,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ChildRemoteControlIntentRuntime:
    def evaluate(self, intent: ChildRemoteControlIntentContract) -> ChildRemoteControlIntentDecision:
        if intent.runtime_execution_allowed:
            raise ValueError("child runtime cannot execute device control in BATCH 4.3")
        if intent.dashboard_bypass_allowed:
            raise ValueError("dashboard bypass is forbidden")

        return ChildRemoteControlIntentDecision(
            intent_id=intent.intent_id,
            child_device_id=intent.child_device_id,
            policy_intent_accepted=intent.is_policy_intent_only(),
            runtime_execution_allowed=False,
            reason="child_control_intent_recorded_without_device_execution",
        )
