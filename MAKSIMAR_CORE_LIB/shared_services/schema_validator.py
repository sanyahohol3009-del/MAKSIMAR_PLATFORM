from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import safe_read_yaml


MANDATORY_TOP_KEYS: tuple[str, ...] = (
    "contract_name",
    "schema_version",
    "description",
    "required",
    "fields",
    "validation_rules",
    "security_rules",
)


class SchemaValidationError(RuntimeError):
    """Raised when schema validation fails critically."""


@dataclass(slots=True, frozen=True)
class ValidationIssue:
    """Single validation issue."""

    path: str
    level: str
    message: str


@dataclass(slots=True)
class ValidationResult:
    """Structured validation result."""

    file_path: Path
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)

    def add_error(self, path: str, message: str) -> None:
        """Append validation error and mark result invalid."""
        self.is_valid = False
        self.issues.append(ValidationIssue(path=path, level="error", message=message))

    def add_warning(self, path: str, message: str) -> None:
        """Append validation warning."""
        self.issues.append(ValidationIssue(path=path, level="warning", message=message))


def _is_non_empty_string(value: Any) -> bool:
    """Check whether value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def _validate_required_list(result: ValidationResult, schema: dict[str, Any]) -> None:
    """Validate required field list."""
    required = schema.get("required")
    if not isinstance(required, list):
        result.add_error("required", "Field 'required' must be a list.")
        return

    for index, item in enumerate(required):
        if not _is_non_empty_string(item):
            result.add_error(f"required[{index}]", "Each required entry must be a non-empty string.")


def _validate_fields_mapping(result: ValidationResult, schema: dict[str, Any]) -> None:
    """Validate fields mapping structure."""
    fields = schema.get("fields")
    if not isinstance(fields, dict):
        result.add_error("fields", "Field 'fields' must be a mapping.")
        return

    for field_name, field_schema in fields.items():
        if not _is_non_empty_string(field_name):
            result.add_error("fields", "Field names must be non-empty strings.")
            continue

        if not isinstance(field_schema, dict):
            result.add_error(f"fields.{field_name}", "Each field definition must be a mapping.")
            continue

        field_type = field_schema.get("type")
        if field_type is None:
            result.add_warning(
                f"fields.{field_name}",
                "Field definition does not declare 'type'.",
            )
        elif not isinstance(field_type, str):
            result.add_error(
                f"fields.{field_name}.type",
                "Field 'type' must be a string.",
            )

        enum_value = field_schema.get("enum")
        if enum_value is not None and not isinstance(enum_value, list):
            result.add_error(
                f"fields.{field_name}.enum",
                "Field 'enum' must be a list when present.",
            )


def _validate_top_level_types(result: ValidationResult, schema: dict[str, Any]) -> None:
    """Validate top-level key types."""
    if not _is_non_empty_string(schema.get("contract_name")):
        result.add_error("contract_name", "Field 'contract_name' must be a non-empty string.")

    if not _is_non_empty_string(schema.get("schema_version")):
        result.add_error("schema_version", "Field 'schema_version' must be a non-empty string.")

    if not _is_non_empty_string(schema.get("description")):
        result.add_error("description", "Field 'description' must be a non-empty string.")

    validation_rules = schema.get("validation_rules")
    if not isinstance(validation_rules, list):
        result.add_error("validation_rules", "Field 'validation_rules' must be a list.")

    security_rules = schema.get("security_rules")
    if not isinstance(security_rules, list):
        result.add_error("security_rules", "Field 'security_rules' must be a list.")


def _validate_required_vs_fields(result: ValidationResult, schema: dict[str, Any]) -> None:
    """Validate required entries against fields mapping."""
    required = schema.get("required")
    fields = schema.get("fields")

    if not isinstance(required, list) or not isinstance(fields, dict):
        return

    for required_key in required:
        if isinstance(required_key, str) and required_key not in fields:
            result.add_error(
                "required",
                f"Required field '{required_key}' is missing from 'fields' mapping.",
            )


def validate_contract_schema(schema: dict[str, Any], file_path: Path) -> ValidationResult:
    """Validate one contract schema mapping.

    Args:
        schema: Parsed YAML mapping.
        file_path: Source file path.

    Returns:
        Structured validation result.
    """
    result = ValidationResult(file_path=file_path)

    for key in MANDATORY_TOP_KEYS:
        if key not in schema:
            result.add_error(key, f"Mandatory top-level key '{key}' is missing.")

    _validate_top_level_types(result, schema)
    _validate_required_list(result, schema)
    _validate_fields_mapping(result, schema)
    _validate_required_vs_fields(result, schema)

    return result


def validate_contract_file(file_path: Path) -> ValidationResult:
    """Read and validate one YAML contract file.

    Args:
        file_path: YAML contract path.

    Returns:
        Structured validation result.
    """
    schema = safe_read_yaml(file_path)
    return validate_contract_schema(schema=schema, file_path=file_path)


def collect_yaml_files(root: Path) -> list[Path]:
    """Collect YAML files recursively.

    Args:
        root: Root directory to scan.

    Returns:
        Sorted list of YAML file paths.
    """
    yaml_files = [
        path
        for path in root.rglob("*.yaml")
        if path.is_file()
    ]
    return sorted(yaml_files)


def validate_contract_tree(root: Path) -> list[ValidationResult]:
    """Validate all YAML contracts under root.

    Args:
        root: Root directory for contract scan.

    Returns:
        List of validation results for each YAML file.
    """
    results: list[ValidationResult] = []
    for file_path in collect_yaml_files(root):
        results.append(validate_contract_file(file_path))
    return results


def raise_on_invalid(results: list[ValidationResult]) -> None:
    """Raise if any validation result is invalid.

    Args:
        results: Validation results.

    Raises:
        SchemaValidationError: If one or more schemas are invalid.
    """
    invalid_results = [result for result in results if not result.is_valid]
    if not invalid_results:
        return

    lines: list[str] = ["Contract validation failed:"]
    for result in invalid_results:
        lines.append(f"- {result.file_path}")
        for issue in result.issues:
            if issue.level == "error":
                lines.append(f"    [{issue.level}] {issue.path}: {issue.message}")

    raise SchemaValidationError("\n".join(lines))
