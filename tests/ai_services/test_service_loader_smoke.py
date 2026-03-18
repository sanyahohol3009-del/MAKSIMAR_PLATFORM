from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.ai_services.service_loader import load_service_definition


def test_service_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """AI service loader should reject missing schema_version."""
    file_path = tmp_path / "qwen_service.yaml"
    file_path.write_text(
        "\n".join(
            [
                "service_id: qwen_service",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_service_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_service_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """AI service loader should accept valid service definition."""
    file_path = tmp_path / "qwen_service.yaml"
    file_path.write_text(
        "\n".join(
            [
                "schema_version: qwen_service.v1",
                "service_id: qwen_service",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_service_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.service_id == "qwen_service"
    assert result.definition.version == "qwen_service.v1"
