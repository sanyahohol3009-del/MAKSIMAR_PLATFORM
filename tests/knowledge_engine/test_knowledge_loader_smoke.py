from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_loader import (
    load_knowledge_definition,
)


def test_knowledge_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Knowledge loader should reject missing schema_version."""
    file_path = tmp_path / "knowledge_object.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: knowledge_object",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_knowledge_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_knowledge_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Knowledge loader should accept valid knowledge definition."""
    file_path = tmp_path / "knowledge_object.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: knowledge_object",
                "schema_version: knowledge_object.v1",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_knowledge_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.object_id == "knowledge_object"
    assert result.definition.version == "knowledge_object.v1"
