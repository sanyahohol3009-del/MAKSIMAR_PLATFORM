from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    load_canonical_capability_registry,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_summary_builder import (
    build_capability_registry_summary,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_loader import (
    load_capability_truth_status_registry,
)


def test_phase_1_acceptance_documents_exist_smoke() -> None:
    required_paths = (
        Path("docs/architecture/open_source_integration/open_source_exclusion_registry_v1.md"),
        Path("docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json"),
        Path("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml"),
        Path("docs/architecture/open_source_integration/phase_1_open_source_canonicalization_acceptance_v1.md"),
    )

    for required_path in required_paths:
        assert required_path.exists()
        assert required_path.is_file()
        assert required_path.read_text(encoding="utf-8").strip()


def test_phase_1_acceptance_registry_read_only_container_ready_smoke() -> None:
    load_result = load_canonical_capability_registry()
    summary = build_capability_registry_summary(load_result)

    assert load_result.read_only_load is True
    assert load_result.direct_core_import_allowed is False
    assert load_result.source_of_truth_override_allowed is False
    assert load_result.runtime_mutation_allowed is False
    assert load_result.ports_opened is False
    assert load_result.containers_started is False
    assert load_result.active_deployment_created is False

    assert summary.containerization_ready_for_reference is True
    assert summary.batch_containerization_readiness_required is True
    assert summary.containerization_ready_capabilities == summary.total_capabilities
    assert summary.container_profile_declared_capabilities == summary.total_capabilities
    assert summary.runtime_enablement_declared_capabilities == summary.total_capabilities
    assert summary.ports_opened is False
    assert summary.containers_started is False
    assert summary.active_deployment_created is False


def test_phase_1_acceptance_truth_status_rejects_fake_runtime_smoke() -> None:
    result = load_capability_truth_status_registry()

    assert result.read_only_load is True
    assert result.implemented_runtime_count == 0
    assert result.non_runtime_count == result.contract.total_statuses
    assert result.runtime_false_positive_count == 0
    assert result.containerization_ready_count == result.contract.total_statuses

    assert result.ports_opened is False
    assert result.containers_started is False
    assert result.active_deployment_created is False
    assert result.runtime_mutation_allowed is False
    assert result.direct_core_import_allowed is False
    assert result.source_of_truth_override_allowed is False

    for entry in result.contract.entries:
        assert entry.truth_status != "IMPLEMENTED"
        assert entry.runtime_implemented is False
        assert entry.runtime_execution_verified is False
        assert entry.runtime_evidence_paths == ()
        assert entry.runtime_test_paths == ()
        assert entry.containerization_ready is True
        assert "manifest_or_adapter_is_not_runtime" in entry.reason_codes


def test_phase_1_acceptance_no_external_source_direct_binding_smoke() -> None:
    result = load_canonical_capability_registry()

    for entry in result.contract.entries:
        assert entry.disable_safe is True
        assert entry.dashboard_read_only is True
        assert entry.direct_core_import_allowed is False
        assert entry.source_of_truth_override_allowed is False
        assert entry.runtime_mutation_allowed is False
        assert not any(path.startswith("EXTERNAL_BACKENDS/") for path in entry.linked_surface_paths)
