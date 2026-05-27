from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnPolicyDisableContract,
    build_default_vpn_policy_disable_contract,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_session_registry import (
    VpnSessionRegistry,
    build_default_vpn_session_registry,
)


VpnRuntimeDecision = Literal["deny_runtime_start", "deny_tunnel_create", "allow_read_model_only"]


@dataclass(frozen=True, slots=True)
class VpnPolicyRuntimeDecision:
    """Runtime policy decision for VPN actions."""

    decision_id: str
    decision: VpnRuntimeDecision
    contract: VpnPolicyDisableContract
    session_registry: VpnSessionRegistry
    requested_action: str
    allowed: bool
    operator_approval_required: bool
    runtime_execution_performed: bool
    tunnel_created: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    audit_required: bool
    dashboard_visible: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.decision_id != "phase_2_vpn_policy_runtime_decision":
            raise ValueError("decision_id must be phase_2_vpn_policy_runtime_decision")
        if not isinstance(self.contract, VpnPolicyDisableContract):
            raise TypeError("contract must be VpnPolicyDisableContract")
        if not isinstance(self.session_registry, VpnSessionRegistry):
            raise TypeError("session_registry must be VpnSessionRegistry")
        if not isinstance(self.requested_action, str) or not self.requested_action:
            raise ValueError("requested_action must be non-empty")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "operator_approval_required": self.operator_approval_required,
            "audit_required": self.audit_required,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "allowed": self.allowed,
            "runtime_execution_performed": self.runtime_execution_performed,
            "tunnel_created": self.tunnel_created,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision": self.decision,
            "contract": self.contract.to_dict(),
            "session_registry": self.session_registry.to_dict(),
            "requested_action": self.requested_action,
            "allowed": self.allowed,
            "operator_approval_required": self.operator_approval_required,
            "runtime_execution_performed": self.runtime_execution_performed,
            "tunnel_created": self.tunnel_created,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "audit_required": self.audit_required,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def evaluate_vpn_policy_runtime(
    requested_action: str = "start_vpn_session",
    contract: VpnPolicyDisableContract | None = None,
    session_registry: VpnSessionRegistry | None = None,
) -> VpnPolicyRuntimeDecision:
    runtime_contract = contract or build_default_vpn_policy_disable_contract()
    registry = session_registry or build_default_vpn_session_registry()

    if requested_action == "read_status":
        decision = "allow_read_model_only"
        reason_codes = ("vpn_status_read_model_allowed",)
    elif requested_action == "create_tunnel":
        decision = "deny_tunnel_create"
        reason_codes = ("vpn_tunnel_creation_denied_by_policy",)
    else:
        decision = "deny_runtime_start"
        reason_codes = ("vpn_runtime_start_denied_by_policy",)

    return VpnPolicyRuntimeDecision(
        decision_id="phase_2_vpn_policy_runtime_decision",
        decision=decision,
        contract=runtime_contract,
        session_registry=registry,
        requested_action=requested_action,
        allowed=False,
        operator_approval_required=True,
        runtime_execution_performed=False,
        tunnel_created=False,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        audit_required=True,
        dashboard_visible=True,
        containerization_ready=True,
        reason_codes=reason_codes,
    )
