from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.test_coverage_debt_summary_contract import (
    CoverageDebtSummaryEntry,
    build_test_coverage_debt_summary_contract,
)


def test_test_coverage_debt_summary_contract_builds() -> None:
    contract = build_test_coverage_debt_summary_contract()

    assert contract.contract_id == "test_coverage_debt_summary_contract_001"
    assert contract.total_entries == 4
    assert contract.cleanup_required_entries == 4
    assert contract.execution_path_coverage_missing_entries == 4
    assert contract.high_priority_entries == 3
    assert contract.owner_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_test_coverage_debt_summary_contract_contains_expected_modules() -> None:
    contract = build_test_coverage_debt_summary_contract()

    values = tuple(
        (entry.debt_entry_id, entry.module_path, entry.priority_level)
        for entry in contract.entries
    )

    assert values == (
        (
            "test_coverage_debt_summary_001",
            "MAKSIMAR_CORE_LIB/config_loaders/cli.py",
            "high",
        ),
        (
            "test_coverage_debt_summary_002",
            "MAKSIMAR_CORE_LIB/contract_validation/cli.py",
            "high",
        ),
        (
            "test_coverage_debt_summary_003",
            "MAKSIMAR_CORE_LIB/contract_validation/rules/*",
            "high",
        ),
        (
            "test_coverage_debt_summary_004",
            "MAKSIMAR_CORE_LIB/contract_validation/validator_core.py",
            "medium",
        ),
    )


def test_test_coverage_debt_summary_entry_rejects_missing_execution_debt_flag() -> None:
    with pytest.raises(
        ValueError,
        match="execution_path_coverage_missing must remain true for canonical coverage debt summary entries.",
    ):
        CoverageDebtSummaryEntry(
            debt_entry_id="bad_coverage_debt",
            module_path="module/path.py",
            debt_scope="bad_scope",
            cleanup_required=True,
            execution_path_coverage_missing=False,
            priority_level="high",
            owner_visible=True,
            truth_bound=True,
            description="Invalid coverage debt entry.",
        )
