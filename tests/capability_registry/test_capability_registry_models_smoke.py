from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.capability_registry import (
    CapabilityRegistryContract,
    CapabilityRegistryEntry,
    build_canonical_capability_registry_contract,
)


def test_capability_registry_models_smoke() -> None:
    contract = build_canonical_capability_registry_contract()

    assert isinstance(contract, CapabilityRegistryContract)
    assert contract.schema_version == "canonical_capability_registry.v1"
    assert contract.registry_id == "phase_1_canonical_capability_registry"
    assert contract.total_capabilities == len(contract.entries)
    assert contract.total_capabilities >= 6

    capability_ids = {entry.capability_id for entry in contract.entries}
    assert "cap_module_manifest_surface" in capability_ids
    assert "cap_container_boundary_surface" in capability_ids
    assert "cap_engine_runtime_surface" in capability_ids
    assert "cap_worker_runtime_surface" in capability_ids
    assert "cap_domain_cube_surface" in capability_ids
    assert "cap_external_retrieval_adapter_candidate" in capability_ids

    for entry in contract.entries:
        assert entry.disable_safe is True
        assert entry.dashboard_read_only is True
        assert entry.direct_core_import_allowed is False
        assert entry.source_of_truth_override_allowed is False
        assert entry.runtime_mutation_allowed is False
        assert entry.linked_surface_paths
        assert not any(path.startswith("EXTERNAL_BACKENDS/") for path in entry.linked_surface_paths)


def test_capability_registry_yaml_contract_smoke() -> None:
    yaml_path = Path(
        "docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml"
    )
    text = yaml_path.read_text(encoding="utf-8")

    assert "schema_version: canonical_capability_registry.v1" in text
    assert "registry_id: phase_1_canonical_capability_registry" in text
    assert "direct_core_import_allowed: false" in text
    assert "source_of_truth_override_allowed: false" in text
    assert "runtime_mutation_allowed: false" in text
    assert "ports_opened: false" in text
    assert "containers_started: false" in text
    assert "cap_module_manifest_surface" in text
    assert "cap_external_retrieval_adapter_candidate" in text


def test_capability_registry_rejects_unsafe_external_core_binding() -> None:
    with pytest.raises(ValueError):
        CapabilityRegistryEntry(
            capability_id="cap_bad_external_binding",
            title="Bad external binding",
            family="retrieval_memory",
            integration_policy="adapter_only",
            source_kind="external_backend_reference",
            owner_surface="EXTERNAL_BACKENDS/bad/source",
            linked_surface_paths=("EXTERNAL_BACKENDS/bad/source/file.py",),
            container_profile="external_backend",
            runtime_enablement="requires_operator_approval",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Bad external direct source binding.",
        )


def test_capability_registry_rejects_runtime_mutation() -> None:
    with pytest.raises(ValueError):
        CapabilityRegistryEntry(
            capability_id="cap_bad_runtime_mutation",
            title="Bad runtime mutation",
            family="worker_runtime",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/workers_registry/worker_capability_models.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/workers_registry/worker_capability_models.py",
            ),
            container_profile="worker_service",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=True,
            description="Bad runtime mutation.",
        )
