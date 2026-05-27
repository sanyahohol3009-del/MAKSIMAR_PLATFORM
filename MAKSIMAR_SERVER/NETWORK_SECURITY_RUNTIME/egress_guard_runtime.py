from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from MAKSIMAR_CORE_LIB.network_security.egress_policy_contract import (
    EgressPolicyContract,
    build_default_egress_policy_contract,
)


EgressRuntimeDecision = Literal["deny_external_egress", "deny_dns", "deny_public_ingress"]


@dataclass(frozen=True, slots=True)
class EgressGuardRuntimeDecision:
    """Server egress guard runtime decision.

    This is an enforceable decision object, not a network executor.
    """

    decision_id: str
    decision: EgressRuntimeDecision
    policy: EgressPolicyContract
    requested_destination: str
    allowed: bool
    dns_resolution_performed: bool
    external_connection_attempted: bool
    public_ingress_enabled: bool
    tunnel_creation_attempted: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    audit_required: bool
    dashboard_visible: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.decision_id != "phase_2_egress_guard_runtime_decision":
            raise ValueError("decision_id must be phase_2_egress_guard_runtime_decision")
        if not isinstance(self.policy, EgressPolicyContract):
            raise TypeError("policy must be EgressPolicyContract")
        if not isinstance(self.requested_destination, str) or not self.requested_destination:
            raise ValueError("requested_destination must be non-empty")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "audit_required": self.audit_required,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "allowed": self.allowed,
            "dns_resolution_performed": self.dns_resolution_performed,
            "external_connection_attempted": self.external_connection_attempted,
            "public_ingress_enabled": self.public_ingress_enabled,
            "tunnel_creation_attempted": self.tunnel_creation_attempted,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision": self.decision,
            "policy": self.policy.to_dict(),
            "requested_destination": self.requested_destination,
            "allowed": self.allowed,
            "dns_resolution_performed": self.dns_resolution_performed,
            "external_connection_attempted": self.external_connection_attempted,
            "public_ingress_enabled": self.public_ingress_enabled,
            "tunnel_creation_attempted": self.tunnel_creation_attempted,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "audit_required": self.audit_required,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def evaluate_egress_guard_runtime(
    requested_destination: str = "example.invalid",
    policy: EgressPolicyContract | None = None,
) -> EgressGuardRuntimeDecision:
    runtime_policy = policy or build_default_egress_policy_contract()

    return EgressGuardRuntimeDecision(
        decision_id="phase_2_egress_guard_runtime_decision",
        decision="deny_external_egress",
        policy=runtime_policy,
        requested_destination=requested_destination,
        allowed=False,
        dns_resolution_performed=False,
        external_connection_attempted=False,
        public_ingress_enabled=False,
        tunnel_creation_attempted=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        audit_required=True,
        dashboard_visible=True,
        containerization_ready=True,
        reason_codes=("external_egress_denied_by_default",),
    )
