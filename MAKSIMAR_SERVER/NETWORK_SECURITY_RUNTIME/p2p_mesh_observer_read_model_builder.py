from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.network_security.egress_policy_contract import (
    EgressPolicyContract,
    build_default_egress_policy_contract,
)
from MAKSIMAR_CORE_LIB.network_security.vpn_status_read_model import (
    VpnStatusReadModel,
    build_default_vpn_status_read_model,
)
from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.network_posture_summary_builder import (
    NetworkPostureSummary,
    build_network_posture_summary,
)
from shared_mobile_core.p2p_mesh_network.device_role_election_contract import (
    DeviceRoleElectionContract,
    build_device_role_election_contract,
)
from shared_mobile_core.p2p_mesh_network.floating_master_contract import (
    FloatingMasterContract,
    build_floating_master_contract,
)
from shared_mobile_core.p2p_mesh_network.p2p_mesh_contract import (
    P2PMeshContract,
    build_p2p_mesh_contract,
)
from shared_mobile_core.p2p_mesh_network.server_presence_contract import (
    ServerPresenceContract,
    build_server_presence_contract,
)


@dataclass(frozen=True, slots=True)
class P2PMeshObserverReadModel:
    """Server-side read-only observer for P2P mesh / floating master posture."""

    schema_version: str
    observer_id: str
    p2p_mesh: P2PMeshContract
    floating_master: FloatingMasterContract
    device_role_election: DeviceRoleElectionContract
    server_presence: ServerPresenceContract
    network_posture_summary: NetworkPostureSummary
    vpn_status: VpnStatusReadModel
    egress_policy: EgressPolicyContract
    observer_ready: bool
    p2p_mesh_disabled: bool
    floating_master_active: bool
    real_p2p_networking_allowed: bool
    peer_discovery_allowed: bool
    socket_open_allowed: bool
    ports_opened: bool
    external_network_access_enabled: bool
    tunnel_creation_allowed: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    source_of_truth_override_allowed: bool
    direct_core_authority_allowed: bool
    dashboard_visible: bool
    read_only: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "p2p_mesh_observer_read_model.v1":
            raise ValueError("schema_version must be p2p_mesh_observer_read_model.v1")
        if self.observer_id != "phase_2_p2p_mesh_observer_read_model":
            raise ValueError("observer_id must be phase_2_p2p_mesh_observer_read_model")
        if not isinstance(self.p2p_mesh, P2PMeshContract):
            raise TypeError("p2p_mesh must be P2PMeshContract")
        if not isinstance(self.floating_master, FloatingMasterContract):
            raise TypeError("floating_master must be FloatingMasterContract")
        if not isinstance(self.device_role_election, DeviceRoleElectionContract):
            raise TypeError("device_role_election must be DeviceRoleElectionContract")
        if not isinstance(self.server_presence, ServerPresenceContract):
            raise TypeError("server_presence must be ServerPresenceContract")
        if not isinstance(self.network_posture_summary, NetworkPostureSummary):
            raise TypeError("network_posture_summary must be NetworkPostureSummary")
        if not isinstance(self.vpn_status, VpnStatusReadModel):
            raise TypeError("vpn_status must be VpnStatusReadModel")
        if not isinstance(self.egress_policy, EgressPolicyContract):
            raise TypeError("egress_policy must be EgressPolicyContract")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "observer_ready": self.observer_ready,
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
            "floating_master_active": self.floating_master_active,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_authority_allowed": self.direct_core_authority_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "observer_id": self.observer_id,
            "p2p_mesh": self.p2p_mesh.to_dict(),
            "floating_master": self.floating_master.to_dict(),
            "device_role_election": self.device_role_election.to_dict(),
            "server_presence": self.server_presence.to_dict(),
            "network_posture_summary": self.network_posture_summary.to_dict(),
            "vpn_status": self.vpn_status.to_dict(),
            "egress_policy": self.egress_policy.to_dict(),
            "observer_ready": self.observer_ready,
            "p2p_mesh_disabled": self.p2p_mesh_disabled,
            "floating_master_active": self.floating_master_active,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "direct_core_authority_allowed": self.direct_core_authority_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_p2p_mesh_observer_read_model(server_present: bool = True) -> P2PMeshObserverReadModel:
    return P2PMeshObserverReadModel(
        schema_version="p2p_mesh_observer_read_model.v1",
        observer_id="phase_2_p2p_mesh_observer_read_model",
        p2p_mesh=build_p2p_mesh_contract(),
        floating_master=build_floating_master_contract(),
        device_role_election=build_device_role_election_contract(),
        server_presence=build_server_presence_contract(server_present=server_present),
        network_posture_summary=build_network_posture_summary(),
        vpn_status=build_default_vpn_status_read_model(),
        egress_policy=build_default_egress_policy_contract(),
        observer_ready=True,
        p2p_mesh_disabled=True,
        floating_master_active=False,
        real_p2p_networking_allowed=False,
        peer_discovery_allowed=False,
        socket_open_allowed=False,
        ports_opened=False,
        external_network_access_enabled=False,
        tunnel_creation_allowed=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_authority_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=(
            "p2p_mesh_observer_ready",
            "canonical_network_security_policy_reused",
            "no_p2p_runtime_execution",
        ),
    )
