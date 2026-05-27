from __future__ import annotations

from shared_mobile_core.p2p_mesh_network.p2p_mesh_contract import (
    P2PMeshContract,
    build_p2p_mesh_contract,
)


def test_p2p_mesh_contract_smoke() -> None:
    mesh = build_p2p_mesh_contract()

    assert isinstance(mesh, P2PMeshContract)
    assert mesh.p2p_adapter.adapter_id == "net_p2p_mesh_adapter"
    assert mesh.disable_policy.p2p_mesh_disabled is True
    assert mesh.p2p_mesh_disabled is True
    assert mesh.real_p2p_networking_allowed is False
    assert mesh.peer_discovery_allowed is False
    assert mesh.socket_open_allowed is False
    assert mesh.ports_opened is False
    assert mesh.external_network_access_enabled is False
    assert mesh.tunnel_creation_allowed is False
    assert mesh.containers_started is False
    assert mesh.active_deployment_created is False
    assert mesh.runtime_mutation_allowed is False
    assert mesh.source_of_truth_override_allowed is False
    assert mesh.direct_core_authority_allowed is False
    assert mesh.dashboard_visible is True
    assert mesh.read_only is True
    assert mesh.control_plane_handoff_required is True
    assert mesh.operator_approval_required is True
    assert mesh.containerization_ready is True
