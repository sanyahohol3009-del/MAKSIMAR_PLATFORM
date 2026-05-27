from __future__ import annotations

from IOS_SHELL.network_vpn.ios_vpn_policy_binding import build_ios_vpn_policy_binding


def test_vpn_capability_required_ios_smoke() -> None:
    binding = build_ios_vpn_policy_binding()

    assert binding.ios_shell_binding_ready is True
    assert binding.profile.profile_id == "vpn_mobile_profile"
    assert binding.permission_state.permission_prompt_allowed is False
    assert binding.state_bridge.mobile_hook.platform == "ios"
    assert binding.state_bridge.mobile_hook.profile_id == "vpn_mobile_profile"
    assert binding.sync_contract.sync_enabled is False
    assert binding.control_plane_handoff_required is True
    assert binding.operator_approval_required is True

    assert binding.system_api_call_allowed is False
    assert binding.network_extension_api_call_allowed is False
    assert binding.nevpn_api_call_allowed is False
    assert binding.permission_prompt_allowed is False
    assert binding.tunnel_creation_allowed is False
    assert binding.secret_material_embedded is False
    assert binding.credential_material_present is False
    assert binding.external_network_access_enabled is False
    assert binding.ports_opened is False
    assert binding.containers_started is False
    assert binding.active_deployment_created is False
    assert binding.runtime_mutation_allowed is False
