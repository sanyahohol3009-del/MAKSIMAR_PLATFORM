from __future__ import annotations

from IOS_SHELL.network_vpn.vpn_state_bridge import (
    IosVpnStateBridge,
    build_ios_vpn_state_bridge,
)


def test_ios_vpn_state_bridge_smoke() -> None:
    bridge = build_ios_vpn_state_bridge()

    assert isinstance(bridge, IosVpnStateBridge)
    assert bridge.platform == "ios"
    assert bridge.mobile_hook.platform == "ios"
    assert bridge.session.profile_id == "vpn_mobile_profile"
    assert bridge.bridge_active is False
    assert bridge.tunnel_active is False
    assert bridge.connected is False
    assert bridge.system_api_call_allowed is False
    assert bridge.network_extension_api_call_allowed is False
    assert bridge.nevpn_api_call_allowed is False
    assert bridge.permission_prompt_allowed is False
    assert bridge.permission_prompt_executed is False
    assert bridge.external_network_access_enabled is False
    assert bridge.ports_opened is False
    assert bridge.containers_started is False
    assert bridge.active_deployment_created is False
    assert bridge.runtime_mutation_allowed is False
    assert bridge.source_of_truth_override_allowed is False
    assert bridge.direct_core_import_allowed is False
    assert bridge.dashboard_visible is True
    assert bridge.read_only is True
    assert bridge.control_plane_handoff_required is True
    assert bridge.containerization_ready is True
