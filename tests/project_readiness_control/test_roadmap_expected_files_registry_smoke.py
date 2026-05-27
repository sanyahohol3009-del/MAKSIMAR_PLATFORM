from __future__ import annotations

from tools.project_readiness_control.roadmap_expected_files_registry import (
    get_expected_batch,
    list_expected_batches,
)


def test_roadmap_expected_files_registry_smoke() -> None:
    batches = list_expected_batches()
    batch_ids = {batch.batch_id for batch in batches}

    expected_batch_ids = {
        "0.1",
        "0.2",
        "0.3",
        "0.4",
        "0.5",
        "0.6",
        "0.7",
        "0.8",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "1.5",
        "2.1",
        "2.2",
        "2.3",
        "2.4",
        "2.5",
        "2.6",
        "2.7",
        "2.8",
        "2.9",
        "2.10",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
        "3.9",
        "3.10",
        "3.11",
        "3.12",
    }

    assert batch_ids == expected_batch_ids
    assert len(batches) == 35

    titles = {batch.batch_id: batch.title for batch in batches}
    assert titles["2.1"] == "Network Backend Adapter Contract"
    assert titles["2.9"] == "Network Container Readiness"
    assert titles["2.10"] == "PHASE 2 Acceptance"

    for batch in batches:
        assert batch.expected_files


def test_phase_3_expected_files_registry_titles_smoke() -> None:
    batches = list_expected_batches()
    titles = {batch.batch_id: batch.title for batch in batches}

    assert titles["3.1"] == "Chat Core Contracts"
    assert titles["3.3"] == "Chat Command Boundary / OpenIM Adapter Contract"
    assert titles["3.12"] == "PHASE 3 Acceptance"
