from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.products_layer.product_loader import load_product_definition


def test_product_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Product loader should reject missing schema_version."""
    file_path = tmp_path / "product_manifest.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: product_manifest",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_product_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_product_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Product loader should accept valid product definition."""
    file_path = tmp_path / "product_manifest.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: product_manifest",
                "schema_version: product_manifest.v1",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_product_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.product_id == "product_manifest"
    assert result.definition.version == "product_manifest.v1"
