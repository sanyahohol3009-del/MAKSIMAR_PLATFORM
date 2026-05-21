from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    build_dashboard_visibility_from_enrollments,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    build_default_foundation_domain_enrollments,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    build_default_foundation_layer_manifests,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_registry_binding_contract import (
    FoundationRegistryEnrollmentReadModel,
    build_foundation_registry_enrollment_read_model,
)


def test_foundation_registry_enrollment_read_model_is_ready_and_inert() -> None:
    read_model = build_foundation_registry_enrollment_read_model()

    assert read_model.read_model_id == "foundation_registry_enrollment_read_model_v1"
    assert tuple(item.layer_id for item in read_model.layer_manifests) == FOUNDATION_LAYER_IDS
    assert tuple(item.registry_domain_id for item in read_model.domain_enrollments) == FOUNDATION_LAYER_IDS
    assert tuple(item.domain_enrollment.registry_domain_id for item in read_model.dashboard_visibility) == FOUNDATION_LAYER_IDS
    assert read_model.foundation_visibility_formalized is True
    assert read_model.existing_registry_surfaces_accounted is True
    assert read_model.replaces_existing_registry is False
    assert read_model.migrates_existing_registry is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.production_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True
    assert read_model.acceptance_ready is True


def test_foundation_registry_enrollment_rejects_registry_write() -> None:
    manifests = build_default_foundation_layer_manifests()
    enrollments = build_default_foundation_domain_enrollments()
    visibility = build_dashboard_visibility_from_enrollments(enrollments)

    with pytest.raises(ValueError, match="registry_write_allowed"):
        FoundationRegistryEnrollmentReadModel(
            read_model_id="bad",
            layer_manifests=manifests,
            domain_enrollments=enrollments,
            dashboard_visibility=visibility,
            foundation_visibility_formalized=True,
            existing_registry_surfaces_accounted=True,
            replaces_existing_registry=False,
            migrates_existing_registry=False,
            registry_write_allowed=True,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )


def test_foundation_registry_enrollment_rejects_incomplete_layer_coverage() -> None:
    manifests = build_default_foundation_layer_manifests()[1:]
    enrollments = build_default_foundation_domain_enrollments()
    visibility = build_dashboard_visibility_from_enrollments(enrollments)

    with pytest.raises(ValueError, match="layer_manifests must cover all foundation layers"):
        FoundationRegistryEnrollmentReadModel(
            read_model_id="bad",
            layer_manifests=manifests,
            domain_enrollments=enrollments,
            dashboard_visibility=visibility,
            foundation_visibility_formalized=True,
            existing_registry_surfaces_accounted=True,
            replaces_existing_registry=False,
            migrates_existing_registry=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )


def test_foundation_registry_enrollment_rejects_public_exposure() -> None:
    manifests = build_default_foundation_layer_manifests()
    enrollments = build_default_foundation_domain_enrollments()
    visibility = build_dashboard_visibility_from_enrollments(enrollments)

    with pytest.raises(ValueError, match="public_exposure_allowed"):
        FoundationRegistryEnrollmentReadModel(
            read_model_id="bad",
            layer_manifests=manifests,
            domain_enrollments=enrollments,
            dashboard_visibility=visibility,
            foundation_visibility_formalized=True,
            existing_registry_surfaces_accounted=True,
            replaces_existing_registry=False,
            migrates_existing_registry=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=True,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )
