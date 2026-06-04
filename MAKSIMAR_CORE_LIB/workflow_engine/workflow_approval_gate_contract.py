from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ALLOWED_APPROVAL_DECISIONS: Tuple[str, ...] = ("pending", "approved", "rejected")
ALLOWED_APPROVAL_SCOPES: Tuple[str, ...] = ("preview_only", "single_run_intent", "deny")
ALLOWED_APPROVAL_RISK_LEVELS: Tuple[str, ...] = ("low", "medium", "high", "critical")


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in workflow approval gate contracts")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow approval gate contracts")


@dataclass(frozen=True)
class WorkflowApprovalGateContract:
    approval_ticket_id: str
    proposal_id: str
    approver_id: str
    decision: str
    approval_scope: str
    risk_level: str
    explicit_user_approval_present: bool
    sandbox_preview_reviewed: bool
    audit_required: bool = True
    contract_only: bool = True
    execution_authority_allowed: bool = False
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "approval_ticket_id",
            _require_non_empty_text(self.approval_ticket_id, "approval_ticket_id"),
        )
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "approver_id", _require_non_empty_text(self.approver_id, "approver_id"))
        object.__setattr__(
            self,
            "decision",
            _require_allowed(self.decision, "decision", ALLOWED_APPROVAL_DECISIONS),
        )
        object.__setattr__(
            self,
            "approval_scope",
            _require_allowed(self.approval_scope, "approval_scope", ALLOWED_APPROVAL_SCOPES),
        )
        object.__setattr__(
            self,
            "risk_level",
            _require_allowed(self.risk_level, "risk_level", ALLOWED_APPROVAL_RISK_LEVELS),
        )

        _require_true(self.audit_required, "audit_required")
        _require_true(self.contract_only, "contract_only")
        _require_false(self.execution_authority_allowed, "execution_authority_allowed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

        if self.decision == "approved":
            if self.explicit_user_approval_present is not True:
                raise ValueError("approved workflow ticket requires explicit_user_approval_present=True")
            if self.sandbox_preview_reviewed is not True:
                raise ValueError("approved workflow ticket requires sandbox_preview_reviewed=True")
            if self.approval_scope != "single_run_intent":
                raise ValueError("approved workflow ticket must use approval_scope=single_run_intent")

        if self.decision == "rejected" and self.approval_scope != "deny":
            raise ValueError("rejected workflow ticket must use approval_scope=deny")

    def allows_intent_creation(self, proposal_id: str) -> bool:
        normalized_proposal_id = _require_non_empty_text(proposal_id, "proposal_id")
        return (
            self.proposal_id == normalized_proposal_id
            and self.decision == "approved"
            and self.approval_scope == "single_run_intent"
            and self.explicit_user_approval_present is True
            and self.sandbox_preview_reviewed is True
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "approval_ticket_id": self.approval_ticket_id,
            "proposal_id": self.proposal_id,
            "approver_id": self.approver_id,
            "decision": self.decision,
            "approval_scope": self.approval_scope,
            "risk_level": self.risk_level,
            "explicit_user_approval_present": self.explicit_user_approval_present,
            "sandbox_preview_reviewed": self.sandbox_preview_reviewed,
            "audit_required": self.audit_required,
            "contract_only": self.contract_only,
            "execution_authority_allowed": self.execution_authority_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_pending_workflow_approval_ticket(
    *,
    approval_ticket_id: str,
    proposal_id: str,
    approver_id: str,
    risk_level: str,
) -> WorkflowApprovalGateContract:
    return WorkflowApprovalGateContract(
        approval_ticket_id=approval_ticket_id,
        proposal_id=proposal_id,
        approver_id=approver_id,
        decision="pending",
        approval_scope="preview_only",
        risk_level=risk_level,
        explicit_user_approval_present=False,
        sandbox_preview_reviewed=False,
    )


def build_approved_workflow_approval_ticket(
    *,
    approval_ticket_id: str,
    proposal_id: str,
    approver_id: str,
    risk_level: str,
) -> WorkflowApprovalGateContract:
    return WorkflowApprovalGateContract(
        approval_ticket_id=approval_ticket_id,
        proposal_id=proposal_id,
        approver_id=approver_id,
        decision="approved",
        approval_scope="single_run_intent",
        risk_level=risk_level,
        explicit_user_approval_present=True,
        sandbox_preview_reviewed=True,
    )


__all__ = [
    "ALLOWED_APPROVAL_DECISIONS",
    "ALLOWED_APPROVAL_RISK_LEVELS",
    "ALLOWED_APPROVAL_SCOPES",
    "WorkflowApprovalGateContract",
    "build_approved_workflow_approval_ticket",
    "build_pending_workflow_approval_ticket",
]
