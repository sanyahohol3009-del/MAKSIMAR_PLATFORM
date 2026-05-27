from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.egress_policy_read_model import (
    EgressPolicyReadModel,
    build_default_egress_policy_read_model,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_status_read_model import (
    VpnStatusReadModel,
    build_default_vpn_status_read_model,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.network_posture_summary_builder import (
    NetworkPostureSummary,
    build_network_posture_summary,
)


@dataclass(frozen=True, slots=True)
class VpnDashboardReadModel:
    """Read-only dashboard model for VPN/network security posture."""

    schema_version: str
    dashboard_id: str
    vpn_status: VpnStatusReadModel
    egress_policy: EgressPolicyReadModel
    posture_summary: NetworkPostureSummary
    read_only: bool
    action_buttons_enabled: bool
    control_plane_handoff_required: bool
    direct_execution_allowed: bool
    dashboard_to_runtime_write_allowed: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    external_network_access_enabled: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "vpn_dashboard_read_model.v1":
            raise ValueError("schema_version must be vpn_dashboard_read_model.v1")
        if self.dashboard_id != "phase_2_vpn_dashboard_read_model":
            raise ValueError("dashboard_id must be phase_2_vpn_dashboard_read_model")
        if not isinstance(self.vpn_status, VpnStatusReadModel):
            raise TypeError("vpn_status must be VpnStatusReadModel")
        if not isinstance(self.egress_policy, EgressPolicyReadModel):
            raise TypeError("egress_policy must be EgressPolicyReadModel")
        if not isinstance(self.posture_summary, NetworkPostureSummary):
            raise TypeError("posture_summary must be NetworkPostureSummary")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "action_buttons_enabled": self.action_buttons_enabled,
            "direct_execution_allowed": self.direct_execution_allowed,
            "dashboard_to_runtime_write_allowed": self.dashboard_to_runtime_write_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "external_network_access_enabled": self.external_network_access_enabled,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "dashboard_id": self.dashboard_id,
            "vpn_status": self.vpn_status.to_dict(),
            "egress_policy": self.egress_policy.to_dict(),
            "posture_summary": self.posture_summary.to_dict(),
            "read_only": self.read_only,
            "action_buttons_enabled": self.action_buttons_enabled,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "direct_execution_allowed": self.direct_execution_allowed,
            "dashboard_to_runtime_write_allowed": self.dashboard_to_runtime_write_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "external_network_access_enabled": self.external_network_access_enabled,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_vpn_dashboard_read_model() -> VpnDashboardReadModel:
    return VpnDashboardReadModel(
        schema_version="vpn_dashboard_read_model.v1",
        dashboard_id="phase_2_vpn_dashboard_read_model",
        vpn_status=build_default_vpn_status_read_model(),
        egress_policy=build_default_egress_policy_read_model(),
        posture_summary=build_network_posture_summary(),
        read_only=True,
        action_buttons_enabled=False,
        control_plane_handoff_required=True,
        direct_execution_allowed=False,
        dashboard_to_runtime_write_allowed=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        external_network_access_enabled=False,
        containerization_ready=True,
        reason_codes=(
            "vpn_dashboard_read_model_ready",
            "dashboard_is_read_only",
            "control_buttons_require_future_control_plane_handoff",
        ),
    )
