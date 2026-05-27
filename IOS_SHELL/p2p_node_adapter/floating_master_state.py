from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.p2p_mesh_network.device_role_election_contract import (
    DeviceRoleElectionContract,
    build_device_role_election_contract,
)
from shared_mobile_core.p2p_mesh_network.floating_master_contract import (
    FloatingMasterContract,
    build_floating_master_contract,
)
from shared_mobile_core.p2p_mesh_network.server_presence_contract import (
    ServerPresenceContract,
    build_server_presence_contract,
)


@dataclass(frozen=True, slots=True)
class IosFloatingMasterState:
    """iOS shell projection of floating-master state.

    It is candidate visibility only. It does not execute election or switch runtime mode.
    """

    schema_version: str
    state_id: str
    platform: str
    shell_surface: str
    floating_master: FloatingMasterContract
    device_role_election: DeviceRoleElectionContract
    server_presence: ServerPresenceContract
    candidate_visible: bool
    local_candidate_role: str
    floating_master_active: bool
    floating_master_election_execution_allowed: bool
    role_election_commit_allowed: bool
    runtime_mode_switch_performed: bool
    platform_api_execution_allowed: bool
    system_network_call_allowed: bool
    permission_prompt_allowed: bool
    real_p2p_networking_allowed: bool
    peer_discovery_allowed: bool
    socket_open_allowed: bool
    ports_opened: bool
    external_network_access_enabled: bool
    tunnel_creation_allowed: bool
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
        if self.schema_version != "ios_floating_master_state.v1":
            raise ValueError("schema_version must be ios_floating_master_state.v1")
        if self.state_id != "ios_floating_master_state_disabled_default":
            raise ValueError("state_id must be ios_floating_master_state_disabled_default")
        if self.platform != "ios":
            raise ValueError("platform must be ios")
        if self.shell_surface != "IOS_SHELL/p2p_node_adapter":
            raise ValueError("shell_surface must be IOS_SHELL/p2p_node_adapter")
        if not isinstance(self.floating_master, FloatingMasterContract):
            raise TypeError("floating_master must be FloatingMasterContract")
        if not isinstance(self.device_role_election, DeviceRoleElectionContract):
            raise TypeError("device_role_election must be DeviceRoleElectionContract")
        if not isinstance(self.server_presence, ServerPresenceContract):
            raise TypeError("server_presence must be ServerPresenceContract")
        if self.local_candidate_role != "ios_node":
            raise ValueError("local_candidate_role must be ios_node")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "candidate_visible": self.candidate_visible,
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
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "role_election_commit_allowed": self.role_election_commit_allowed,
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
            "platform_api_execution_allowed": self.platform_api_execution_allowed,
            "system_network_call_allowed": self.system_network_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
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
            "state_id": self.state_id,
            "platform": self.platform,
            "shell_surface": self.shell_surface,
            "floating_master": self.floating_master.to_dict(),
            "device_role_election": self.device_role_election.to_dict(),
            "server_presence": self.server_presence.to_dict(),
            "candidate_visible": self.candidate_visible,
            "local_candidate_role": self.local_candidate_role,
            "floating_master_active": self.floating_master_active,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "role_election_commit_allowed": self.role_election_commit_allowed,
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
            "platform_api_execution_allowed": self.platform_api_execution_allowed,
            "system_network_call_allowed": self.system_network_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
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


def build_ios_floating_master_state(server_present: bool = True) -> IosFloatingMasterState:
    return IosFloatingMasterState(
        schema_version="ios_floating_master_state.v1",
        state_id="ios_floating_master_state_disabled_default",
        platform="ios",
        shell_surface="IOS_SHELL/p2p_node_adapter",
        floating_master=build_floating_master_contract(),
        device_role_election=build_device_role_election_contract(),
        server_presence=build_server_presence_contract(server_present=server_present),
        candidate_visible=True,
        local_candidate_role="ios_node",
        floating_master_active=False,
        floating_master_election_execution_allowed=False,
        role_election_commit_allowed=False,
        runtime_mode_switch_performed=False,
        platform_api_execution_allowed=False,
        system_network_call_allowed=False,
        permission_prompt_allowed=False,
        real_p2p_networking_allowed=False,
        peer_discovery_allowed=False,
        socket_open_allowed=False,
        ports_opened=False,
        external_network_access_enabled=False,
        tunnel_creation_allowed=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_authority_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=("ios_floating_master_state_candidate_visible_no_execution",),
    )
