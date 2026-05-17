from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.rbac_contract import evaluate_rbac_request
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import (
    RbacPermission,
    RbacPolicy,
    RbacRole,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_rbac_allows_matching_role_permission() -> None:
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
        request_id="sec_req_rbac_001",
        trace_id="trace_rbac_001",
        subject_id="operator_1",
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

    result = evaluate_rbac_request(request, policy)

    assert result.allowed is True
    assert result.matched_permission_ids == ("perm_read_memory",)


def test_rbac_denies_missing_permission() -> None:
    policy = RbacPolicy(policy_id="policy_empty", roles=())

    request = build_security_request(
        request_id="sec_req_rbac_deny_001",
        trace_id="trace_rbac_deny_001",
        subject_id="operator_1",
        subject_kind=SecuritySubjectKind.OPERATOR,
        roles=("operator",),
        authenticated=True,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.LOW,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="execute core",
    )

    result = evaluate_rbac_request(request, policy)

    assert result.allowed is False
    assert result.reason_codes == ("rbac_permission_missing",)
