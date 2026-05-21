from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    FoundationDomainEnrollmentModel,
    build_default_foundation_domain_enrollments,
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    build_foundation_layer_manifest_model,
)


def test_default_foundation_domain_enrollments_cover_all_layers() -> None:
    enrollments = build_default_foundation_domain_enrollments()

    assert tuple(item.registry_domain_id for item in enrollments) == FOUNDATION_LAYER_IDS
    assert all(item.existing_registry_accounted is True for item in enrollments)
    assert all(item.replaces_existing_registry is False for item in enrollments)
    assert all(item.migrates_existing_registry is False for item in enrollments)
    assert all(item.registry_write_allowed is False for item in enrollments)
    assert all(item.auto_enrollment_write_allowed is False for item in enrollments)
    assert all(item.runtime_mutation_allowed is False for item in enrollments)
    assert all(item.dashboard_safe is True for item in enrollments)
    assert all(item.read_only is True for item in enrollments)


def test_foundation_domain_enrollment_builder_accounts_existing_refs() -> None:
    enrollment = build_foundation_domain_enrollment_model("network_containerization")

    assert enrollment.enrollment_id == "network_containerization_domain_enrollment_v1"
    assert enrollment.registry_domain_id == "network_containerization"
    assert "MAKSIMAR_CORE_LIB/network_containerization" in enrollment.existing_registry_refs
    assert "NETWORK_SEGMENTATION" in enrollment.existing_registry_refs
    assert "CONTAINER_DEPLOYMENT" in enrollment.existing_registry_refs


def test_foundation_domain_enrollment_rejects_registry_replacement() -> None:
    manifest = build_foundation_layer_manifest_model("data_plane")

    with pytest.raises(ValueError, match="replaces_existing_registry"):
        FoundationDomainEnrollmentModel(
            enrollment_id="bad",
            layer_manifest=manifest,
            registry_domain_id="data_plane",
            registry_domain_title="Data Plane",
            existing_registry_refs=("MAKSIMAR_CORE_LIB/data_plane",),
            existing_registry_accounted=True,
            replaces_existing_registry=True,
            migrates_existing_registry=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_foundation_domain_enrollment_rejects_mismatched_domain() -> None:
    manifest = build_foundation_layer_manifest_model("security_layer")

    with pytest.raises(ValueError, match="registry_domain_id must match"):
        FoundationDomainEnrollmentModel(
            enrollment_id="bad",
            layer_manifest=manifest,
            registry_domain_id="data_plane",
            registry_domain_title="Data Plane",
            existing_registry_refs=("MAKSIMAR_CORE_LIB/data_plane",),
            existing_registry_accounted=True,
            replaces_existing_registry=False,
            migrates_existing_registry=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
