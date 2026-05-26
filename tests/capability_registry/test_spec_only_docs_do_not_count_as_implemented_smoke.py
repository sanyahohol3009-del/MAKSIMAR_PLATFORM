from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_models import (
    CapabilityTruthStatusEntry,
)


def test_spec_only_docs_do_not_count_as_implemented_smoke() -> None:
    entry = CapabilityTruthStatusEntry(
        capability_id="cap_spec_only_docs",
        truth_status="SPEC_ONLY",
        evidence_level="none",
        container_profile="not_loaded",
        runtime_enablement="disabled",
        spec_paths=("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",),
        manifest_paths=(),
        source_paths=(),
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
        reason_codes=("spec_only_docs_are_not_runtime",),
    )

    assert entry.truth_status == "SPEC_ONLY"
    assert entry.runtime_implemented is False
    assert entry.runtime_execution_verified is False
    assert entry.runtime_evidence_paths == ()
    assert entry.runtime_test_paths == ()
    assert entry.container_profile == "not_loaded"
    assert entry.containerization_ready is True


def test_spec_only_rejects_implementation_evidence_smoke() -> None:
    with pytest.raises(ValueError):
        CapabilityTruthStatusEntry(
            capability_id="cap_bad_spec_with_runtime",
            truth_status="SPEC_ONLY",
            evidence_level="none",
            container_profile="not_loaded",
            runtime_enablement="disabled",
            spec_paths=("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",),
            manifest_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",),
            source_paths=(),
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
            reason_codes=("spec_only_must_not_include_manifest",),
        )
