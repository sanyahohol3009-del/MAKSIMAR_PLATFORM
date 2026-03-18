from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.models import ContractIssue


def _expected_contract_name(file_path: Path) -> str:
    """Infer expected contract_name from filename."""
    return file_path.name.removesuffix(".v1.yaml")


def _expected_schema_version(file_path: Path) -> str:
    """Infer expected schema_version from filename."""
    return file_path.name.removesuffix(".yaml")


def validate_file_naming_rules(
    *,
    payload: dict[str, object],
    file_path: Path,
) -> list[ContractIssue]:
    """Validate contract_name and schema_version against filename.

    Args:
        payload: Parsed YAML payload.
        file_path: Source file path.

    Returns:
        Collected contract issues.
    """
    issues: list[ContractIssue] = []

    contract_name = payload.get("contract_name")
    expected_contract_name = _expected_contract_name(file_path)
    if isinstance(contract_name, str):
        if contract_name != expected_contract_name:
            issues.append(
                ContractIssue(
                    file_path=file_path,
                    path="contract_name",
                    level="error",
                    message=(
                        f"contract_name must match filename. "
                        f"expected='{expected_contract_name}', actual='{contract_name}'"
                    ),
                )
            )

    schema_version = payload.get("schema_version")
    expected_schema_version = _expected_schema_version(file_path)
    if isinstance(schema_version, str):
        if schema_version != expected_schema_version:
            issues.append(
                ContractIssue(
                    file_path=file_path,
                    path="schema_version",
                    level="error",
                    message=(
                        f"schema_version must match filename. "
                        f"expected='{expected_schema_version}', actual='{schema_version}'"
                    ),
                )
            )

    return issues
