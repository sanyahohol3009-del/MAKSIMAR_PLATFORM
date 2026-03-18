from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.file_loader import load_config_documents
from MAKSIMAR_CORE_LIB.config_loaders.models import (
    ConfigDocument,
    ConfigLoadResult,
    ConfigLoadSummary,
)
from MAKSIMAR_CORE_LIB.config_loaders.rules import (
    validate_config_naming_rules,
    validate_config_shape_rules,
)
from MAKSIMAR_CORE_LIB.config_loaders.summary import build_summary


def validate_loaded_config(document: ConfigDocument) -> ConfigLoadResult:
    """Validate one already loaded config document.

    Args:
        document: Loaded config document.

    Returns:
        Per-file validation result.
    """
    result = ConfigLoadResult(
    file_path=document.file_path,
    schema_version=document.schema_version,
    payload=document.payload,
    is_valid=True,
)

    issues = []
    issues.extend(
        validate_config_shape_rules(
            payload=document.payload,
            file_path=document.file_path,
        )
    )
    issues.extend(
        validate_config_naming_rules(
            payload=document.payload,
            file_path=document.file_path,
        )
    )

    for issue in issues:
        if issue.level == "error":
            result.add_error(issue.path, issue.message)
        else:
            result.add_warning(issue.path, issue.message)

    return result


def load_config_root(root: Path) -> tuple[list[ConfigLoadResult], ConfigLoadSummary]:
    """Load and validate all config files under one root.

    Args:
        root: Config root directory.

    Returns:
        Tuple of per-file results and aggregated summary.
    """
    documents = load_config_documents(root)
    results = [validate_loaded_config(document) for document in documents]
    summary = build_summary(results)
    return results, summary
