from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import (
    RbacEvaluationResult,
    RbacPolicy,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import SecurityRequest


def evaluate_rbac_request(
    request: SecurityRequest,
    policy: RbacPolicy,
) -> RbacEvaluationResult:
    matched_role_ids: list[str] = []
    matched_permission_ids: list[str] = []

    for role in policy.roles:
        if role.role_id not in request.subject.roles:
            continue

        for permission in role.permissions:
            if (
                permission.action is request.action
                and permission.resource_kind is request.resource.resource_kind
            ):
                matched_role_ids.append(role.role_id)
                matched_permission_ids.append(permission.permission_id)

    if matched_permission_ids:
        return RbacEvaluationResult(
            allowed=True,
            matched_role_ids=tuple(sorted(set(matched_role_ids))),
            matched_permission_ids=tuple(sorted(set(matched_permission_ids))),
            reason_codes=("rbac_permission_matched",),
        )

    return RbacEvaluationResult(
        allowed=False,
        matched_role_ids=tuple(sorted(set(matched_role_ids))),
        matched_permission_ids=(),
        reason_codes=("rbac_permission_missing",),
    )
