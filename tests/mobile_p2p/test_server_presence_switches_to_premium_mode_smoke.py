from __future__ import annotations

from shared_mobile_core.p2p_mesh_network.server_presence_contract import (
    ServerPresenceContract,
    build_server_presence_contract,
)


def test_server_presence_switches_to_premium_mode_smoke() -> None:
    present = build_server_presence_contract(server_present=True)
    absent = build_server_presence_contract(server_present=False)

    assert isinstance(present, ServerPresenceContract)
    assert present.server_present is True
    assert present.premium_mode_candidate is True
    assert present.floating_master_mode_candidate is False
    assert present.runtime_mode_switch_performed is False

    assert isinstance(absent, ServerPresenceContract)
    assert absent.server_present is False
    assert absent.premium_mode_candidate is False
    assert absent.floating_master_mode_candidate is True
    assert absent.runtime_mode_switch_performed is False

    for state in (present, absent):
        assert state.real_p2p_networking_allowed is False
        assert state.peer_discovery_allowed is False
        assert state.socket_open_allowed is False
        assert state.ports_opened is False
        assert state.external_network_access_enabled is False
        assert state.runtime_mutation_allowed is False
        assert state.source_of_truth_override_allowed is False
        assert state.direct_core_authority_allowed is False
        assert state.dashboard_visible is True
        assert state.read_only is True
        assert state.control_plane_handoff_required is True
        assert state.operator_approval_required is True
        assert state.containerization_ready is True
