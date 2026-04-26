from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_capability_matrix_contract import (
    VisualCapabilityMatrixEntry,
    build_visual_capability_matrix_contract,
)


def test_visual_capability_matrix_contract_builds() -> None:
    contract = build_visual_capability_matrix_contract()

    assert contract.contract_id == "visual_capability_matrix_contract_001"
    assert contract.total_entries == 4
    assert contract.degraded_fallback_supported_entries == 4
    assert contract.swap_safe_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_visual_capability_matrix_contract_contains_expected_capabilities() -> None:
    contract = build_visual_capability_matrix_contract()

    values = tuple(
        (
            entry.capability_entry_id,
            entry.backend_id,
            entry.graph_capable,
            entry.chart_capable,
            entry.overlay_capable,
            entry.motion_capable,
        )
        for entry in contract.entries
    )

    assert values == (
        ("visual_capability_matrix_001", "visual_backend_graph_001", True, False, False, False),
        ("visual_capability_matrix_002", "visual_backend_chart_001", False, True, False, False),
        ("visual_capability_matrix_003", "visual_backend_overlay_001", False, False, True, False),
        ("visual_capability_matrix_004", "motion_backend_virtual_001", False, False, False, True),
    )


def test_visual_capability_matrix_entry_rejects_empty_capability_profile() -> None:
    with pytest.raises(
        ValueError,
        match="At least one capability flag must remain true for canonical visual capability matrix entries.",
    ):
        VisualCapabilityMatrixEntry(
            capability_entry_id="bad_capability_entry",
            backend_id="visual_backend_graph_001",
            capability_scope="bad_scope",
            graph_capable=False,
            chart_capable=False,
            overlay_capable=False,
            motion_capable=False,
            degraded_fallback_supported=True,
            swap_safe=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid capability entry.",
        )
