from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ANDROID_SHELL.p2p_node_adapter.floating_master_state import (
    AndroidFloatingMasterState,
    build_android_floating_master_state,
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
class AndroidP2PNodeStateBridge:
    """Android shell bridge over shared P2P/Floating Master contracts."""

    schema_version: str
    bridge_id: str
    platform: str
    shell_surface: str
    p2p_mesh: P2PMeshContract
    floating_master: FloatingMasterContract
    device_role_election: DeviceRoleElectionContract
    server_presence: ServerPresenceContract
    floating_master_state: AndroidFloatingMasterState
    bridge_ready: bool
    node_role: str
    source_layer: str
    canonical_policy_layer: str
    real_p2p_networking_allowed: bool
    peer_discovery_allowed: bool
    socket_open_allowed: bool
    ports_opened: bool
    external_network_access_enabled: bool
    tunnel_creation_allowed: bool
    floating_master_election_execution_allowed: bool
    platform_api_execution_allowed: bool
    system_network_call_allowed: bool
    permission_prompt_allowed: bool
    role_election_commit_allowed: bool
    runtime_mode_switch_performed: bool
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
        if self.schema_version != "android_p2p_node_state_bridge.v1":
            raise ValueError("schema_version must be android_p2p_node_state_bridge.v1")
        if self.bridge_id != "android_p2p_node_state_bridge_disabled_default":
            raise ValueError("bridge_id must be android_p2p_node_state_bridge_disabled_default")
        if self.platform != "android":
            raise ValueError("platform must be android")
        if self.shell_surface != "ANDROID_SHELL/p2p_node_adapter":
            raise ValueError("shell_surface must be ANDROID_SHELL/p2p_node_adapter")
        if self.node_role != "android_node":
            raise ValueError("node_role must be android_node")
        if self.source_layer != "shared_mobile_core/p2p_mesh_network":
            raise ValueError("source_layer must remain shared_mobile_core/p2p_mesh_network")
        if self.canonical_policy_layer != "MAKSIMAR_CORE_LIB/network_security":
            raise ValueError("canonical_policy_layer must remain MAKSIMAR_CORE_LIB/network_security")
        if not isinstance(self.p2p_mesh, P2PMeshContract):
            raise TypeError("p2p_mesh must be P2PMeshContract")
        if not isinstance(self.floating_master, FloatingMasterContract):
            raise TypeError("floating_master must be FloatingMasterContract")
        if not isinstance(self.device_role_election, DeviceRoleElectionContract):
            raise TypeError("device_role_election must be DeviceRoleElectionContract")
        if not isinstance(self.server_presence, ServerPresenceContract):
            raise TypeError("server_presence must be ServerPresenceContract")
        if not isinstance(self.floating_master_state, AndroidFloatingMasterState):
            raise TypeError("floating_master_state must be AndroidFloatingMasterState")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "bridge_ready": self.bridge_ready,
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
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "platform_api_execution_allowed": self.platform_api_execution_allowed,
            "system_network_call_allowed": self.system_network_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "role_election_commit_allowed": self.role_election_commit_allowed,
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
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
            "bridge_id": self.bridge_id,
            "platform": self.platform,
            "shell_surface": self.shell_surface,
            "p2p_mesh": self.p2p_mesh.to_dict(),
            "floating_master": self.floating_master.to_dict(),
            "device_role_election": self.device_role_election.to_dict(),
            "server_presence": self.server_presence.to_dict(),
            "floating_master_state": self.floating_master_state.to_dict(),
            "bridge_ready": self.bridge_ready,
            "node_role": self.node_role,
            "source_layer": self.source_layer,
            "canonical_policy_layer": self.canonical_policy_layer,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_creation_allowed": self.tunnel_creation_allowed,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "platform_api_execution_allowed": self.platform_api_execution_allowed,
            "system_network_call_allowed": self.system_network_call_allowed,
            "permission_prompt_allowed": self.permission_prompt_allowed,
            "role_election_commit_allowed": self.role_election_commit_allowed,
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
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


def build_android_p2p_node_state_bridge(server_present: bool = True) -> AndroidP2PNodeStateBridge:
    return AndroidP2PNodeStateBridge(
        schema_version="android_p2p_node_state_bridge.v1",
        bridge_id="android_p2p_node_state_bridge_disabled_default",
        platform="android",
        shell_surface="ANDROID_SHELL/p2p_node_adapter",
        p2p_mesh=build_p2p_mesh_contract(),
        floating_master=build_floating_master_contract(),
        device_role_election=build_device_role_election_contract(),
        server_presence=build_server_presence_contract(server_present=server_present),
        floating_master_state=build_android_floating_master_state(server_present=server_present),
        bridge_ready=True,
        node_role="android_node",
        source_layer="shared_mobile_core/p2p_mesh_network",
        canonical_policy_layer="MAKSIMAR_CORE_LIB/network_security",
        real_p2p_networking_allowed=False,
        peer_discovery_allowed=False,
        socket_open_allowed=False,
        ports_opened=False,
        external_network_access_enabled=False,
        tunnel_creation_allowed=False,
        floating_master_election_execution_allowed=False,
        platform_api_execution_allowed=False,
        system_network_call_allowed=False,
        permission_prompt_allowed=False,
        role_election_commit_allowed=False,
        runtime_mode_switch_performed=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_authority_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=("android_p2p_node_adapter_projects_shared_p2p_state",),
    )
