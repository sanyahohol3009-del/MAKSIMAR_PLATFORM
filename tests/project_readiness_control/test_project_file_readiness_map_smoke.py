from __future__ import annotations

from pathlib import Path

from tools.project_readiness_control.project_file_readiness_map import (
    build_readiness_reports,
    render_text,
    reports_to_payload,
)


def test_project_file_readiness_map_for_batch_0_1_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    reports = build_readiness_reports(project_root=project_root, batch_id="0.1")
    payload = reports_to_payload(reports)

    assert payload["status"] == "READY"
    assert payload["total_batches"] == 1
    assert payload["ready_batches"] == 1
    assert payload["missing_batches"] == 0

    rendered = render_text(payload)
    assert "MAKSIMAR PROJECT FILE READINESS MAP" in rendered
    assert "PHASE/BATCH 0.1" in rendered
    assert "tools/project_readiness_control/scanner_discovery.py" in rendered


def test_project_file_readiness_map_all_registered_batches_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    reports = build_readiness_reports(project_root=project_root)
    payload = reports_to_payload(reports)

    assert payload["status"] == "PARTIAL"
    assert payload["total_batches"] == 13
    assert payload["ready_batches"] == 12
    assert payload["partial_batches"] == 0
    assert payload["missing_batches"] == 1

    rendered = render_text(payload)
    assert "PHASE/BATCH 0.6" in rendered
    assert "tools/project_readiness_control/surface_inventory.py" in rendered
    assert "[OK] tools/project_readiness_control/surface_inventory.py" in rendered

    assert "PHASE/BATCH 1.1" in rendered
    assert "docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json" in rendered
    assert "[OK] docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json" in rendered

    assert "PHASE/BATCH 1.2" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py" in rendered
    assert "[OK] docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml" in rendered

    assert "PHASE/BATCH 1.3" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/capability_registry/capability_registry_loader.py" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/capability_registry/capability_registry_summary_builder.py" in rendered

    assert "PHASE/BATCH 1.4" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_models.py" in rendered
    assert "[OK] MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_loader.py" in rendered

    assert "PHASE/BATCH 1.5" in rendered
    assert "[MISSING] docs/architecture/open_source_integration/phase_1_open_source_canonicalization_acceptance_v1.md" in rendered
