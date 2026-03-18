from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.memory_loader import load_memory_definition


def test_memory_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Memory loader should reject missing schema_version."""
    file_path = tmp_path / "memory_entity.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: memory_entity",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_memory_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_memory_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Memory loader should accept valid memory definition."""
    file_path = tmp_path / "memory_entity.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: memory_entity",
                "schema_version: memory_entity.v1",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_memory_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.entity_id == "memory_entity"
    assert result.definition.version == "memory_entity.v1"
