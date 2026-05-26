from __future__ import annotations

from tools.project_readiness_control.roadmap_expected_files_registry import (
    get_expected_batch,
    list_expected_batches,
)


def test_roadmap_expected_files_registry_smoke() -> None:
    batches = list_expected_batches()
    batch_ids = {batch.batch_id for batch in batches}

    assert batch_ids == {"0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8"}

    batch_0_1 = get_expected_batch("0.1")
    assert batch_0_1.title == "Existing Scanner Discovery"
    assert any(
        expected.path == "tools/project_readiness_control/scanner_discovery.py"
        for expected in batch_0_1.expected_files
    )

    batch_0_6 = get_expected_batch("0.6")
    assert batch_0_6.title == "Project Readiness Sub-Runners"
    assert any(
        expected.path == "tools/project_readiness_control/surface_inventory.py"
        for expected in batch_0_6.expected_files
    )

    batch_0_8 = get_expected_batch("0.8")
    assert batch_0_8.title == "PHASE 0 Acceptance"
