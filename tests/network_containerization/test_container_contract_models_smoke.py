from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.container_contract_models import (
    ContainerContractModel,
    build_default_container_contract_model,
)
from MAKSIMAR_CORE_LIB.network_containerization.container_exposure_policy import (
    build_no_public_exposure_policy,
)
from MAKSIMAR_CORE_LIB.network_containerization.container_healthcheck_models import (
    build_default_container_healthcheck_model,
)
from MAKSIMAR_CORE_LIB.network_containerization.restart_policy_models import (
    build_default_restart_policy_model,
)


def test_default_container_contract_is_not_deploying_and_not_public() -> None:
    contract = build_default_container_contract_model()

    assert contract.service_id == "maksimar_blueprint_service"
    assert contract.network_segment == "net_control"
    assert contract.exposure_policy.public_exposure_allowed is False
    assert contract.active_deployment_allowed is False
    assert contract.production_deployment_allowed is False
    assert contract.runtime_network_mutation_allowed is False
    assert contract.dashboard_safe is True


def test_container_contract_rejects_production_deployment_allowed() -> None:
    with pytest.raises(ValueError, match="production_deployment_allowed"):
        ContainerContractModel(
            service_id="bad_service",
            image_source="maksimar/bad:blueprint",
            network_segment="net_control",
            healthcheck=build_default_container_healthcheck_model(),
            restart_policy=build_default_restart_policy_model(),
            exposure_policy=build_no_public_exposure_policy(),
            run_as_non_root_required=True,
            read_only_filesystem_required=True,
            drop_capabilities_required=True,
            no_new_privileges_required=True,
            active_deployment_allowed=False,
            production_deployment_allowed=True,
            runtime_network_mutation_allowed=False,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
