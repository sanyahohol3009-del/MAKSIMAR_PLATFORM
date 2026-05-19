from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import SecurityDecisionStatus
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)
from MAKSIMAR_CORE_LIB.security_layer.security_tracer_read_model import (
    SecurityTracerGateSnapshot,
    SecurityTracerScenarioStatus,
    build_security_tracer_result_read_model,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.security_gate import evaluate_runtime_security_gate
from MAKSIMAR_SERVER.SECURITY_LAYER.security_telemetry_read_model_builder import (
    build_security_telemetry_read_model,
)


def test_security_gate_denies_unauthorized_mock() -> None:
    request = build_security_request(
        request_id="e2e_security_unauthorized_001",
        trace_id="trace_e2e_security_unauthorized_001",
        subject_id="unauthorized_subject",
        subject_kind=SecuritySubjectKind.UNKNOWN,
        roles=(),
        authenticated=False,
        voice_identity_verified=False,
        resource_id="core_root_high_risk_execution",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.HIGH,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="E2E unauthorized high-risk request without verified voice identity.",
        metadata={
            "scenario": "control_core_to_security_deny",
            "requires_security_gate": True,
        },
    )

    empty_policy = RbacPolicy(policy_id="e2e_empty_security_policy", roles=())

    runtime_evaluation = evaluate_runtime_security_gate(
        request,
        empty_policy,
    )

    telemetry = build_security_telemetry_read_model(
        runtime_evaluation=runtime_evaluation,
        project_root=Path("."),
    )

    tracer = build_security_tracer_result_read_model(
        tracer_id="security_e2e_tracer_001",
        scenario_id="control_core_to_security_high_risk_deny",
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        gate_snapshot=SecurityTracerGateSnapshot(
            request_id=runtime_evaluation.request_id,
            trace_id=runtime_evaluation.trace_id,
            decision_status=runtime_evaluation.gate_result.decision.status.value,
            risk_level=runtime_evaluation.gate_result.decision.risk_level.value,
            decision_allows_execution=runtime_evaluation.decision_allows_execution,
            actual_execution_performed=runtime_evaluation.actual_execution_performed,
            reason_codes=runtime_evaluation.reason_codes,
        ),
        telemetry=telemetry,
        expected_blocked=True,
    )

    assert runtime_evaluation.gate_result.decision.status is SecurityDecisionStatus.DENY
    assert runtime_evaluation.decision_allows_execution is False
    assert runtime_evaluation.actual_execution_performed is False
    assert telemetry.gate.actual_execution_performed is False
    assert telemetry.gate.decision_allows_execution is False
    assert tracer.scenario_status is SecurityTracerScenarioStatus.PASSED
    assert tracer.operation_blocked is True
    assert tracer.action_execution_allowed is False
    assert tracer.dashboard_safe is True
    assert tracer.runtime_mutation_allowed is False
    assert tracer.canonical_write_allowed is False
    assert tracer.direct_execution_allowed is False
    assert tracer.ui_to_execution_allowed is False
    assert "subject_not_authenticated" in tracer.reason_codes
