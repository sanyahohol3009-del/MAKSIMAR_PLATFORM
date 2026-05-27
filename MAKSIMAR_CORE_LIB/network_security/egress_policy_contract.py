from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


EgressDecision = Literal["deny_by_default", "allow_read_only_metadata"]


@dataclass(frozen=True, slots=True)
class EgressPolicyContract:
    """Network egress policy contract.

    Default behavior is deny. No external network access is enabled here.
    """

    policy_id: str
    decision: EgressDecision
    deny_by_default: bool
    allow_external_network: bool
    allow_dns_resolution: bool
    allow_public_ingress: bool
    allow_tunnel_creation: bool
    require_operator_approval: bool
    dashboard_visible: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.policy_id != "phase_2_egress_policy_contract":
            raise ValueError("policy_id must be phase_2_egress_policy_contract")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "deny_by_default": self.deny_by_default,
            "require_operator_approval": self.require_operator_approval,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "allow_external_network": self.allow_external_network,
            "allow_dns_resolution": self.allow_dns_resolution,
            "allow_public_ingress": self.allow_public_ingress,
            "allow_tunnel_creation": self.allow_tunnel_creation,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "decision": self.decision,
            "deny_by_default": self.deny_by_default,
            "allow_external_network": self.allow_external_network,
            "allow_dns_resolution": self.allow_dns_resolution,
            "allow_public_ingress": self.allow_public_ingress,
            "allow_tunnel_creation": self.allow_tunnel_creation,
            "require_operator_approval": self.require_operator_approval,
            "dashboard_visible": self.dashboard_visible,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_default_egress_policy_contract() -> EgressPolicyContract:
    return EgressPolicyContract(
        policy_id="phase_2_egress_policy_contract",
        decision="deny_by_default",
        deny_by_default=True,
        allow_external_network=False,
        allow_dns_resolution=False,
        allow_public_ingress=False,
        allow_tunnel_creation=False,
        require_operator_approval=True,
        dashboard_visible=True,
        runtime_mutation_allowed=False,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        containerization_ready=True,
        reason_codes=("egress_denied_by_default_until_policy_gate",),
    )
