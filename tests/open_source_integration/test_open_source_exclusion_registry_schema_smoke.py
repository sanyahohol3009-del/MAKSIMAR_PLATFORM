from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path(
    "docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json"
)


def test_open_source_exclusion_registry_schema_smoke() -> None:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "open_source_exclusion_registry.v1"
    assert payload["registry_id"] == "phase_1_open_source_exclusion_registry"
    assert payload["phase"] == "PHASE 1 - Open Source Canonicalization"

    default_policy = payload["default_policy"]
    assert default_policy["external_project_may_enter_immutable_core"] is False
    assert default_policy["external_project_may_be_source_of_truth"] is False
    assert default_policy["external_project_may_mutate_runtime"] is False
    assert default_policy["external_project_may_bypass_security_gate"] is False

    entries = payload["excluded_capabilities"]
    assert len(entries) >= 5

    required_ids = {
        "generic_workflow_brain",
        "generic_approval_action_model",
        "retrieval_source_of_truth",
        "proposal_codegen_governance_spine",
        "media_artifact_memory",
    }
    observed_ids = {entry["capability_id"] for entry in entries}
    assert required_ids <= observed_ids

    for entry in entries:
        assert entry["status"] == "EXCLUDED_FROM_CORE"
        assert entry["external_project_may_enter_immutable_core"] is False
        assert entry["core_dependency_required"] is False
        assert entry["allowed_core_import"] is False
        assert entry["container_profile"] in {"not_loaded", "external_backend"}
        assert entry["existing_maksimar_surfaces"]
