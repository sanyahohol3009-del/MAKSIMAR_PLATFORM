from __future__ import annotations

from IOS_SHELL.p2p_node_adapter.floating_master_state import (
    IosFloatingMasterState,
    build_ios_floating_master_state,
)
from IOS_SHELL.p2p_node_adapter.p2p_node_state_bridge import (
    IosP2PNodeStateBridge,
    build_ios_p2p_node_state_bridge,
)


def test_ios_p2p_node_state_bridge_smoke() -> None:
    bridge = build_ios_p2p_node_state_bridge(server_present=True)
    floating = build_ios_floating_master_state(server_present=False)

    assert isinstance(bridge, IosP2PNodeStateBridge)
    assert isinstance(floating, IosFloatingMasterState)
    assert bridge.platform == "ios"
    assert bridge.node_role == "ios_node"
    assert bridge.source_layer == "shared_mobile_core/p2p_mesh_network"
    assert bridge.canonical_policy_layer == "MAKSIMAR_CORE_LIB/network_security"
    assert bridge.p2p_mesh.p2p_mesh_disabled is True
    assert bridge.floating_master.floating_master_active is False
    assert bridge.device_role_election.selected_role == "none"
    assert bridge.server_presence.premium_mode_candidate is True
    assert floating.server_presence.floating_master_mode_candidate is True

    for state in (bridge, floating):
        assert state.real_p2p_networking_allowed is False
        assert state.peer_discovery_allowed is False
        assert state.socket_open_allowed is False
        assert state.ports_opened is False
        assert state.external_network_access_enabled is False
        assert state.tunnel_creation_allowed is False
        assert state.floating_master_election_execution_allowed is False
        assert state.platform_api_execution_allowed is False
        assert state.system_network_call_allowed is False
        assert state.runtime_mutation_allowed is False
        assert state.source_of_truth_override_allowed is False
        assert state.direct_core_authority_allowed is False
        assert state.dashboard_visible is True
        assert state.read_only is True
        assert state.control_plane_handoff_required is True
        assert state.operator_approval_required is True
        assert state.containerization_ready is True
