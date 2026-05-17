from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.rbac_contract import evaluate_rbac_request
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import (
    SecurityDecision,
    SecurityDecisionStatus,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityRequest,
    SecurityRiskLevel,
)


def enforce_security_policy(
    request: SecurityRequest,
    policy: RbacPolicy,
) -> SecurityDecision:
    if not request.subject.authenticated:
        return SecurityDecision(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            status=SecurityDecisionStatus.DENY,
            risk_level=request.risk_level,
            reason_codes=("subject_not_authenticated",),
            human_summary="Security request denied because subject is not authenticated.",
            approval_required=request.requires_approval,
            voice_identity_required=request.requires_voice_identity,
            signature_required=request.requires_signature,
            action_execution_allowed=False,
        )

    if request.risk_level in (SecurityRiskLevel.HIGH, SecurityRiskLevel.CRITICAL):
        if request.requires_voice_identity and not request.subject.voice_identity_verified:
            return SecurityDecision(
                request_id=request.context.request_id,
                trace_id=request.context.trace_id,
                status=SecurityDecisionStatus.NEEDS_VOICE_IDENTITY,
                risk_level=request.risk_level,
                reason_codes=("voice_identity_required",),
                human_summary="Security request requires verified owner voice identity.",
                approval_required=request.requires_approval,
                voice_identity_required=True,
                signature_required=request.requires_signature,
                action_execution_allowed=False,
            )

    if request.requires_signature:
        return SecurityDecision(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            status=SecurityDecisionStatus.NEEDS_SIGNATURE,
            risk_level=request.risk_level,
            reason_codes=("signature_required",),
            human_summary="Security request requires a valid signature before execution.",
            approval_required=request.requires_approval,
            voice_identity_required=False,
            signature_required=True,
            action_execution_allowed=False,
        )

    if request.requires_approval:
        return SecurityDecision(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            status=SecurityDecisionStatus.NEEDS_APPROVAL,
            risk_level=request.risk_level,
            reason_codes=("approval_required",),
            human_summary="Security request requires human approval before execution.",
            approval_required=True,
            voice_identity_required=False,
            signature_required=False,
            action_execution_allowed=False,
        )

    rbac_result = evaluate_rbac_request(request, policy)
    if not rbac_result.allowed:
        return SecurityDecision(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            status=SecurityDecisionStatus.DENY,
            risk_level=request.risk_level,
            reason_codes=rbac_result.reason_codes,
            human_summary="Security request denied by RBAC policy.",
            approval_required=False,
            voice_identity_required=False,
            signature_required=False,
            action_execution_allowed=False,
        )

    return SecurityDecision(
        request_id=request.context.request_id,
        trace_id=request.context.trace_id,
        status=SecurityDecisionStatus.ALLOW,
        risk_level=request.risk_level,
        reason_codes=("security_policy_allowed",),
        human_summary="Security request allowed by policy and RBAC.",
        approval_required=False,
        voice_identity_required=False,
        signature_required=False,
        action_execution_allowed=True,
    )
