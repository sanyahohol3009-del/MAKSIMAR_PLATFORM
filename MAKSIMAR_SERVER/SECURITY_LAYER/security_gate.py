from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.security_layer.execution_bundle_verifier_contract import ExecutionBundle
from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPolicy
from MAKSIMAR_CORE_LIB.security_layer.security_gate_contract import (
    SecurityGateResult,
    evaluate_security_gate,
)
from MAKSIMAR_CORE_LIB.security_layer.security_read_model import SecurityGateRuntimeReadModel
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import SecurityRequest
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_existing_policy_adapter import (
    ExistingPolicyAdapterSnapshot,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_vendor_gate_adapter import (
    VendorGateAdapterDecision,
)


@dataclass(frozen=True, slots=True)
class SecurityRuntimeGateEvaluation:
    request_id: str
    trace_id: str
    gate_result: SecurityGateResult
    existing_policy_adapter: ExistingPolicyAdapterSnapshot | None
    vendor_gate_decision: VendorGateAdapterDecision | None
    decision_allows_execution: bool
    actual_execution_performed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.trace_id:
            raise ValueError("trace_id must not be empty")
        if not isinstance(self.gate_result, SecurityGateResult):
            raise TypeError("gate_result must be SecurityGateResult")
        if self.existing_policy_adapter is not None and not isinstance(
            self.existing_policy_adapter,
            ExistingPolicyAdapterSnapshot,
        ):
            raise TypeError("existing_policy_adapter must be ExistingPolicyAdapterSnapshot or None")
        if self.vendor_gate_decision is not None and not isinstance(
            self.vendor_gate_decision,
            VendorGateAdapterDecision,
        ):
            raise TypeError("vendor_gate_decision must be VendorGateAdapterDecision or None")
        if self.decision_allows_execution != self.gate_result.action_execution_allowed:
            raise ValueError("decision_allows_execution must mirror gate_result.action_execution_allowed")
        if self.actual_execution_performed:
            raise ValueError("runtime security gate facade must not perform execution")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_dashboard_execution_allowed:
            raise ValueError("direct_dashboard_execution_allowed must remain false")

    def to_gate_read_model(self) -> SecurityGateRuntimeReadModel:
        return SecurityGateRuntimeReadModel(
            request_id=self.request_id,
            trace_id=self.trace_id,
            decision_status=self.gate_result.decision.status.value,
            risk_level=self.gate_result.decision.risk_level.value,
            decision_allows_execution=self.decision_allows_execution,
            actual_execution_performed=self.actual_execution_performed,
            reason_codes=self.reason_codes,
        )


def evaluate_runtime_security_gate(
    request: SecurityRequest,
    policy: RbacPolicy,
    *,
    bundle: ExecutionBundle | None = None,
    existing_policy_adapter: ExistingPolicyAdapterSnapshot | None = None,
    vendor_gate_decision: VendorGateAdapterDecision | None = None,
) -> SecurityRuntimeGateEvaluation:
    if vendor_gate_decision is not None and not vendor_gate_decision.allowed_for_read_only_reference:
        raise ValueError("vendor gate adapter must allow at least read-only reference")

    gate_result = evaluate_security_gate(request, policy, bundle=bundle)
    reason_codes = list(gate_result.reason_codes)

    if vendor_gate_decision is not None and not vendor_gate_decision.allowed_for_runtime:
        reason_codes = ["vendor_gate_blocks_runtime"] + list(vendor_gate_decision.reason_codes)

        return SecurityRuntimeGateEvaluation(
            request_id=request.context.request_id,
            trace_id=request.context.trace_id,
            gate_result=SecurityGateResult(
                request_id=gate_result.request_id,
                trace_id=gate_result.trace_id,
                decision=gate_result.decision,
                bundle_verification=gate_result.bundle_verification,
                action_execution_allowed=False,
                reason_codes=tuple(reason_codes),
            ),
            existing_policy_adapter=existing_policy_adapter,
            vendor_gate_decision=vendor_gate_decision,
            decision_allows_execution=False,
            actual_execution_performed=False,
            reason_codes=tuple(reason_codes),
        )

    return SecurityRuntimeGateEvaluation(
        request_id=request.context.request_id,
        trace_id=request.context.trace_id,
        gate_result=gate_result,
        existing_policy_adapter=existing_policy_adapter,
        vendor_gate_decision=vendor_gate_decision,
        decision_allows_execution=gate_result.action_execution_allowed,
        actual_execution_performed=False,
        reason_codes=tuple(reason_codes),
    )
