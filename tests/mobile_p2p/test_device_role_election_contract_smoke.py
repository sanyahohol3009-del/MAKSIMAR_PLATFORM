from __future__ import annotations

from shared_mobile_core.p2p_mesh_network.device_role_election_contract import (
    DeviceRoleElectionContract,
    build_device_role_election_contract,
)


def test_device_role_election_contract_smoke() -> None:
    election = build_device_role_election_contract()

    assert isinstance(election, DeviceRoleElectionContract)
    assert "floating_master_candidate" in election.candidate_roles
    assert election.selected_role == "none"
    assert election.election_required is True
    assert election.election_execution_allowed is False
    assert election.floating_master_election_execution_allowed is False
    assert election.election_result_committed is False
    assert election.peer_discovery_allowed is False
    assert election.socket_open_allowed is False
    assert election.ports_opened is False
    assert election.external_network_access_enabled is False
    assert election.runtime_mutation_allowed is False
    assert election.source_of_truth_override_allowed is False
    assert election.direct_core_authority_allowed is False
    assert election.dashboard_visible is True
    assert election.read_only is True
    assert election.control_plane_handoff_required is True
    assert election.operator_approval_required is True
    assert election.containerization_ready is True
