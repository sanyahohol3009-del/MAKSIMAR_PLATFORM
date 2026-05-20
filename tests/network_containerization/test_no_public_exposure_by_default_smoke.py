from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_containerization import (
    build_container_deployment_read_model,
    build_default_container_contract_model,
    build_default_network_segments,
    build_network_topology_read_model,
    build_no_public_exposure_policy,
)


def test_no_public_exposure_by_default_across_network_container_models() -> None:
    segments = build_default_network_segments()
    exposure_policy = build_no_public_exposure_policy()
    contract = build_default_container_contract_model()
    topology = build_network_topology_read_model()
    deployment = build_container_deployment_read_model()

    assert all(segment.public_exposure_allowed is False for segment in segments)
    assert exposure_policy.public_exposure_allowed is False
    assert contract.exposure_policy.public_exposure_allowed is False
    assert topology.public_exposure_allowed is False
    assert deployment.public_exposure_allowed is False
    assert deployment.deployment_allowed_now is False
