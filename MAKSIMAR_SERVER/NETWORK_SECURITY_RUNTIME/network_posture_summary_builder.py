from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.egress_guard_runtime import (
    EgressGuardRuntimeDecision,
    evaluate_egress_guard_runtime,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_policy_runtime import (
    VpnPolicyRuntimeDecision,
    evaluate_vpn_policy_runtime,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_session_registry import (
    VpnSessionRegistry,
    build_default_vpn_session_registry,
)


@dataclass(frozen=True, slots=True)
class NetworkPostureSummary:
    """Dashboard-ready network posture summary."""

    schema_version: str
    summary_id: str
    session_registry: VpnSessionRegistry
    vpn_decision: VpnPolicyRuntimeDecision
    egress_decision: EgressGuardRuntimeDecision
    network_security_runtime_ready: bool
    runtime_policy_gated: bool
    vpn_runtime_disabled: bool
    egress_denied_by_default: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    dashboard_visible: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "network_posture_summary.v1":
            raise ValueError("schema_version must be network_posture_summary.v1")
        if self.summary_id != "phase_2_network_posture_summary":
            raise ValueError("summary_id must be phase_2_network_posture_summary")
        if not isinstance(self.session_registry, VpnSessionRegistry):
            raise TypeError("session_registry must be VpnSessionRegistry")
        if not isinstance(self.vpn_decision, VpnPolicyRuntimeDecision):
            raise TypeError("vpn_decision must be VpnPolicyRuntimeDecision")
        if not isinstance(self.egress_decision, EgressGuardRuntimeDecision):
            raise TypeError("egress_decision must be EgressGuardRuntimeDecision")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "network_security_runtime_ready": self.network_security_runtime_ready,
            "runtime_policy_gated": self.runtime_policy_gated,
            "vpn_runtime_disabled": self.vpn_runtime_disabled,
            "egress_denied_by_default": self.egress_denied_by_default,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "external_network_access_enabled": self.external_network_access_enabled,
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
            "schema_version": self.schema_version,
            "summary_id": self.summary_id,
            "session_registry": self.session_registry.to_dict(),
            "vpn_decision": self.vpn_decision.to_dict(),
            "egress_decision": self.egress_decision.to_dict(),
            "network_security_runtime_ready": self.network_security_runtime_ready,
            "runtime_policy_gated": self.runtime_policy_gated,
            "vpn_runtime_disabled": self.vpn_runtime_disabled,
            "egress_denied_by_default": self.egress_denied_by_default,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_visible": self.dashboard_visible,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_network_posture_summary() -> NetworkPostureSummary:
    registry = build_default_vpn_session_registry()
    vpn_decision = evaluate_vpn_policy_runtime(session_registry=registry)
    egress_decision = evaluate_egress_guard_runtime()

    return NetworkPostureSummary(
        schema_version="network_posture_summary.v1",
        summary_id="phase_2_network_posture_summary",
        session_registry=registry,
        vpn_decision=vpn_decision,
        egress_decision=egress_decision,
        network_security_runtime_ready=True,
        runtime_policy_gated=True,
        vpn_runtime_disabled=True,
        egress_denied_by_default=True,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        dashboard_visible=True,
        containerization_ready=True,
        reason_codes=(
            "server_network_security_runtime_ready",
            "vpn_disabled_by_policy",
            "egress_denied_by_default",
        ),
    )
