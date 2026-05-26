from __future__ import annotations

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_summary_builder import (
    CapabilityRegistrySummary,
    CapabilityRegistrySummaryBucket,
    build_capability_registry_summary,
)


def test_capability_registry_summary_builder_smoke() -> None:
    summary = build_capability_registry_summary()

    assert isinstance(summary, CapabilityRegistrySummary)
    assert summary.schema_version == "canonical_capability_registry.v1"
    assert summary.registry_id == "phase_1_canonical_capability_registry"
    assert summary.total_capabilities >= 6
    assert summary.maksimar_owned_capabilities >= 5
    assert summary.external_adapter_candidates >= 1
    assert summary.disable_safe_capabilities == summary.total_capabilities
    assert summary.dashboard_read_only_capabilities == summary.total_capabilities
    assert summary.container_profile_declared_capabilities == summary.total_capabilities
    assert summary.runtime_enablement_declared_capabilities == summary.total_capabilities
    assert summary.containerization_ready_capabilities == summary.total_capabilities
    assert summary.batch_containerization_readiness_required is True

    assert summary.read_only_load is True
    assert summary.active_deployment_created is False
    assert summary.ports_opened is False
    assert summary.containers_started is False
    assert summary.runtime_mutation_allowed is False
    assert summary.direct_core_import_allowed is False
    assert summary.source_of_truth_override_allowed is False
    assert summary.containerization_ready_for_reference is True

    container_profiles = {bucket.name for bucket in summary.container_profile_buckets}
    assert "core_library" in container_profiles
    assert "worker_service" in container_profiles
    assert "product_cube" in container_profiles
    assert "external_backend" in container_profiles


def test_capability_registry_summary_to_dict_smoke() -> None:
    summary = build_capability_registry_summary()
    payload = summary.to_dict()

    assert payload["schema_version"] == "canonical_capability_registry.v1"
    assert payload["registry_id"] == "phase_1_canonical_capability_registry"
    assert payload["total_capabilities"] == summary.total_capabilities
    assert payload["containerization_ready_for_reference"] is True
    assert payload["containerization_ready_capabilities"] == summary.total_capabilities
    assert payload["batch_containerization_readiness_required"] is True
    assert payload["ports_opened"] is False
    assert payload["containers_started"] is False
    assert payload["active_deployment_created"] is False
    assert isinstance(payload["container_profile_buckets"], list)
    assert payload["container_profile_buckets"]


def test_capability_registry_summary_bucket_validation_smoke() -> None:
    bucket = CapabilityRegistrySummaryBucket(name="external_backend", count=1)

    assert bucket.to_dict() == {"name": "external_backend", "count": 1}
