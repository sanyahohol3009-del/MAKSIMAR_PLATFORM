from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_swap_equivalence_contract import (
    VisualBackendSwapEquivalenceEntry,
    build_visual_backend_swap_equivalence_contract,
)


def test_visual_backend_swap_equivalence_contract_builds() -> None:
    contract = build_visual_backend_swap_equivalence_contract()

    assert contract.contract_id == "visual_backend_swap_equivalence_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_semantics_equal_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.swap_equivalent_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_visual_backend_swap_equivalence_contract_contains_expected_pairs() -> None:
    contract = build_visual_backend_swap_equivalence_contract()

    values = tuple(
        (
            entry.equivalence_entry_id,
            entry.primary_backend_id,
            entry.secondary_backend_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_backend_swap_equivalence_001",
            "visual_backend_graph_001",
            "visual_backend_overlay_001",
        ),
        (
            "visual_backend_swap_equivalence_002",
            "visual_backend_chart_001",
            "motion_backend_virtual_001",
        ),
        (
            "visual_backend_swap_equivalence_003",
            "visual_backend_graph_001",
            "visual_backend_chart_001",
        ),
    )


def test_visual_backend_swap_equivalence_entry_rejects_contract_change_requirement() -> None:
    with pytest.raises(
        ValueError,
        match="contract_change_required must remain false for canonical visual backend swap equivalence entries.",
    ):
        VisualBackendSwapEquivalenceEntry(
            equivalence_entry_id="bad_swap_equivalence",
            canonical_input_id="input_a",
            primary_backend_id="visual_backend_graph_001",
            secondary_backend_id="visual_backend_chart_001",
            canonical_semantics_equal=True,
            canonical_id_preserved=True,
            contract_change_required=True,
            read_model_change_required=False,
            swap_equivalent=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid swap equivalence entry.",
        )
