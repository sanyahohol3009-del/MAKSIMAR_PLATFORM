from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_non_execution_guard_contract import (
    GraphNonExecutionGuardEntry,
    build_graph_non_execution_guard_contract,
)


def test_graph_non_execution_guard_contract_builds() -> None:
    contract = build_graph_non_execution_guard_contract()

    assert contract.contract_id == "graph_non_execution_guard_contract_001"
    assert contract.total_entries == 3
    assert contract.execution_forbidden_entries == 3
    assert contract.safe_preview_only_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_graph_non_execution_guard_contract_contains_expected_entries() -> None:
    contract = build_graph_non_execution_guard_contract()

    values = tuple(
        (
            entry.guard_entry_id,
            entry.interaction_kind,
            entry.safe_preview_only,
        )
        for entry in contract.entries
    )

    assert values == (
        ("graph_non_execution_guard_001", "graph_select", True),
        ("graph_non_execution_guard_002", "graph_zoom", True),
        ("graph_non_execution_guard_003", "graph_pan", True),
    )


def test_graph_non_execution_guard_entry_rejects_execution_opening() -> None:
    with pytest.raises(
        ValueError,
        match="execution_forbidden must remain true for canonical graph non-execution guard entries.",
    ):
        GraphNonExecutionGuardEntry(
            guard_entry_id="bad_guard",
            interaction_kind="graph_select",
            execution_forbidden=False,
            runtime_write_forbidden=True,
            control_plane_bypass_forbidden=True,
            safe_preview_only=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid graph non-execution guard entry.",
        )
