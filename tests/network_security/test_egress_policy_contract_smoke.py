from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_security.egress_policy_contract import (
    EgressPolicyContract,
    build_default_egress_policy_contract,
)


def test_egress_policy_contract_smoke() -> None:
    policy = build_default_egress_policy_contract()

    assert policy.deny_by_default is True
    assert policy.allow_external_network is False
    assert policy.allow_dns_resolution is False
    assert policy.allow_public_ingress is False
    assert policy.allow_tunnel_creation is False
    assert policy.require_operator_approval is True
    assert policy.dashboard_visible is True
    assert policy.runtime_mutation_allowed is False
    assert policy.direct_core_import_allowed is False
    assert policy.source_of_truth_override_allowed is False
    assert policy.ports_opened is False
    assert policy.containers_started is False
    assert policy.active_deployment_created is False
    assert policy.containerization_ready is True


def test_egress_policy_rejects_external_network_smoke() -> None:
    with pytest.raises(ValueError):
        EgressPolicyContract(
            policy_id="phase_2_egress_policy_contract",
            decision="deny_by_default",
            deny_by_default=True,
            allow_external_network=True,
            allow_dns_resolution=False,
            allow_public_ingress=False,
            allow_tunnel_creation=False,
            require_operator_approval=True,
            dashboard_visible=True,
            runtime_mutation_allowed=False,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            containerization_ready=True,
            reason_codes=("external_network_forbidden",),
        )
