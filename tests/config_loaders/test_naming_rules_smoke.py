from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.rules.naming_rules import validate_config_naming_rules


def test_validate_config_naming_rules_accepts_matching_prefix() -> None:
    """Matching filename prefix should produce no issues."""
    issues = validate_config_naming_rules(
        payload={"schema_version": "memory_system_config.v1"},
        file_path=Path("memory_system.yaml"),
    )
    assert issues == []


def test_validate_config_naming_rules_warns_on_prefix_mismatch() -> None:
    """Mismatched filename prefix should produce one warning."""
    issues = validate_config_naming_rules(
        payload={"schema_version": "wrong_prefix.v1"},
        file_path=Path("memory_system.yaml"),
    )
    assert len(issues) == 1
    assert issues[0].level == "warning"
