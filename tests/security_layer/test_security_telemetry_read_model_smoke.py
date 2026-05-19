from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPermission, RbacPolicy, RbacRole
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.security_gate import evaluate_runtime_security_gate
from MAKSIMAR_SERVER.SECURITY_LAYER.security_telemetry_read_model_builder import (
    build_security_telemetry_read_model,
)


def test_security_telemetry_read_model_is_dashboard_safe() -> None:
    policy = RbacPolicy(
        policy_id="telemetry_policy",
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
        request_id="telemetry_req_001",
        trace_id="telemetry_trace_001",
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
        reason="telemetry read",
    )

    evaluation = evaluate_runtime_security_gate(request, policy)
    telemetry = build_security_telemetry_read_model(
        runtime_evaluation=evaluation,
        project_root=Path("."),
    )

    assert telemetry.dashboard_safe is True
    assert telemetry.runtime_mutation_allowed is False
    assert telemetry.canonical_write_allowed is False
    assert telemetry.direct_execution_allowed is False
    assert telemetry.gate.actual_execution_performed is False
    assert telemetry.to_dict()["layer_id"] == "SECURITY_LAYER"
