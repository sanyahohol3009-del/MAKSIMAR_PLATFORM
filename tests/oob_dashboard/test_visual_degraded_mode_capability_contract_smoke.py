from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_degraded_mode_capability_contract import (
    VisualDegradedModeCapabilityEntry,
    build_visual_degraded_mode_capability_contract,
)


def test_visual_degraded_mode_capability_contract_builds() -> None:
    contract = build_visual_degraded_mode_capability_contract()

    assert contract.contract_id == "visual_degraded_mode_capability_contract_001"
    assert contract.total_entries == 4
    assert contract.readable_operator_state_preserved_entries == 4
    assert contract.truth_bound_entries == 4


def test_visual_degraded_mode_capability_contract_contains_expected_ids() -> None:
    contract = build_visual_degraded_mode_capability_contract()

    values = tuple(
        (entry.degraded_entry_id, entry.backend_id, entry.degraded_mode_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_degraded_mode_capability_001",
            "visual_backend_graph_001",
            "visual_backend_graph_001_degraded_mode",
        ),
        (
            "visual_degraded_mode_capability_002",
            "visual_backend_chart_001",
            "visual_backend_chart_001_degraded_mode",
        ),
        (
            "visual_degraded_mode_capability_003",
            "visual_backend_overlay_001",
            "visual_backend_overlay_001_degraded_mode",
        ),
        (
            "visual_degraded_mode_capability_004",
            "motion_backend_virtual_001",
            "motion_backend_virtual_001_degraded_mode",
        ),
    )


def test_visual_degraded_mode_capability_entry_rejects_unreadable_operator_state() -> None:
    with pytest.raises(
        ValueError,
        match="readable_operator_state_preserved must remain true for canonical degraded capability entries.",
    ):
        VisualDegradedModeCapabilityEntry(
            degraded_entry_id="bad_degraded_entry",
            backend_id="visual_backend_graph_001",
            degraded_mode_id="bad_degraded_mode",
            reduced_graph_density=True,
            reduced_chart_density=False,
            reduced_overlay_density=False,
            reduced_motion_density=False,
            readable_operator_state_preserved=False,
            truth_bound=True,
            description="Invalid degraded capability entry.",
        )
