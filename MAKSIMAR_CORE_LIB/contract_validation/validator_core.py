from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.file_loader import load_contract_documents
from MAKSIMAR_CORE_LIB.contract_validation.models import ContractCheckResult, ContractDocument
from MAKSIMAR_CORE_LIB.contract_validation.rules import (
    apply_cross_file_rules,
    validate_field_consistency,
    validate_file_naming_rules,
    validate_top_level_structure,
)
from MAKSIMAR_CORE_LIB.contract_validation.validation_result import build_result_from_issues, build_summary


def validate_loaded_contract(document: ContractDocument) -> ContractCheckResult:
    """Validate one already loaded contract document.

    Args:
        document: Loaded contract document.

    Returns:
        Canonical per-file validation result.
    """
    payload = document.payload
    file_path = document.file_path

    issues = []
    issues.extend(validate_top_level_structure(payload=payload, file_path=file_path))
    issues.extend(validate_file_naming_rules(payload=payload, file_path=file_path))
    issues.extend(validate_field_consistency(payload=payload, file_path=file_path))

    contract_name = payload.get("contract_name") if isinstance(payload.get("contract_name"), str) else None
    schema_version = payload.get("schema_version") if isinstance(payload.get("schema_version"), str) else None

    return build_result_from_issues(
        file_path=file_path,
        contract_name=contract_name,
        schema_version=schema_version,
        issues=issues,
    )


def validate_contract_root(root: Path) -> tuple[list[ContractCheckResult], object]:
    """Validate all contracts under one root directory.

    Args:
        root: Contracts root directory.

    Returns:
        Tuple of per-file results and aggregated summary.
    """
    documents = load_contract_documents(root)
    results = [validate_loaded_contract(document) for document in documents]
    apply_cross_file_rules(results)
    summary = build_summary(results)
    return results, summary
