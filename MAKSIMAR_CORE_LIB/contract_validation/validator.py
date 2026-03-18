from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.file_loader import load_contract_documents
from MAKSIMAR_CORE_LIB.contract_validation.models import (
    ContractCheckResult,
    ContractDocument,
    ValidationSummary,
)
from MAKSIMAR_CORE_LIB.shared_services.schema_validator import validate_contract_schema


def validate_loaded_contract(document: ContractDocument) -> ContractCheckResult:
    """Validate one already loaded contract document.

    Args:
        document: Loaded contract document.

    Returns:
        Canonical contract check result.
    """
    schema_result = validate_contract_schema(
        schema=document.payload,
        file_path=document.file_path,
    )

    result = ContractCheckResult(
        file_path=document.file_path,
        contract_name=document.payload.get("contract_name")
        if isinstance(document.payload.get("contract_name"), str)
        else None,
        schema_version=document.payload.get("schema_version")
        if isinstance(document.payload.get("schema_version"), str)
        else None,
        is_valid=schema_result.is_valid,
    )

    for issue in schema_result.issues:
        if issue.level == "error":
            result.add_error(issue.path, issue.message)
        else:
            result.add_warning(issue.path, issue.message)

    return result


def validate_contract_root(root: Path) -> tuple[list[ContractCheckResult], ValidationSummary]:
    """Validate all contracts under one root directory.

    Args:
        root: Contracts root directory.

    Returns:
        Tuple of per-file results and aggregated summary.
    """
    documents = load_contract_documents(root)
    results = [validate_loaded_contract(document) for document in documents]

    summary = ValidationSummary()
    for result in results:
        summary.register_result(result)

    return results, summary
