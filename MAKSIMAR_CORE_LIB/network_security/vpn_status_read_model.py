from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


VpnStatusViewState = Literal["disabled", "policy_blocked", "read_model_only"]


@dataclass(frozen=True, slots=True)
class VpnStatusReadModel:
    """Dashboard-safe VPN status read model.

    This model is read-only. It never starts VPN runtime, opens ports,
    creates tunnels, starts containers, or mutates source-of-truth state.
    """

    schema_version: str
    view_id: str
    status: VpnStatusViewState
    server_vpn_disabled: bool
    mobile_vpn_disabled: bool
    p2p_mesh_disabled: bool
    tunnel_active: bool
    connected: bool
    runtime_execution_performed: bool
    external_network_access_enabled: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    dashboard_visible: bool
    read_only: bool
    action_buttons_enabled: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "vpn_status_read_model.v1":
            raise ValueError("schema_version must be vpn_status_read_model.v1")
        if self.view_id != "phase_2_vpn_status_read_model":
            raise ValueError("view_id must be phase_2_vpn_status_read_model")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "server_vpn_disabled": self.server_vpn_disabled,
            "mobile_vpn_disabled": self.mobile_vpn_disabled,
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "tunnel_active": self.tunnel_active,
            "connected": self.connected,
            "runtime_execution_performed": self.runtime_execution_performed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "action_buttons_enabled": self.action_buttons_enabled,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "view_id": self.view_id,
            "status": self.status,
            "server_vpn_disabled": self.server_vpn_disabled,
            "mobile_vpn_disabled": self.mobile_vpn_disabled,
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "tunnel_active": self.tunnel_active,
            "connected": self.connected,
            "runtime_execution_performed": self.runtime_execution_performed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "action_buttons_enabled": self.action_buttons_enabled,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_default_vpn_status_read_model() -> VpnStatusReadModel:
    return VpnStatusReadModel(
        schema_version="vpn_status_read_model.v1",
        view_id="phase_2_vpn_status_read_model",
        status="policy_blocked",
        server_vpn_disabled=True,
        mobile_vpn_disabled=True,
        p2p_mesh_disabled=True,
        tunnel_active=False,
        connected=False,
        runtime_execution_performed=False,
        external_network_access_enabled=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
        dashboard_visible=True,
        read_only=True,
        action_buttons_enabled=False,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=("vpn_status_visible_read_only_until_control_plane_handoff",),
    )
