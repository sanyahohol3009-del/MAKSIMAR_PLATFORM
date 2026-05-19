from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.approval_service_contract import (
    ApprovalStatus,
    apply_approval_to_decision,
    build_approval_record_for_request,
)
from MAKSIMAR_CORE_LIB.security_layer.policy_enforcer_contract import enforce_security_policy
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import SecurityDecisionStatus
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_approval_can_allow_needs_approval_decision() -> None:
    request = build_security_request(
        request_id="sec_req_approval_001",
        trace_id="trace_approval_001",
        subject_id="owner",
        subject_kind=SecuritySubjectKind.OWNER,
        roles=("owner",),
        authenticated=True,
        voice_identity_verified=True,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.HIGH,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="approved high risk",
    )
    decision = enforce_security_policy(request, RbacPolicy(policy_id="empty", roles=()))
    approval = build_approval_record_for_request(
        request,
        approval_id="approval_001",
        status=ApprovalStatus.APPROVED,
        approver_id="owner",
    )

    approved = apply_approval_to_decision(decision, approval)

    assert decision.status is SecurityDecisionStatus.NEEDS_APPROVAL
    assert approved.status is SecurityDecisionStatus.ALLOW
    assert approved.action_execution_allowed is True
