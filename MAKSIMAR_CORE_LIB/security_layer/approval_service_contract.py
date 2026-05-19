from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import (
    SecurityDecision,
    SecurityDecisionStatus,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import SecurityRequest


class ApprovalStatus(str, Enum):
    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    APPROVED = "approved"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class ApprovalRecord:
    approval_id: str
    request_id: str
    trace_id: str
    status: ApprovalStatus
    approver_id: str
    reason: str
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("approval_id", self.approval_id),
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("reason", self.reason),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.status, ApprovalStatus):
            raise TypeError("status must be ApprovalStatus")
        if self.status in (ApprovalStatus.APPROVED, ApprovalStatus.DENIED) and not self.approver_id:
            raise ValueError("approved/denied records require approver_id")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def build_approval_record_for_request(
    request: SecurityRequest,
    *,
    approval_id: str,
    status: ApprovalStatus,
    approver_id: str = "",
    reason: str = "approval evaluated",
) -> ApprovalRecord:
    return ApprovalRecord(
        approval_id=approval_id,
        request_id=request.context.request_id,
        trace_id=request.context.trace_id,
        status=status,
        approver_id=approver_id,
        reason=reason,
    )


def apply_approval_to_decision(
    decision: SecurityDecision,
    approval: ApprovalRecord,
) -> SecurityDecision:
    if decision.request_id != approval.request_id:
        raise ValueError("approval request_id must match decision request_id")
    if decision.trace_id != approval.trace_id:
        raise ValueError("approval trace_id must match decision trace_id")

    if decision.status is not SecurityDecisionStatus.NEEDS_APPROVAL:
        return decision

    if approval.status is ApprovalStatus.APPROVED:
        return SecurityDecision(
            request_id=decision.request_id,
            trace_id=decision.trace_id,
            status=SecurityDecisionStatus.ALLOW,
            risk_level=decision.risk_level,
            reason_codes=("approval_granted",),
            human_summary="Security request allowed after explicit approval.",
            approval_required=False,
            voice_identity_required=False,
            signature_required=False,
            action_execution_allowed=True,
        )

    if approval.status is ApprovalStatus.DENIED:
        return SecurityDecision(
            request_id=decision.request_id,
            trace_id=decision.trace_id,
            status=SecurityDecisionStatus.DENY,
            risk_level=decision.risk_level,
            reason_codes=("approval_denied",),
            human_summary="Security request denied by explicit approval decision.",
            approval_required=False,
            voice_identity_required=False,
            signature_required=False,
            action_execution_allowed=False,
        )

    return decision
