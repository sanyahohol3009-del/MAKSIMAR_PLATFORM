from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.models import (
    ContractCheckResult,
    ValidationSummary,
)


def test_contract_check_result_marks_invalid_on_error() -> None:
    """ContractCheckResult should become invalid after add_error."""
    result = ContractCheckResult(file_path=Path("example.yaml"))
    assert result.is_valid is True

    result.add_error("fields.name", "Missing field")

    assert result.is_valid is False
    assert len(result.issues) == 1
    assert result.issues[0].level == "error"


def test_validation_summary_counts_results() -> None:
    """ValidationSummary should count valid and invalid results."""
    summary = ValidationSummary()

    valid_result = ContractCheckResult(file_path=Path("valid.yaml"))
    invalid_result = ContractCheckResult(file_path=Path("invalid.yaml"))
    invalid_result.add_error("required", "Broken contract")

    summary.register_result(valid_result)
    summary.register_result(invalid_result)

    assert summary.total_files == 2
    assert summary.valid_files == 1
    assert summary.invalid_files == 1
    assert summary.error_count == 1
