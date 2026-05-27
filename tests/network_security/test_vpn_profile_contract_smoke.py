from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_security.vpn_profile_contract import build_default_vpn_profiles


def test_vpn_profile_contract_smoke() -> None:
    profiles = build_default_vpn_profiles()

    assert profiles
    for profile in profiles:
        assert profile.dashboard_visible is True
        assert profile.disable_safe is True
        assert profile.policy_disable_supported is True
        assert profile.credential_material_present is False
        assert profile.secret_material_embedded is False
        assert profile.tunnel_creation_allowed is False
        assert profile.network_egress_allowed_by_default is False
        assert profile.external_network_access_enabled is False
        assert profile.ports_opened is False
        assert profile.containers_started is False
        assert profile.active_deployment_created is False
        assert profile.runtime_mutation_allowed is False
        assert profile.direct_core_import_allowed is False
        assert profile.source_of_truth_override_allowed is False
        assert profile.containerization_ready is True
