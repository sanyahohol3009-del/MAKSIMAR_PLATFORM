from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.models import ContractIssue


def validate_field_consistency(
    *,
    payload: dict[str, object],
    file_path: Path,
) -> list[ContractIssue]:
    """Validate field-level consistency not covered by basic schema checks.

    Args:
        payload: Parsed YAML payload.
        file_path: Source file path.

    Returns:
        Collected contract issues.
    """
    issues: list[ContractIssue] = []

    fields = payload.get("fields")
    if not isinstance(fields, dict):
        return issues

    for field_name, field_schema in fields.items():
        if not isinstance(field_name, str) or not isinstance(field_schema, dict):
            continue

        description = field_schema.get("description")
        if description is None:
            issues.append(
                ContractIssue(
                    file_path=file_path,
                    path=f"fields.{field_name}.description",
                    level="warning",
                    message="Field definition should declare 'description'.",
                )
            )
        elif not isinstance(description, str) or not description.strip():
            issues.append(
                ContractIssue(
                    file_path=file_path,
                    path=f"fields.{field_name}.description",
                    level="error",
                    message="Field 'description' must be a non-empty string.",
                )
            )

    return issues
