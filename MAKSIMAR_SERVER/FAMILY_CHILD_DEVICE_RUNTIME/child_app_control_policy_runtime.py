from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_app_control_policy_contract import (
    ChildAppControlPolicyContract,
)


@dataclass(frozen=True)
class ChildAppControlDecision:
    policy_id: str
    app_blocking_allowed: bool
    install_approval_required: bool
    runtime_execution_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "app_blocking_allowed": self.app_blocking_allowed,
            "install_approval_required": self.install_approval_required,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ChildAppControlPolicyRuntime:
    def evaluate(self, policy: ChildAppControlPolicyContract) -> ChildAppControlDecision:
        if policy.runtime_execution_allowed:
            raise ValueError("app control runtime execution is forbidden in BATCH 4.3")
        return ChildAppControlDecision(
            policy_id=policy.policy_id,
            app_blocking_allowed=policy.app_blocking_allowed_by_guardian_policy,
            install_approval_required=policy.requires_install_approval(),
            runtime_execution_allowed=False,
            reason="app_control_policy_decision_only",
        )
