from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.models import (
    ContractCheckResult,
    ContractIssue,
    ValidationSummary,
)


def build_result_from_issues(
    *,
    file_path: Path,
    contract_name: str | None,
    schema_version: str | None,
    issues: list[ContractIssue],
) -> ContractCheckResult:
    """Build canonical ContractCheckResult from collected issues.

    Args:
        file_path: Source contract file path.
        contract_name: Parsed contract name if available.
        schema_version: Parsed schema version if available.
        issues: Collected issues for this contract.

    Returns:
        Canonical contract check result.
    """
    result = ContractCheckResult(
        file_path=file_path,
        contract_name=contract_name,
        schema_version=schema_version,
        is_valid=True,
    )

    for issue in issues:
        if issue.level == "error":
            result.add_error(issue.path, issue.message)
        else:
            result.add_warning(issue.path, issue.message)

    return result


def build_summary(results: list[ContractCheckResult]) -> ValidationSummary:
    """Aggregate summary from per-file validation results.

    Args:
        results: Per-file validation results.

    Returns:
        Aggregated validation summary.
    """
    summary = ValidationSummary()
    for result in results:
        summary.register_result(result)
    return summary
