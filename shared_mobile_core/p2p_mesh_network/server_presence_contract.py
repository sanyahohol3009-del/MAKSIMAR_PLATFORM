from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.p2p_mesh_network.device_role_election_contract import (
    DeviceRoleElectionContract,
    build_device_role_election_contract,
)


@dataclass(frozen=True, slots=True)
class ServerPresenceContract:
    """Server presence contract for premium/floating-master mode selection.

    This models mode selection only. It does not switch runtime/network mode.
    """

    schema_version: str
    presence_id: str
    election: DeviceRoleElectionContract
    server_present: bool
    premium_mode_candidate: bool
    floating_master_mode_candidate: bool
    runtime_mode_switch_performed: bool
    real_p2p_networking_allowed: bool
    peer_discovery_allowed: bool
    socket_open_allowed: bool
    ports_opened: bool
    external_network_access_enabled: bool
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
        if self.schema_version != "server_presence_contract.v1":
            raise ValueError("schema_version must be server_presence_contract.v1")
        if self.presence_id not in {"server_presence_observed", "server_presence_absent"}:
            raise ValueError("presence_id must be server_presence_observed or server_presence_absent")
        if not isinstance(self.election, DeviceRoleElectionContract):
            raise TypeError("election must be DeviceRoleElectionContract")
        if self.premium_mode_candidate is not self.server_present:
            raise ValueError("premium_mode_candidate must mirror server_present")
        if self.floating_master_mode_candidate is self.server_present:
            raise ValueError("floating_master_mode_candidate must be inverse of server_present")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
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
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
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
            "presence_id": self.presence_id,
            "election": self.election.to_dict(),
            "server_present": self.server_present,
            "premium_mode_candidate": self.premium_mode_candidate,
            "floating_master_mode_candidate": self.floating_master_mode_candidate,
            "runtime_mode_switch_performed": self.runtime_mode_switch_performed,
            "real_p2p_networking_allowed": self.real_p2p_networking_allowed,
            "peer_discovery_allowed": self.peer_discovery_allowed,
            "socket_open_allowed": self.socket_open_allowed,
            "ports_opened": self.ports_opened,
            "external_network_access_enabled": self.external_network_access_enabled,
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


def build_server_presence_contract(server_present: bool = True) -> ServerPresenceContract:
    return ServerPresenceContract(
        schema_version="server_presence_contract.v1",
        presence_id="server_presence_observed" if server_present else "server_presence_absent",
        election=build_device_role_election_contract(),
        server_present=server_present,
        premium_mode_candidate=server_present,
        floating_master_mode_candidate=not server_present,
        runtime_mode_switch_performed=False,
        real_p2p_networking_allowed=False,
        peer_discovery_allowed=False,
        socket_open_allowed=False,
        ports_opened=False,
        external_network_access_enabled=False,
        runtime_mutation_allowed=False,
        source_of_truth_override_allowed=False,
        direct_core_authority_allowed=False,
        dashboard_visible=True,
        read_only=True,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        containerization_ready=True,
        reason_codes=(
            (
                "server_presence_visible_premium_mode_candidate"
                if server_present
                else "server_absent_floating_master_candidate_without_runtime_switch"
            ),
        ),
    )
