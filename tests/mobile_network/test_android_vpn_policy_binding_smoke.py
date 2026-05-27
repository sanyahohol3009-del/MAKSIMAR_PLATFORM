from __future__ import annotations

from ANDROID_SHELL.network_vpn.android_vpn_policy_binding import (
    AndroidVpnPolicyBinding,
    build_android_vpn_policy_binding,
)


def test_android_vpn_policy_binding_smoke() -> None:
    binding = build_android_vpn_policy_binding()

    assert isinstance(binding, AndroidVpnPolicyBinding)
    assert binding.platform == "android"
    assert binding.source_of_truth_layer == "MAKSIMAR_CORE_LIB/network_security"
    assert binding.runtime_layer == "MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME"
    assert binding.shell_layer == "ANDROID_SHELL/network_vpn"
    assert binding.android_shell_binding_ready is True
    assert binding.policy_disabled is True
    assert binding.control_plane_handoff_required is True
    assert binding.operator_approval_required is True
    assert binding.system_api_call_allowed is False
    assert binding.permission_prompt_allowed is False
    assert binding.tunnel_creation_allowed is False
    assert binding.secret_material_embedded is False
    assert binding.credential_material_present is False
    assert binding.external_network_access_enabled is False
    assert binding.ports_opened is False
    assert binding.containers_started is False
    assert binding.active_deployment_created is False
    assert binding.runtime_mutation_allowed is False
    assert binding.source_of_truth_override_allowed is False
    assert binding.direct_core_import_allowed is False
    assert binding.dashboard_visible is True
    assert binding.read_only is True
    assert binding.containerization_ready is True

    payload = binding.to_dict()
    assert payload["profile"]["canonical_profile"]["profile_id"] == "vpn_mobile_profile"
    assert payload["vpn_policy"]["mobile_vpn_disabled"] is True
    assert payload["egress_policy"]["deny_by_default"] is True
