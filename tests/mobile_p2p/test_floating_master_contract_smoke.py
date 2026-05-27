from __future__ import annotations

from shared_mobile_core.p2p_mesh_network.floating_master_contract import (
    FloatingMasterContract,
    build_floating_master_contract,
)


def test_floating_master_contract_smoke() -> None:
    floating = build_floating_master_contract()

    assert isinstance(floating, FloatingMasterContract)
    assert floating.role_mode == "candidate_only"
    assert floating.floating_master_allowed is False
    assert floating.floating_master_active is False
    assert floating.floating_master_election_execution_allowed is False
    assert floating.election_result_committed is False
    assert floating.real_p2p_networking_allowed is False
    assert floating.peer_discovery_allowed is False
    assert floating.socket_open_allowed is False
    assert floating.ports_opened is False
    assert floating.external_network_access_enabled is False
    assert floating.tunnel_creation_allowed is False
    assert floating.containers_started is False
    assert floating.active_deployment_created is False
    assert floating.runtime_mutation_allowed is False
    assert floating.source_of_truth_override_allowed is False
    assert floating.direct_core_authority_allowed is False
    assert floating.dashboard_visible is True
    assert floating.read_only is True
    assert floating.control_plane_handoff_required is True
    assert floating.operator_approval_required is True
    assert floating.containerization_ready is True
