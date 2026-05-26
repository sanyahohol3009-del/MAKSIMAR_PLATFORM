from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_loader import (
    build_capability_truth_status_contract,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_models import (
    CapabilityTruthStatusEntry,
)


def test_manifest_only_status_is_not_runtime_smoke() -> None:
    contract = build_capability_truth_status_contract()

    manifest_only_entries = tuple(
        entry for entry in contract.entries if entry.truth_status == "MANIFEST_ONLY"
    )
    assert manifest_only_entries

    for entry in manifest_only_entries:
        assert entry.manifest_paths
        assert entry.runtime_implemented is False
        assert entry.runtime_execution_verified is False
        assert entry.runtime_evidence_paths == ()
        assert entry.runtime_test_paths == ()
        assert entry.containerization_ready is True


def test_manifest_only_rejects_runtime_claim_smoke() -> None:
    with pytest.raises(ValueError):
        CapabilityTruthStatusEntry(
            capability_id="cap_manifest_false_runtime",
            truth_status="MANIFEST_ONLY",
            evidence_level="read_model_only",
            container_profile="core_library",
            runtime_enablement="read_only_reference",
            spec_paths=("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",),
            manifest_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",),
            source_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",),
            adapter_paths=(),
            quarantine_policy_refs=(),
            runtime_evidence_paths=(),
            runtime_test_paths=(),
            runtime_implemented=True,
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
            reason_codes=("manifest_only_cannot_be_runtime",),
        )
