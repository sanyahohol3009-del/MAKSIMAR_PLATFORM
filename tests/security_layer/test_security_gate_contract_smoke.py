from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import (
    RbacPermission,
    RbacPolicy,
    RbacRole,
)
from MAKSIMAR_CORE_LIB.security_layer.security_gate_contract import evaluate_security_gate
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_security_gate_denies_unauthenticated_request() -> None:
    request = build_security_request(
        request_id="sec_req_gate_001",
        trace_id="trace_gate_001",
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

    result = evaluate_security_gate(request, RbacPolicy(policy_id="empty", roles=()))

    assert result.action_execution_allowed is False
    assert "security_decision_blocks_execution" in result.reason_codes


def test_security_gate_allows_low_risk_matching_rbac_without_bundle() -> None:
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
        request_id="sec_req_gate_002",
        trace_id="trace_gate_002",
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

    result = evaluate_security_gate(request, policy)

    assert result.action_execution_allowed is True
