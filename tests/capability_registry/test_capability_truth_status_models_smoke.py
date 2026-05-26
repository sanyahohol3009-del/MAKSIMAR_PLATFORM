from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_loader import (
    build_capability_truth_status_contract,
    load_capability_truth_status_registry,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_models import (
    CapabilityTruthStatusContract,
    CapabilityTruthStatusEntry,
    make_implemented_runtime_entry,
)


def test_capability_truth_status_models_smoke() -> None:
    contract = build_capability_truth_status_contract()

    assert isinstance(contract, CapabilityTruthStatusContract)
    assert contract.schema_version == "capability_truth_status.v1"
    assert contract.registry_id == "phase_1_capability_truth_status_registry"
    assert contract.total_statuses >= 6
    assert contract.implemented_runtime_statuses == 0
    assert contract.non_runtime_statuses == contract.total_statuses
    assert contract.containerization_ready_statuses == contract.total_statuses

    statuses = {entry.truth_status for entry in contract.entries}
    assert "MANIFEST_ONLY" in statuses
    assert "ADAPTER_ONLY" in statuses
    assert "IMPLEMENTED" not in statuses

    for entry in contract.entries:
        assert entry.runtime_implemented is False
        assert entry.runtime_execution_verified is False
        assert entry.runtime_evidence_paths == ()
        assert entry.runtime_test_paths == ()
        assert entry.disable_safe is True
        assert entry.dashboard_read_only is True
        assert entry.direct_core_import_allowed is False
        assert entry.source_of_truth_override_allowed is False
        assert entry.runtime_mutation_allowed is False
        assert entry.ports_opened is False
        assert entry.containers_started is False
        assert entry.active_deployment_created is False
        assert entry.containerization_ready is True


def test_capability_truth_status_loader_smoke() -> None:
    result = load_capability_truth_status_registry()

    assert result.schema_version == "capability_truth_status_load_result.v1"
    assert result.registry_id == "phase_1_capability_truth_status_load_result"
    assert result.source_registry_id == "phase_1_canonical_capability_registry"
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


def test_implemented_runtime_requires_real_runtime_evidence_smoke() -> None:
    implemented_entry = make_implemented_runtime_entry()

    assert implemented_entry.truth_status == "IMPLEMENTED"
    assert implemented_entry.evidence_level == "runtime_verified"
    assert implemented_entry.runtime_implemented is True
    assert implemented_entry.runtime_execution_verified is True
    assert implemented_entry.source_paths
    assert implemented_entry.runtime_evidence_paths
    assert implemented_entry.runtime_test_paths

    with pytest.raises(ValueError):
        CapabilityTruthStatusEntry(
            capability_id="cap_bad_fake_implemented",
            truth_status="IMPLEMENTED",
            evidence_level="read_model_only",
            container_profile="worker_service",
            runtime_enablement="requires_operator_approval",
            spec_paths=("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",),
            manifest_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",),
            source_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_models.py",),
            adapter_paths=(),
            quarantine_policy_refs=(),
            runtime_evidence_paths=(),
            runtime_test_paths=(),
            runtime_implemented=False,
            runtime_execution_verified=False,
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            ports_opened=False,
            containers_started=False,
            active_deployment_created=False,
            containerization_ready=True,
            reason_codes=("fake_runtime_rejected",),
        )
