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
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_update_recovery_enrollment_builder import (
    UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES,
    UpdateRecoveryFoundationEnrollmentReadModel,
    build_update_recovery_foundation_enrollment_read_model,
)


def test_update_recovery_foundation_enrollment_is_registry_visible_and_read_only() -> None:
    read_model = build_update_recovery_foundation_enrollment_read_model()

    assert read_model.read_model_id == "update_recovery_foundation_enrollment_read_model_v1"
    assert read_model.layer_manifest.layer_id == "update_recovery_infra"
    assert read_model.domain_enrollment.registry_domain_id == "update_recovery_infra"
    assert read_model.dashboard_visibility.domain_enrollment.registry_domain_id == "update_recovery_infra"
    assert read_model.existing_update_recovery_surfaces == UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES
    assert read_model.update_recovery_registry_visible is True
    assert read_model.existing_update_recovery_accounted is True
    assert read_model.replaces_update_recovery is False
    assert read_model.migrates_update_recovery is False
    assert read_model.duplicates_update_recovery_logic is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_update_recovery_foundation_enrollment_accounts_expected_existing_surfaces() -> None:
    read_model = build_update_recovery_foundation_enrollment_read_model()

    assert "UPDATE_RECOVERY/layer_manifest.yaml" in read_model.existing_update_recovery_surfaces
    assert "UPDATE_RECOVERY/container_contract.yaml" in read_model.existing_update_recovery_surfaces
    assert "MAKSIMAR_CORE_LIB/update_recovery/update_recovery_read_model.py" in read_model.existing_update_recovery_surfaces
    assert "MAKSIMAR_CORE_LIB/update_recovery/signed_update_service_contract.py" in read_model.existing_update_recovery_surfaces
    assert "MAKSIMAR_SERVER/UPDATE_RECOVERY/update_recovery_read_model_builder.py" in read_model.existing_update_recovery_surfaces
    assert "docs/architecture/foundation/update_recovery_infra_foundation_v1.md" in read_model.existing_update_recovery_surfaces


def test_update_recovery_foundation_enrollment_to_dict_is_inert() -> None:
    payload = build_update_recovery_foundation_enrollment_read_model().to_dict()

    assert payload["update_recovery_registry_visible"] is True
    assert payload["existing_update_recovery_accounted"] is True
    assert payload["replaces_update_recovery"] is False
    assert payload["migrates_update_recovery"] is False
    assert payload["duplicates_update_recovery_logic"] is False
    assert payload["registry_write_allowed"] is False
    assert payload["auto_enrollment_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["deployment_allowed"] is False
    assert payload["public_exposure_allowed"] is False
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True


def test_update_recovery_foundation_enrollment_rejects_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_update_recovery"):
        UpdateRecoveryFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("update_recovery_infra"),
            domain_enrollment=build_foundation_domain_enrollment_model("update_recovery_infra"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("update_recovery_infra"),
            existing_update_recovery_surfaces=UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES,
            update_recovery_registry_visible=True,
            existing_update_recovery_accounted=True,
            replaces_update_recovery=True,
            migrates_update_recovery=False,
            duplicates_update_recovery_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_update_recovery_foundation_enrollment_rejects_deployment() -> None:
    with pytest.raises(ValueError, match="deployment_allowed"):
        UpdateRecoveryFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("update_recovery_infra"),
            domain_enrollment=build_foundation_domain_enrollment_model("update_recovery_infra"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("update_recovery_infra"),
            existing_update_recovery_surfaces=UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES,
            update_recovery_registry_visible=True,
            existing_update_recovery_accounted=True,
            replaces_update_recovery=False,
            migrates_update_recovery=False,
            duplicates_update_recovery_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            deployment_allowed=True,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_update_recovery_foundation_enrollment_rejects_wrong_layer_binding() -> None:
    with pytest.raises(ValueError, match="layer_manifest must describe update_recovery_infra"):
        UpdateRecoveryFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("network_containerization"),
            domain_enrollment=build_foundation_domain_enrollment_model("update_recovery_infra"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("update_recovery_infra"),
            existing_update_recovery_surfaces=UPDATE_RECOVERY_FOUNDATION_EXISTING_SURFACES,
            update_recovery_registry_visible=True,
            existing_update_recovery_accounted=True,
            replaces_update_recovery=False,
            migrates_update_recovery=False,
            duplicates_update_recovery_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
