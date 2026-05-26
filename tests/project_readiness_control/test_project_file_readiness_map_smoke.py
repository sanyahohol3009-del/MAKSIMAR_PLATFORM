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

    rendered = render_text(payload)
    assert "MAKSIMAR PROJECT FILE READINESS MAP" in rendered
    assert "PHASE/BATCH 0.1" in rendered
    assert "tools/project_readiness_control/scanner_discovery.py" in rendered


def test_project_file_readiness_map_all_registered_batches_smoke() -> None:
    project_root = Path(__file__).resolve().parents[2]

    reports = build_readiness_reports(project_root=project_root)
    payload = reports_to_payload(reports)

    assert payload["status"] == "READY"
    assert payload["total_batches"] == 8
    assert payload["ready_batches"] == 8
    assert payload["missing_batches"] == 0

    rendered = render_text(payload)
    assert "PHASE/BATCH 0.6" in rendered
    assert "tools/project_readiness_control/surface_inventory.py" in rendered
    assert "[OK] tools/project_readiness_control/surface_inventory.py" in rendered
