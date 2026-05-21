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
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_security_enrollment_builder import (
    SECURITY_FOUNDATION_EXISTING_SURFACES,
    SecurityFoundationEnrollmentReadModel,
    build_security_foundation_enrollment_read_model,
)


def test_security_foundation_enrollment_is_registry_visible_and_read_only() -> None:
    read_model = build_security_foundation_enrollment_read_model()

    assert read_model.read_model_id == "security_foundation_enrollment_read_model_v1"
    assert read_model.layer_manifest.layer_id == "security_layer"
    assert read_model.domain_enrollment.registry_domain_id == "security_layer"
    assert read_model.dashboard_visibility.domain_enrollment.registry_domain_id == "security_layer"
    assert read_model.existing_security_surfaces == SECURITY_FOUNDATION_EXISTING_SURFACES
    assert read_model.security_registry_visible is True
    assert read_model.existing_security_layer_accounted is True
    assert read_model.replaces_security_layer is False
    assert read_model.migrates_security_layer is False
    assert read_model.duplicates_security_logic is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_security_foundation_enrollment_accounts_expected_existing_surfaces() -> None:
    read_model = build_security_foundation_enrollment_read_model()

    assert "SECURITY_LAYER/layer_manifest.yaml" in read_model.existing_security_surfaces
    assert "SECURITY_LAYER/container_contract.yaml" in read_model.existing_security_surfaces
    assert "MAKSIMAR_CORE_LIB/security_layer/security_read_model.py" in read_model.existing_security_surfaces
    assert "MAKSIMAR_SERVER/SECURITY_LAYER/security_gate.py" in read_model.existing_security_surfaces
    assert "docs/architecture/foundation/security_layer_foundation_v1.md" in read_model.existing_security_surfaces


def test_security_foundation_enrollment_to_dict_is_dashboard_safe() -> None:
    payload = build_security_foundation_enrollment_read_model().to_dict()

    assert payload["security_registry_visible"] is True
    assert payload["existing_security_layer_accounted"] is True
    assert payload["replaces_security_layer"] is False
    assert payload["migrates_security_layer"] is False
    assert payload["duplicates_security_logic"] is False
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True


def test_security_foundation_enrollment_rejects_security_layer_replacement() -> None:
    with pytest.raises(ValueError, match="replaces_security_layer"):
        SecurityFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("security_layer"),
            domain_enrollment=build_foundation_domain_enrollment_model("security_layer"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("security_layer"),
            existing_security_surfaces=SECURITY_FOUNDATION_EXISTING_SURFACES,
            security_registry_visible=True,
            existing_security_layer_accounted=True,
            replaces_security_layer=True,
            migrates_security_layer=False,
            duplicates_security_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_security_foundation_enrollment_rejects_registry_write() -> None:
    with pytest.raises(ValueError, match="registry_write_allowed"):
        SecurityFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("security_layer"),
            domain_enrollment=build_foundation_domain_enrollment_model("security_layer"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("security_layer"),
            existing_security_surfaces=SECURITY_FOUNDATION_EXISTING_SURFACES,
            security_registry_visible=True,
            existing_security_layer_accounted=True,
            replaces_security_layer=False,
            migrates_security_layer=False,
            duplicates_security_logic=False,
            registry_write_allowed=True,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_security_foundation_enrollment_rejects_wrong_layer_binding() -> None:
    with pytest.raises(ValueError, match="layer_manifest must describe security_layer"):
        SecurityFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("data_plane"),
            domain_enrollment=build_foundation_domain_enrollment_model("security_layer"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("security_layer"),
            existing_security_surfaces=SECURITY_FOUNDATION_EXISTING_SURFACES,
            security_registry_visible=True,
            existing_security_layer_accounted=True,
            replaces_security_layer=False,
            migrates_security_layer=False,
            duplicates_security_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
