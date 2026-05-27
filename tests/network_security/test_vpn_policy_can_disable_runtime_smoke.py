from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnPolicyDisableContract,
    build_default_vpn_policy_disable_contract,
)


def test_vpn_policy_can_disable_runtime_smoke() -> None:
    contract = build_default_vpn_policy_disable_contract()

    assert contract.runtime_disabled_by_default is True
    assert contract.server_vpn_disabled is True
    assert contract.mobile_vpn_disabled is True
    assert contract.p2p_mesh_disabled is True
    assert contract.egress_guard_enforce_only is True
    assert contract.dashboard_visible is True
    assert contract.disable_safe is True
    assert contract.policy_disable_supported is True
    assert contract.runtime_mutation_allowed is False
    assert contract.direct_core_import_allowed is False
    assert contract.source_of_truth_override_allowed is False
    assert contract.network_egress_allowed_by_default is False
    assert contract.external_network_access_enabled is False
    assert contract.ports_opened is False
    assert contract.containers_started is False
    assert contract.active_deployment_created is False
    assert contract.containerization_ready is True


def test_vpn_policy_rejects_enabled_external_network_smoke() -> None:
    with pytest.raises(ValueError):
        VpnPolicyDisableContract(
            schema_version="vpn_policy_disable_contract.v1",
            policy_id="phase_2_vpn_policy_disable_contract",
            runtime_disabled_by_default=True,
            server_vpn_disabled=True,
            mobile_vpn_disabled=True,
            p2p_mesh_disabled=True,
            egress_guard_enforce_only=True,
            dashboard_visible=True,
            disable_safe=True,
            policy_disable_supported=True,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            network_egress_allowed_by_default=False,
            external_network_access_enabled=True,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            containerization_ready=True,
            reason_codes=("external_network_must_remain_disabled",),
        )
