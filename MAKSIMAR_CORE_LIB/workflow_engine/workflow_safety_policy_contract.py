from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    MobileWorkflowPermissionDecision,
    MobileWorkflowPermissionProfile,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import WorkflowApprovalGateContract


ALLOWED_SAFETY_DECISION_CODES: Tuple[str, ...] = (
    "allowed_for_intent_creation",
    "permission_required",
    "permission_denied",
    "approval_required",
    "approval_denied",
    "critical_risk_blocked",
    "execution_tier_blocked",
    "unsafe_authority_flag",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str, *, require_non_empty: bool) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in workflow safety policy contracts")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow safety policy contracts")


@dataclass(frozen=True)
class WorkflowSafetyDecision:
    allowed_for_intent_creation: bool
    decision_code: str
    reason: str
    permission_decision: Optional[MobileWorkflowPermissionDecision] = None

    def __post_init__(self) -> None:
        if not isinstance(self.allowed_for_intent_creation, bool):
            raise TypeError("allowed_for_intent_creation must be a boolean")
        if self.decision_code not in ALLOWED_SAFETY_DECISION_CODES:
            raise ValueError(f"decision_code must be one of {ALLOWED_SAFETY_DECISION_CODES}")
        object.__setattr__(self, "reason", _require_non_empty_text(self.reason, "reason"))
        if self.permission_decision is not None and not isinstance(
            self.permission_decision,
            MobileWorkflowPermissionDecision,
        ):
            raise TypeError("permission_decision must be a MobileWorkflowPermissionDecision")

    def to_read_model(self) -> dict[str, object]:
        return {
            "allowed_for_intent_creation": self.allowed_for_intent_creation,
            "decision_code": self.decision_code,
            "reason": self.reason,
            "permission_decision": (
                self.permission_decision.to_read_model()
                if self.permission_decision is not None
                else None
            ),
        }


@dataclass(frozen=True)
class WorkflowSafetyPolicyContract:
    policy_id: str = "phase6.workflow.safety.policy.v1"
    allowed_execution_tiers: Tuple[str, ...] = ("mobile_local", "server_local", "hybrid", "cloud_optional")
    require_permission: bool = True
    require_user_approval: bool = True
    require_sandbox_preview: bool = True
    require_audit: bool = True
    block_critical_risk: bool = True
    contract_only: bool = True
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    dashboard_execution_allowed: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", _require_non_empty_text(self.policy_id, "policy_id"))
        object.__setattr__(
            self,
            "allowed_execution_tiers",
            _normalize_text_tuple(
                self.allowed_execution_tiers,
                "allowed_execution_tiers",
                require_non_empty=True,
            ),
        )

        _require_true(self.require_permission, "require_permission")
        _require_true(self.require_user_approval, "require_user_approval")
        _require_true(self.require_sandbox_preview, "require_sandbox_preview")
        _require_true(self.require_audit, "require_audit")
        _require_true(self.block_critical_risk, "block_critical_risk")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def evaluate_proposal(
        self,
        proposal: LocalAIWorkflowProposalContract,
        permission_profile: Optional[MobileWorkflowPermissionProfile],
        approval_ticket: Optional[WorkflowApprovalGateContract],
    ) -> WorkflowSafetyDecision:
        if not isinstance(proposal, LocalAIWorkflowProposalContract):
            raise TypeError("proposal must be a LocalAIWorkflowProposalContract")

        if proposal.graph.local_scope.execution_tier not in self.allowed_execution_tiers:
            return WorkflowSafetyDecision(
                False,
                "execution_tier_blocked",
                "workflow execution tier is not allowed by policy",
            )

        if proposal.risk_level == "critical" and self.block_critical_risk:
            return WorkflowSafetyDecision(
                False,
                "critical_risk_blocked",
                "critical risk workflow proposals are blocked by policy",
            )

        if (
            proposal.proposal_is_execution_authority
            or proposal.execution_authority_allowed
            or proposal.direct_core_write_allowed
            or proposal.direct_server_canonical_write_allowed
            or proposal.network_socket_tunnel_allowed
            or proposal.hidden_remote_control_allowed
            or proposal.runtime_mutation_allowed
            or proposal.platform_api_call_allowed
        ):
            return WorkflowSafetyDecision(
                False,
                "unsafe_authority_flag",
                "proposal contains unsafe authority flags",
            )

        if permission_profile is None:
            return WorkflowSafetyDecision(
                False,
                "permission_required",
                "mobile workflow permission profile is required",
            )

        permission_decision = permission_profile.evaluate_proposal(proposal)
        if permission_decision.allowed is not True:
            return WorkflowSafetyDecision(
                False,
                "permission_denied",
                "mobile workflow permission profile denied the proposal",
                permission_decision=permission_decision,
            )

        if approval_ticket is None:
            return WorkflowSafetyDecision(
                False,
                "approval_required",
                "workflow approval ticket is required",
                permission_decision=permission_decision,
            )

        if approval_ticket.allows_intent_creation(proposal.proposal_id) is not True:
            return WorkflowSafetyDecision(
                False,
                "approval_denied",
                "workflow approval ticket does not allow intent creation",
                permission_decision=permission_decision,
            )

        return WorkflowSafetyDecision(
            True,
            "allowed_for_intent_creation",
            "proposal is allowed to create a policy-gated workflow intent",
            permission_decision=permission_decision,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "allowed_execution_tiers": self.allowed_execution_tiers,
            "require_permission": self.require_permission,
            "require_user_approval": self.require_user_approval,
            "require_sandbox_preview": self.require_sandbox_preview,
            "require_audit": self.require_audit,
            "block_critical_risk": self.block_critical_risk,
            "contract_only": self.contract_only,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_workflow_safety_policy_contract() -> WorkflowSafetyPolicyContract:
    return WorkflowSafetyPolicyContract()


__all__ = [
    "ALLOWED_SAFETY_DECISION_CODES",
    "WorkflowSafetyDecision",
    "WorkflowSafetyPolicyContract",
    "build_workflow_safety_policy_contract",
]
