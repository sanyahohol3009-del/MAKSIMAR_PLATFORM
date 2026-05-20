from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_containerization.network_containerization_acceptance_read_model import (
    build_network_containerization_acceptance_read_model,
)


def test_network_containerization_acceptance_read_model_is_safe_and_complete() -> None:
    read_model = build_network_containerization_acceptance_read_model()

    assert read_model.read_model_id == "network_containerization_acceptance_read_model_v1"
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True
    assert read_model.no_public_exposure_by_default is True
    assert read_model.security_layer_green_required is True
    assert read_model.data_plane_green_required is True
    assert read_model.update_recovery_green_required is True
    assert read_model.network_trust_boundaries_accounted is True
    assert read_model.manifest_present is True
    assert read_model.deployment_allowed_now is False
    assert read_model.public_exposure_allowed is False
    assert read_model.runtime_network_mutation_allowed is False


def test_network_containerization_acceptance_read_model_exports_required_commands() -> None:
    read_model = build_network_containerization_acceptance_read_model()

    assert "tests/network_containerization -q" in read_model.acceptance_test_commands
    assert "tests/network_trust_boundaries -q" in read_model.acceptance_test_commands
    assert "pytest -q -n auto" in read_model.acceptance_test_commands

def test_network_containerization_acceptance_read_model_is_exposed_from_package_facade() -> None:
    from MAKSIMAR_CORE_LIB.network_containerization import (
        NetworkContainerizationAcceptanceReadModel,
        build_network_containerization_acceptance_read_model,
    )

    read_model = build_network_containerization_acceptance_read_model()

    assert isinstance(read_model, NetworkContainerizationAcceptanceReadModel)
    assert read_model.read_model_id == "network_containerization_acceptance_read_model_v1"
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True

