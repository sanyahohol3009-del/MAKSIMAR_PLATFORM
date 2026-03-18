from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.models import ConfigIssue


def _expected_schema_prefix(file_path: Path) -> str:
    """Infer expected schema prefix from filename stem."""
    return file_path.name.removesuffix(".yaml")


def _matches_allowed_schema_pattern(schema_version: str, expected_stem: str) -> bool:
    """Check whether schema_version matches one of the allowed naming patterns.

    Allowed patterns:
    1. exact local style:
       <expected_stem>.v1
    2. local-prefix style:
       <expected_stem>...
    3. domain-prefixed global style:
       ..._<expected_stem>.v1

    Args:
        schema_version: Declared schema version.
        expected_stem: Filename stem.

    Returns:
        True if naming is accepted.
    """
    if schema_version == f"{expected_stem}.v1":
        return True

    if schema_version.startswith(expected_stem):
        return True

    if schema_version.endswith(f"_{expected_stem}.v1"):
        return True

    return False


def validate_config_naming_rules(
    *,
    payload: dict[str, object],
    file_path: Path,
) -> list[ConfigIssue]:
    """Validate config naming conventions.

    Rules:
    - schema_version must exist
    - schema_version naming must follow one of the accepted project patterns

    Args:
        payload: Parsed config payload.
        file_path: Config file path.

    Returns:
        Collected config issues.
    """
    issues: list[ConfigIssue] = []

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str):
        return issues

    expected_stem = _expected_schema_prefix(file_path)

    if not _matches_allowed_schema_pattern(schema_version, expected_stem):
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="schema_version",
                level="warning",
                message=(
                    "schema_version does not match accepted project naming patterns. "
                    f"filename_stem='{expected_stem}', actual='{schema_version}'"
                ),
            )
        )

    return issues
