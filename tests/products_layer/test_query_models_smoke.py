from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.products_layer.product_models import ProductDefinition
from MAKSIMAR_CORE_LIB.products_layer.product_summary import build_product_summary
from MAKSIMAR_CORE_LIB.products_layer.query_models import ProductQuery


def test_build_product_summary_matches_product_ids() -> None:
    """Retrieval summary should match by product_id substring."""
    definitions = [
        ProductDefinition(
            product_id="product_manifest",
            version="product_manifest.v1",
            file_path=Path("product_manifest.v1.yaml"),
            payload={},
        ),
        ProductDefinition(
            product_id="product_profile",
            version="product_profile.v1",
            file_path=Path("product_profile.v1.yaml"),
            payload={},
        ),
    ]

    query = ProductQuery(query_text="manifest", limit=10)
    summary = build_product_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].product_id == "product_manifest"


def test_build_product_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        ProductDefinition(
            product_id="product_manifest",
            version="product_manifest.v1",
            file_path=Path("product_manifest.v1.yaml"),
            payload={},
        ),
        ProductDefinition(
            product_id="product_profile",
            version="product_profile.v1",
            file_path=Path("product_profile.v1.yaml"),
            payload={},
        ),
    ]

    query = ProductQuery(query_text="product", limit=1)
    summary = build_product_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
