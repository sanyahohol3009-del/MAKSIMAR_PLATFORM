from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import SecurityDecision
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityRequest,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.security_gate import (
    SecurityRuntimeGateEvaluation,
    evaluate_runtime_security_gate,
)


@dataclass(frozen=True, slots=True)
class SecurityDecisionBuildInput:
    request_id: str
    trace_id: str
    subject_id: str
    subject_kind: SecuritySubjectKind
    roles: tuple[str, ...]
    authenticated: bool
    voice_identity_verified: bool
    service_identity_verified: bool
    resource_id: str
    resource_kind: SecurityResourceKind
    action: SecurityActionKind
    risk_level: SecurityRiskLevel
    source_layer_id: str
    target_layer_id: str
    reason: str
    metadata: dict[str, Any]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("subject_id", self.subject_id),
            ("resource_id", self.resource_id),
            ("source_layer_id", self.source_layer_id),
            ("target_layer_id", self.target_layer_id),
            ("reason", self.reason),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.subject_kind, SecuritySubjectKind):
            raise TypeError("subject_kind must be SecuritySubjectKind")
        if not isinstance(self.roles, tuple):
            raise TypeError("roles must be a tuple")
        if not isinstance(self.resource_kind, SecurityResourceKind):
            raise TypeError("resource_kind must be SecurityResourceKind")
        if not isinstance(self.action, SecurityActionKind):
            raise TypeError("action must be SecurityActionKind")
        if not isinstance(self.risk_level, SecurityRiskLevel):
            raise TypeError("risk_level must be SecurityRiskLevel")
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")


def build_security_request_from_decision_input(
    decision_input: SecurityDecisionBuildInput,
) -> SecurityRequest:
    return build_security_request(
        request_id=decision_input.request_id,
        trace_id=decision_input.trace_id,
        subject_id=decision_input.subject_id,
        subject_kind=decision_input.subject_kind,
        roles=decision_input.roles,
        authenticated=decision_input.authenticated,
        voice_identity_verified=decision_input.voice_identity_verified,
        service_identity_verified=decision_input.service_identity_verified,
        resource_id=decision_input.resource_id,
        resource_kind=decision_input.resource_kind,
        action=decision_input.action,
        risk_level=decision_input.risk_level,
        source_layer_id=decision_input.source_layer_id,
        target_layer_id=decision_input.target_layer_id,
        reason=decision_input.reason,
        metadata=decision_input.metadata,
    )


def build_security_runtime_decision(
    decision_input: SecurityDecisionBuildInput,
    policy: RbacPolicy,
) -> SecurityRuntimeGateEvaluation:
    request = build_security_request_from_decision_input(decision_input)
    return evaluate_runtime_security_gate(request, policy)


def extract_security_decision(
    runtime_evaluation: SecurityRuntimeGateEvaluation,
) -> SecurityDecision:
    return runtime_evaluation.gate_result.decision
