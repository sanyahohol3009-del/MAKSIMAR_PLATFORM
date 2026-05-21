from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    build_foundation_dashboard_visibility_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_data_plane_enrollment_builder import (
    DATA_PLANE_FOUNDATION_EXISTING_SURFACES,
    DataPlaneFoundationEnrollmentReadModel,
    build_data_plane_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    build_foundation_layer_manifest_model,
)


def test_data_plane_foundation_enrollment_is_registry_visible_and_read_only() -> None:
    read_model = build_data_plane_foundation_enrollment_read_model()

    assert read_model.read_model_id == "data_plane_foundation_enrollment_read_model_v1"
    assert read_model.layer_manifest.layer_id == "data_plane"
    assert read_model.domain_enrollment.registry_domain_id == "data_plane"
    assert read_model.dashboard_visibility.domain_enrollment.registry_domain_id == "data_plane"
    assert read_model.existing_data_plane_surfaces == DATA_PLANE_FOUNDATION_EXISTING_SURFACES
    assert read_model.data_plane_registry_visible is True
    assert read_model.existing_data_plane_accounted is True
    assert read_model.replaces_data_plane is False
    assert read_model.migrates_data_plane is False
    assert read_model.duplicates_data_plane_logic is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_data_plane_foundation_enrollment_accounts_expected_existing_surfaces() -> None:
    read_model = build_data_plane_foundation_enrollment_read_model()

    assert "DATA_PLANE/layer_manifest.yaml" in read_model.existing_data_plane_surfaces
    assert "DATA_PLANE/container_contract.yaml" in read_model.existing_data_plane_surfaces
    assert "MAKSIMAR_CORE_LIB/data_plane/data_plane_read_model.py" in read_model.existing_data_plane_surfaces
    assert "MAKSIMAR_CORE_LIB/data_plane/append_only_log_contract.py" in read_model.existing_data_plane_surfaces
    assert "MAKSIMAR_SERVER/DATA_PLANE/data_plane_read_model_builder.py" in read_model.existing_data_plane_surfaces
    assert "docs/architecture/foundation/data_plane_foundation_v1.md" in read_model.existing_data_plane_surfaces


def test_data_plane_foundation_enrollment_to_dict_is_dashboard_safe() -> None:
    payload = build_data_plane_foundation_enrollment_read_model().to_dict()

    assert payload["data_plane_registry_visible"] is True
    assert payload["existing_data_plane_accounted"] is True
    assert payload["replaces_data_plane"] is False
    assert payload["migrates_data_plane"] is False
    assert payload["duplicates_data_plane_logic"] is False
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True


def test_data_plane_foundation_enrollment_rejects_data_plane_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_data_plane"):
        DataPlaneFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("data_plane"),
            domain_enrollment=build_foundation_domain_enrollment_model("data_plane"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("data_plane"),
            existing_data_plane_surfaces=DATA_PLANE_FOUNDATION_EXISTING_SURFACES,
            data_plane_registry_visible=True,
            existing_data_plane_accounted=True,
            replaces_data_plane=True,
            migrates_data_plane=False,
            duplicates_data_plane_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_data_plane_foundation_enrollment_rejects_runtime_mutation() -> None:
    with pytest.raises(ValueError, match="runtime_mutation_allowed"):
        DataPlaneFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("data_plane"),
            domain_enrollment=build_foundation_domain_enrollment_model("data_plane"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("data_plane"),
            existing_data_plane_surfaces=DATA_PLANE_FOUNDATION_EXISTING_SURFACES,
            data_plane_registry_visible=True,
            existing_data_plane_accounted=True,
            replaces_data_plane=False,
            migrates_data_plane=False,
            duplicates_data_plane_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=True,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_data_plane_foundation_enrollment_rejects_wrong_layer_binding() -> None:
    with pytest.raises(ValueError, match="layer_manifest must describe data_plane"):
        DataPlaneFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("security_layer"),
            domain_enrollment=build_foundation_domain_enrollment_model("data_plane"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("data_plane"),
            existing_data_plane_surfaces=DATA_PLANE_FOUNDATION_EXISTING_SURFACES,
            data_plane_registry_visible=True,
            existing_data_plane_accounted=True,
            replaces_data_plane=False,
            migrates_data_plane=False,
            duplicates_data_plane_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
