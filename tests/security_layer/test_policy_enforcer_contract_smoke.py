from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.policy_enforcer_contract import (
    enforce_security_policy,
)
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import (
    RbacPermission,
    RbacPolicy,
    RbacRole,
)
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import (
    SecurityDecisionStatus,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_policy_enforcer_blocks_unauthenticated_subject() -> None:
    policy = RbacPolicy(policy_id="policy_empty", roles=())

    request = build_security_request(
        request_id="sec_req_policy_001",
        trace_id="trace_policy_001",
        subject_id="unknown",
        subject_kind=SecuritySubjectKind.UNKNOWN,
        roles=(),
        authenticated=False,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.LOW,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="unauthenticated",
    )

    decision = enforce_security_policy(request, policy)

    assert decision.status is SecurityDecisionStatus.DENY
    assert decision.action_execution_allowed is False


def test_policy_enforcer_requires_voice_for_high_risk() -> None:
    policy = RbacPolicy(policy_id="policy_empty", roles=())

    request = build_security_request(
        request_id="sec_req_policy_voice_001",
        trace_id="trace_policy_voice_001",
        subject_id="owner",
        subject_kind=SecuritySubjectKind.OWNER,
        roles=("owner",),
        authenticated=True,
        voice_identity_verified=False,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.HIGH,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="high risk",
    )

    decision = enforce_security_policy(request, policy)

    assert decision.status is SecurityDecisionStatus.NEEDS_VOICE_IDENTITY
    assert decision.action_execution_allowed is False


def test_policy_enforcer_allows_low_risk_matching_rbac() -> None:
    policy = RbacPolicy(
        policy_id="policy_001",
        roles=(
            RbacRole(
                role_id="operator",
                permissions=(
                    RbacPermission(
                        permission_id="perm_read_memory",
                        action=SecurityActionKind.READ,
                        resource_kind=SecurityResourceKind.MEMORY,
                    ),
                ),
            ),
        ),
    )

    request = build_security_request(
        request_id="sec_req_policy_allow_001",
        trace_id="trace_policy_allow_001",
        subject_id="operator",
        subject_kind=SecuritySubjectKind.OPERATOR,
        roles=("operator",),
        authenticated=True,
        resource_id="memory",
        resource_kind=SecurityResourceKind.MEMORY,
        action=SecurityActionKind.READ,
        risk_level=SecurityRiskLevel.LOW,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="MEMORY",
        reason="read memory",
    )

    decision = enforce_security_policy(request, policy)

    assert decision.status is SecurityDecisionStatus.ALLOW
    assert decision.action_execution_allowed is True
