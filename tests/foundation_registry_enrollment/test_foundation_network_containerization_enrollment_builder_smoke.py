from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    build_foundation_dashboard_visibility_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    build_foundation_layer_manifest_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_network_containerization_enrollment_builder import (
    NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES,
    NetworkContainerizationFoundationEnrollmentReadModel,
    build_network_containerization_foundation_enrollment_read_model,
)


def test_network_containerization_foundation_enrollment_is_registry_visible_and_read_only() -> None:
    read_model = build_network_containerization_foundation_enrollment_read_model()

    assert read_model.read_model_id == "network_containerization_foundation_enrollment_read_model_v1"
    assert read_model.layer_manifest.layer_id == "network_containerization"
    assert read_model.domain_enrollment.registry_domain_id == "network_containerization"
    assert read_model.dashboard_visibility.domain_enrollment.registry_domain_id == "network_containerization"
    assert read_model.existing_network_containerization_surfaces == NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES
    assert read_model.network_containerization_registry_visible is True
    assert read_model.existing_network_containerization_accounted is True
    assert read_model.replaces_network_containerization is False
    assert read_model.migrates_network_containerization is False
    assert read_model.duplicates_network_containerization_logic is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.active_docker_deployment_allowed is False
    assert read_model.active_compose_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_network_containerization_foundation_enrollment_accounts_expected_existing_surfaces() -> None:
    read_model = build_network_containerization_foundation_enrollment_read_model()

    assert "NETWORK_SEGMENTATION/layer_manifest.yaml" in read_model.existing_network_containerization_surfaces
    assert "NETWORK_SEGMENTATION/container_network_rules.yaml" in read_model.existing_network_containerization_surfaces
    assert "CONTAINER_DEPLOYMENT/layer_manifest.yaml" in read_model.existing_network_containerization_surfaces
    assert "CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml" in read_model.existing_network_containerization_surfaces
    assert "MAKSIMAR_CORE_LIB/network_containerization/network_topology_builder.py" in read_model.existing_network_containerization_surfaces
    assert "MAKSIMAR_CORE_LIB/network_containerization/network_containerization_acceptance_read_model.py" in read_model.existing_network_containerization_surfaces
    assert "docs/architecture/foundation/network_containerization_phase_4_final_closure_v1.md" in read_model.existing_network_containerization_surfaces


def test_network_containerization_foundation_enrollment_to_dict_is_inert() -> None:
    payload = build_network_containerization_foundation_enrollment_read_model().to_dict()

    assert payload["network_containerization_registry_visible"] is True
    assert payload["existing_network_containerization_accounted"] is True
    assert payload["replaces_network_containerization"] is False
    assert payload["migrates_network_containerization"] is False
    assert payload["duplicates_network_containerization_logic"] is False
    assert payload["registry_write_allowed"] is False
    assert payload["auto_enrollment_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["active_docker_deployment_allowed"] is False
    assert payload["active_compose_deployment_allowed"] is False
    assert payload["public_exposure_allowed"] is False
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True


def test_network_containerization_foundation_enrollment_rejects_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_network_containerization"):
        NetworkContainerizationFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("network_containerization"),
            domain_enrollment=build_foundation_domain_enrollment_model("network_containerization"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("network_containerization"),
            existing_network_containerization_surfaces=NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES,
            network_containerization_registry_visible=True,
            existing_network_containerization_accounted=True,
            replaces_network_containerization=True,
            migrates_network_containerization=False,
            duplicates_network_containerization_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            active_docker_deployment_allowed=False,
            active_compose_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_network_containerization_foundation_enrollment_rejects_active_docker_deployment() -> None:
    with pytest.raises(ValueError, match="active_docker_deployment_allowed"):
        NetworkContainerizationFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("network_containerization"),
            domain_enrollment=build_foundation_domain_enrollment_model("network_containerization"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("network_containerization"),
            existing_network_containerization_surfaces=NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES,
            network_containerization_registry_visible=True,
            existing_network_containerization_accounted=True,
            replaces_network_containerization=False,
            migrates_network_containerization=False,
            duplicates_network_containerization_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            active_docker_deployment_allowed=True,
            active_compose_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_network_containerization_foundation_enrollment_rejects_wrong_layer_binding() -> None:
    with pytest.raises(ValueError, match="layer_manifest must describe network_containerization"):
        NetworkContainerizationFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("update_recovery_infra"),
            domain_enrollment=build_foundation_domain_enrollment_model("network_containerization"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("network_containerization"),
            existing_network_containerization_surfaces=NETWORK_CONTAINERIZATION_FOUNDATION_EXISTING_SURFACES,
            network_containerization_registry_visible=True,
            existing_network_containerization_accounted=True,
            replaces_network_containerization=False,
            migrates_network_containerization=False,
            duplicates_network_containerization_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            active_docker_deployment_allowed=False,
            active_compose_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
