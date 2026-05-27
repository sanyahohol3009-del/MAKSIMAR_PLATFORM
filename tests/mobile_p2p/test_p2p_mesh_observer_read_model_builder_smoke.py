from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.p2p_mesh_observer_read_model_builder import (
    P2PMeshObserverReadModel,
    build_p2p_mesh_observer_read_model,
)


def test_p2p_mesh_observer_read_model_builder_smoke() -> None:
    observer = build_p2p_mesh_observer_read_model(server_present=True)

    assert isinstance(observer, P2PMeshObserverReadModel)
    assert observer.observer_ready is True
    assert observer.p2p_mesh_disabled is True
    assert observer.floating_master_active is False
    assert observer.real_p2p_networking_allowed is False
    assert observer.peer_discovery_allowed is False
    assert observer.socket_open_allowed is False
    assert observer.ports_opened is False
    assert observer.external_network_access_enabled is False
    assert observer.tunnel_creation_allowed is False
    assert observer.containers_started is False
    assert observer.active_deployment_created is False
    assert observer.runtime_mutation_allowed is False
    assert observer.source_of_truth_override_allowed is False
    assert observer.direct_core_authority_allowed is False
    assert observer.dashboard_visible is True
    assert observer.read_only is True
    assert observer.control_plane_handoff_required is True
    assert observer.operator_approval_required is True
    assert observer.containerization_ready is True

    payload = observer.to_dict()
    assert payload["p2p_mesh"]["p2p_adapter"]["adapter_id"] == "net_p2p_mesh_adapter"
    assert payload["vpn_status"]["p2p_mesh_disabled"] is True
    assert payload["server_presence"]["premium_mode_candidate"] is True
