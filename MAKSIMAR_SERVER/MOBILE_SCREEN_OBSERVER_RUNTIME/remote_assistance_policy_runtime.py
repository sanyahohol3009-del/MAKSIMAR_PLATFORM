from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)


@dataclass(frozen=True)
class RemoteAssistanceDecision:
    intent_id: str
    allowed_to_execute: bool
    approval_required: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "intent_id": self.intent_id,
            "allowed_to_execute": self.allowed_to_execute,
            "approval_required": self.approval_required,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class RemoteAssistancePolicyRuntime:
    def evaluate(self, intent: RemoteAssistanceIntentContract) -> RemoteAssistanceDecision:
        if intent.device_control_execution_allowed:
            raise ValueError("normal observer runtime cannot execute device control")
        if intent.dashboard_direct_execute_allowed:
            raise ValueError("dashboard direct execution is forbidden")
        if intent.runtime_mutation_allowed:
            raise ValueError("runtime mutation is forbidden")
        if intent.core_write_allowed:
            raise ValueError("core write is forbidden")

        return RemoteAssistanceDecision(
            intent_id=intent.intent_id,
            allowed_to_execute=False,
            approval_required=intent.requires_manual_approval(),
            reason="normal_observer_remote_assistance_is_approval_gated_and_non_executing",
        )
