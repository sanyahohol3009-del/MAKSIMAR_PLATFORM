from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.p2p_mesh_network.floating_master_contract import (
    FloatingMasterContract,
    build_floating_master_contract,
)
from shared_mobile_core.p2p_mesh_network.p2p_mesh_contract import (
    P2PMeshContract,
    build_p2p_mesh_contract,
)


@dataclass(frozen=True, slots=True)
class DeviceRoleElectionContract:
    """Read-only device role election contract.

    This exposes candidate eligibility only. It does not perform election.
    """

    schema_version: str
    election_id: str
    p2p_mesh: P2PMeshContract
    floating_master: FloatingMasterContract
    candidate_roles: tuple[str, ...]
    selected_role: str
    election_required: bool
    election_execution_allowed: bool
    floating_master_election_execution_allowed: bool
    election_result_committed: bool
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
        if self.schema_version != "device_role_election_contract.v1":
            raise ValueError("schema_version must be device_role_election_contract.v1")
        if self.election_id != "device_role_election_disabled_default":
            raise ValueError("election_id must be device_role_election_disabled_default")
        if not isinstance(self.p2p_mesh, P2PMeshContract):
            raise TypeError("p2p_mesh must be P2PMeshContract")
        if not isinstance(self.floating_master, FloatingMasterContract):
            raise TypeError("floating_master must be FloatingMasterContract")
        if self.selected_role != "none":
            raise ValueError("selected_role must remain none")
        if "floating_master_candidate" not in self.candidate_roles:
            raise ValueError("candidate_roles must include floating_master_candidate")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "election_required": self.election_required,
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
            "election_execution_allowed": self.election_execution_allowed,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "election_result_committed": self.election_result_committed,
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
            "election_id": self.election_id,
            "p2p_mesh": self.p2p_mesh.to_dict(),
            "floating_master": self.floating_master.to_dict(),
            "candidate_roles": list(self.candidate_roles),
            "selected_role": self.selected_role,
            "election_required": self.election_required,
            "election_execution_allowed": self.election_execution_allowed,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "election_result_committed": self.election_result_committed,
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


def build_device_role_election_contract() -> DeviceRoleElectionContract:
    return DeviceRoleElectionContract(
        schema_version="device_role_election_contract.v1",
        election_id="device_role_election_disabled_default",
        p2p_mesh=build_p2p_mesh_contract(),
        floating_master=build_floating_master_contract(),
        candidate_roles=("server_node", "android_node", "ios_node", "floating_master_candidate"),
        selected_role="none",
        election_required=True,
        election_execution_allowed=False,
        floating_master_election_execution_allowed=False,
        election_result_committed=False,
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
        reason_codes=("device_role_election_visible_but_execution_blocked",),
    )
