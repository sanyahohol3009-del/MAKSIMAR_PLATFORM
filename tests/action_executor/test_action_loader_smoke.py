from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.action_executor.action_loader import load_action_definition


def test_action_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Action loader should reject missing schema_version."""
    file_path = tmp_path / "action_manifest.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: action_manifest",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_action_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_action_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Action loader should accept valid action definition."""
    file_path = tmp_path / "action_manifest.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: action_manifest",
                "schema_version: action_manifest.v1",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_action_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.action_id == "action_manifest"
    assert result.definition.version == "action_manifest.v1"
