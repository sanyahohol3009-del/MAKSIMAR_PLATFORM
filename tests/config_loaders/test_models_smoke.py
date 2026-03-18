from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.models import ConfigLoadResult, ConfigLoadSummary


def test_config_load_result_marks_invalid_on_error() -> None:
    """ConfigLoadResult should become invalid after add_error."""
    result = ConfigLoadResult(file_path=Path("config.yaml"))
    assert result.is_valid is True

    result.add_error("schema_version", "Missing schema_version")

    assert result.is_valid is False
    assert len(result.issues) == 1
    assert result.issues[0].level == "error"


def test_config_load_summary_counts_results() -> None:
    """ConfigLoadSummary should count valid and invalid results."""
    summary = ConfigLoadSummary()

    valid_result = ConfigLoadResult(file_path=Path("valid.yaml"))
    invalid_result = ConfigLoadResult(file_path=Path("invalid.yaml"))
    invalid_result.add_error("schema_version", "Missing schema_version")

    summary.register_result(valid_result)
    summary.register_result(invalid_result)

    assert summary.total_files == 2
    assert summary.valid_files == 1
    assert summary.invalid_files == 1
    assert summary.error_count == 1
