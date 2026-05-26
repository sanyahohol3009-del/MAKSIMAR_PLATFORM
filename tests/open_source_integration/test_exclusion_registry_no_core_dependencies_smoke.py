from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path(
    "docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json"
)


def test_exclusion_registry_no_core_dependencies_smoke() -> None:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    forbidden_runtime_modes = {
        "direct_core_import",
        "direct_runtime_mutation",
        "source_of_truth",
        "security_gate_bypass",
    }

    for entry in payload["excluded_capabilities"]:
        assert entry["external_project_may_enter_immutable_core"] is False
        assert entry["core_dependency_required"] is False
        assert entry["allowed_core_import"] is False
        assert entry["allowed_runtime_integration"] not in forbidden_runtime_modes

        for surface in entry["existing_maksimar_surfaces"]:
            assert not surface.startswith("EXTERNAL_BACKENDS/")
            assert "source/benchmarks" not in surface
            assert "smoke_reports" not in surface
