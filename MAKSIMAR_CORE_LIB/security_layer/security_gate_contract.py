from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.security_layer.execution_bundle_verifier_contract import (
    ExecutionBundle,
    ExecutionBundleVerificationResult,
    verify_execution_bundle,
)
from MAKSIMAR_CORE_LIB.security_layer.policy_enforcer_contract import enforce_security_policy
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import SecurityDecision
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import SecurityRequest


@dataclass(frozen=True, slots=True)
class SecurityGateResult:
    request_id: str
    trace_id: str
    decision: SecurityDecision
    bundle_verification: ExecutionBundleVerificationResult | None
    action_execution_allowed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.trace_id:
            raise ValueError("trace_id must not be empty")
        if not isinstance(self.decision, SecurityDecision):
            raise TypeError("decision must be SecurityDecision")
        if self.action_execution_allowed and not self.decision.action_execution_allowed:
            raise ValueError("gate cannot allow execution when decision blocks execution")
        if self.action_execution_allowed and self.bundle_verification is not None:
            if not self.bundle_verification.ready_for_execution:
                raise ValueError("gate cannot allow execution when bundle verification blocks execution")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def evaluate_security_gate(
    request: SecurityRequest,
    policy: RbacPolicy,
    *,
    bundle: ExecutionBundle | None = None,
) -> SecurityGateResult:
    decision = enforce_security_policy(request, policy)

    if not decision.action_execution_allowed:
        return SecurityGateResult(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            decision=decision,
            bundle_verification=None,
            action_execution_allowed=False,
            reason_codes=("security_decision_blocks_execution",) + decision.reason_codes,
        )

    if bundle is None:
        return SecurityGateResult(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            decision=decision,
            bundle_verification=None,
            action_execution_allowed=True,
            reason_codes=("security_gate_allowed_without_bundle",),
        )

    bundle_result = verify_execution_bundle(bundle)
    if not bundle_result.ready_for_execution:
        return SecurityGateResult(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            decision=decision,
            bundle_verification=bundle_result,
            action_execution_allowed=False,
            reason_codes=("execution_bundle_blocks_execution",) + bundle_result.reason_codes,
        )

    return SecurityGateResult(
        request_id=request.context.request_id,
        trace_id=request.context.trace_id,
        decision=decision,
        bundle_verification=bundle_result,
        action_execution_allowed=True,
        reason_codes=("security_gate_allowed",),
    )
