from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.security_read_model import (
    SecurityReadModelStatus,
    SecurityTelemetryReadModel,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.security_gate import SecurityRuntimeGateEvaluation
from MAKSIMAR_SERVER.SECURITY_LAYER.security_layer_health import (
    build_security_layer_health_read_model,
)


def build_security_telemetry_read_model(
    *,
    runtime_evaluation: SecurityRuntimeGateEvaluation,
    project_root: Path,
) -> SecurityTelemetryReadModel:
    adapter_readiness = []

    if runtime_evaluation.existing_policy_adapter is not None:
        adapter_readiness.append(runtime_evaluation.existing_policy_adapter.to_read_model())

    if runtime_evaluation.vendor_gate_decision is not None:
        adapter_readiness.append(runtime_evaluation.vendor_gate_decision.to_read_model())

    health = build_security_layer_health_read_model(
        project_root=project_root,
        adapter_readiness=tuple(adapter_readiness),
    )

    if not runtime_evaluation.decision_allows_execution:
        status = SecurityReadModelStatus.BLOCKED
        reason_codes = ("security_runtime_decision_blocked",) + runtime_evaluation.reason_codes
    elif health.status is not SecurityReadModelStatus.HEALTHY:
        status = SecurityReadModelStatus.DEGRADED
        reason_codes = ("security_runtime_allowed_but_health_degraded",)
    else:
        status = SecurityReadModelStatus.HEALTHY
        reason_codes = ("security_runtime_allowed_and_healthy",)

    return SecurityTelemetryReadModel(
        layer_id="SECURITY_LAYER",
        batch_id="PHASE_1_BATCH_1_4",
        status=status,
        gate=runtime_evaluation.to_gate_read_model(),
        health=health,
        generated_by="security_telemetry_read_model_builder",
        reason_codes=reason_codes,
    )
