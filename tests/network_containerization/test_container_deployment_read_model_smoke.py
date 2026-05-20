from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.container_deployment_read_model import (
    ContainerDeploymentReadModel,
    build_container_deployment_read_model,
)
from MAKSIMAR_CORE_LIB.network_containerization.network_topology_builder import (
    build_network_topology_read_model,
)


def test_container_deployment_read_model_is_dashboard_safe_and_inert() -> None:
    read_model = build_container_deployment_read_model()

    assert read_model.read_model_id == "container_deployment_read_model_v1"
    assert read_model.deployment_allowed_now is False
    assert read_model.active_docker_deployment_allowed is False
    assert read_model.active_compose_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.runtime_network_mutation_allowed is False
    assert read_model.dashboard_safe is True


def test_container_deployment_read_model_rejects_runtime_network_mutation() -> None:
    with pytest.raises(ValueError, match="runtime_network_mutation_allowed"):
        ContainerDeploymentReadModel(
            read_model_id="bad",
            topology=build_network_topology_read_model(),
            container_deployment_blueprint_path="CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml",
            container_contract_schema_path="CONTAINER_DEPLOYMENT/container_contract.schema.yaml",
            security_required_gate_path="CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml",
            foundation_green_gate_path="CONTAINER_DEPLOYMENT/no_production_deploy_until_foundation_green.yaml",
            deployment_allowed_now=False,
            active_docker_deployment_allowed=False,
            active_compose_deployment_allowed=False,
            public_exposure_allowed=False,
            runtime_network_mutation_allowed=True,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
