from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.test_warning_cleanup_policy_contract import (
    build_test_warning_cleanup_policy_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class CoverageDebtSummaryEntry:
    debt_entry_id: str
    module_path: str
    debt_scope: str
    cleanup_required: bool
    execution_path_coverage_missing: bool
    priority_level: str
    owner_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.debt_entry_id, "debt_entry_id")
        _require_non_empty(self.module_path, "module_path")
        _require_non_empty(self.debt_scope, "debt_scope")
        _require_non_empty(self.priority_level, "priority_level")
        _require_non_empty(self.description, "description")

        if not self.cleanup_required:
            raise ValueError(
                "cleanup_required must remain true for canonical coverage debt summary entries."
            )
        if not self.execution_path_coverage_missing:
            raise ValueError(
                "execution_path_coverage_missing must remain true for canonical coverage debt summary entries."
            )
        if self.priority_level not in {"high", "medium"}:
            raise ValueError("priority_level must be either 'high' or 'medium'.")
        if not self.owner_visible:
            raise ValueError(
                "owner_visible must remain true for canonical coverage debt summary entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical coverage debt summary entries."
            )


@dataclass(frozen=True, slots=True)
class CoverageDebtSummaryContract:
    contract_id: str
    total_entries: int
    cleanup_required_entries: int
    execution_path_coverage_missing_entries: int
    high_priority_entries: int
    owner_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[CoverageDebtSummaryEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.cleanup_required_entries != sum(
            1 for entry in self.entries if entry.cleanup_required
        ):
            raise ValueError(
                "cleanup_required_entries must match cleanup_required count."
            )
        if self.execution_path_coverage_missing_entries != sum(
            1 for entry in self.entries if entry.execution_path_coverage_missing
        ):
            raise ValueError(
                "execution_path_coverage_missing_entries must match execution_path_coverage_missing count."
            )
        if self.high_priority_entries != sum(
            1 for entry in self.entries if entry.priority_level == "high"
        ):
            raise ValueError(
                "high_priority_entries must match high priority count."
            )
        if self.owner_visible_entries != sum(
            1 for entry in self.entries if entry.owner_visible
        ):
            raise ValueError(
                "owner_visible_entries must match owner_visible count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_test_coverage_debt_summary_contract() -> CoverageDebtSummaryContract:
    warning_policy = build_test_warning_cleanup_policy_contract()

    if warning_policy.cleanup_required_entries != 3:
        raise ValueError("warning policy must remain fully active before coverage debt summary.")

    entries = (
        CoverageDebtSummaryEntry(
            debt_entry_id="test_coverage_debt_summary_001",
            module_path="MAKSIMAR_CORE_LIB/config_loaders/cli.py",
            debt_scope="cli_execution_path_missing",
            cleanup_required=True,
            execution_path_coverage_missing=True,
            priority_level="high",
            owner_visible=True,
            truth_bound=True,
            description="Canonical coverage debt summary for config loader CLI execution path.",
        ),
        CoverageDebtSummaryEntry(
            debt_entry_id="test_coverage_debt_summary_002",
            module_path="MAKSIMAR_CORE_LIB/contract_validation/cli.py",
            debt_scope="cli_execution_path_missing",
            cleanup_required=True,
            execution_path_coverage_missing=True,
            priority_level="high",
            owner_visible=True,
            truth_bound=True,
            description="Canonical coverage debt summary for contract validation CLI execution path.",
        ),
        CoverageDebtSummaryEntry(
            debt_entry_id="test_coverage_debt_summary_003",
            module_path="MAKSIMAR_CORE_LIB/contract_validation/rules/*",
            debt_scope="validation_rule_execution_path_missing",
            cleanup_required=True,
            execution_path_coverage_missing=True,
            priority_level="high",
            owner_visible=True,
            truth_bound=True,
            description="Canonical coverage debt summary for contract validation rule execution paths.",
        ),
        CoverageDebtSummaryEntry(
            debt_entry_id="test_coverage_debt_summary_004",
            module_path="MAKSIMAR_CORE_LIB/contract_validation/validator_core.py",
            debt_scope="validator_core_execution_path_missing",
            cleanup_required=True,
            execution_path_coverage_missing=True,
            priority_level="medium",
            owner_visible=True,
            truth_bound=True,
            description="Canonical coverage debt summary for validator core execution path.",
        ),
    )

    return CoverageDebtSummaryContract(
        contract_id="test_coverage_debt_summary_contract_001",
        total_entries=len(entries),
        cleanup_required_entries=sum(1 for entry in entries if entry.cleanup_required),
        execution_path_coverage_missing_entries=sum(
            1 for entry in entries if entry.execution_path_coverage_missing
        ),
        high_priority_entries=sum(1 for entry in entries if entry.priority_level == "high"),
        owner_visible_entries=sum(1 for entry in entries if entry.owner_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
