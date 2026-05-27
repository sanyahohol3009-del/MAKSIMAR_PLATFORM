from __future__ import annotations

from ANDROID_SHELL.network_vpn.vpn_profile_models import (
    AndroidVpnProfileModel,
    build_android_vpn_profile_model,
)


def test_android_vpn_profile_contract_smoke() -> None:
    profile = build_android_vpn_profile_model()

    assert isinstance(profile, AndroidVpnProfileModel)
    assert profile.platform == "android"
    assert profile.profile_id == "vpn_mobile_profile"
    assert profile.canonical_profile.profile_id == "vpn_mobile_profile"
    assert profile.profile_visible is True
    assert profile.profile_editable_from_android is False
    assert profile.system_api_call_allowed is False
    assert profile.tunnel_creation_allowed is False
    assert profile.permission_prompt_allowed is False
    assert profile.secret_material_embedded is False
    assert profile.credential_material_present is False
    assert profile.external_network_access_enabled is False
    assert profile.ports_opened is False
    assert profile.containers_started is False
    assert profile.active_deployment_created is False
    assert profile.runtime_mutation_allowed is False
    assert profile.source_of_truth_override_allowed is False
    assert profile.direct_core_import_allowed is False
    assert profile.control_plane_handoff_required is True
    assert profile.containerization_ready is True
