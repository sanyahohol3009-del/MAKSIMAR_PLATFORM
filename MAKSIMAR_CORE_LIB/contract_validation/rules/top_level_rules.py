from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.models import ContractIssue
from MAKSIMAR_CORE_LIB.shared_services.schema_validator import (
    ValidationResult,
    validate_contract_schema,
)


def validate_top_level_structure(
    *,
    payload: dict[str, object],
    file_path: Path,
) -> list[ContractIssue]:
    """Validate top-level schema structure using shared schema validator.

    Args:
        payload: Parsed YAML payload.
        file_path: Source file path.

    Returns:
        Collected contract issues.
    """
    schema_result: ValidationResult = validate_contract_schema(
        schema=payload,
        file_path=file_path,
    )

    issues: list[ContractIssue] = []
    for issue in schema_result.issues:
        issues.append(
            ContractIssue(
                file_path=file_path,
                path=issue.path,
                level=issue.level,
                message=issue.message,
            )
        )
    return issues
