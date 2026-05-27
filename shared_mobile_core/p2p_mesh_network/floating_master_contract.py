from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.p2p_mesh_network.p2p_mesh_contract import (
    P2PMeshContract,
    build_p2p_mesh_contract,
)


@dataclass(frozen=True, slots=True)
class FloatingMasterContract:
    """Disabled/read-only floating master role contract.

    This models eligibility and policy state only.
    It does not execute master election.
    """

    schema_version: str
    floating_master_id: str
    p2p_mesh: P2PMeshContract
    role_mode: str
    floating_master_allowed: bool
    floating_master_active: bool
    floating_master_election_execution_allowed: bool
    election_result_committed: bool
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
        if self.schema_version != "floating_master_contract.v1":
            raise ValueError("schema_version must be floating_master_contract.v1")
        if self.floating_master_id != "floating_master_disabled_default":
            raise ValueError("floating_master_id must be floating_master_disabled_default")
        if not isinstance(self.p2p_mesh, P2PMeshContract):
            raise TypeError("p2p_mesh must be P2PMeshContract")
        if self.role_mode != "candidate_only":
            raise ValueError("role_mode must be candidate_only")
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
            "floating_master_allowed": self.floating_master_allowed,
            "floating_master_active": self.floating_master_active,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "election_result_committed": self.election_result_committed,
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
            "floating_master_id": self.floating_master_id,
            "p2p_mesh": self.p2p_mesh.to_dict(),
            "role_mode": self.role_mode,
            "floating_master_allowed": self.floating_master_allowed,
            "floating_master_active": self.floating_master_active,
            "floating_master_election_execution_allowed": self.floating_master_election_execution_allowed,
            "election_result_committed": self.election_result_committed,
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


def build_floating_master_contract() -> FloatingMasterContract:
    return FloatingMasterContract(
        schema_version="floating_master_contract.v1",
        floating_master_id="floating_master_disabled_default",
        p2p_mesh=build_p2p_mesh_contract(),
        role_mode="candidate_only",
        floating_master_allowed=False,
        floating_master_active=False,
        floating_master_election_execution_allowed=False,
        election_result_committed=False,
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
        reason_codes=("floating_master_candidate_only_no_election_execution",),
    )
