from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.models import ConfigIssue


def validate_config_shape_rules(
    *,
    payload: dict[str, object],
    file_path: Path,
) -> list[ConfigIssue]:
    """Validate minimal config document shape.

    Rules:
    - schema_version required
    - description recommended
    - rules recommended and must be list when present

    Args:
        payload: Parsed config payload.
        file_path: Config file path.

    Returns:
        Collected config issues.
    """
    issues: list[ConfigIssue] = []

    schema_version = payload.get("schema_version")
    if schema_version is None:
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="schema_version",
                level="error",
                message="Config file must declare 'schema_version'.",
            )
        )
    elif not isinstance(schema_version, str) or not schema_version.strip():
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="schema_version",
                level="error",
                message="Field 'schema_version' must be a non-empty string.",
            )
        )

    description = payload.get("description")
    if description is None:
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="description",
                level="warning",
                message="Config file should declare 'description'.",
            )
        )
    elif not isinstance(description, str) or not description.strip():
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="description",
                level="error",
                message="Field 'description' must be a non-empty string.",
            )
        )

    rules = payload.get("rules")
    if rules is None:
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="rules",
                level="warning",
                message="Config file should declare 'rules'.",
            )
        )
    elif not isinstance(rules, list):
        issues.append(
            ConfigIssue(
                file_path=file_path,
                path="rules",
                level="error",
                message="Field 'rules' must be a list when present.",
            )
        )

    return issues
