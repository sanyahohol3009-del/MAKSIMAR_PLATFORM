from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.products_layer.product_models import (
    ProductDefinition,
    ProductLoadResult,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def collect_product_files() -> list[Path]:
    """Collect product contract files."""
    root = PATHS.product_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_product_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical product id from payload or filename."""
    product_id = payload.get("product_id")
    if isinstance(product_id, str) and product_id.strip():
        return product_id.strip()

    contract_name = payload.get("contract_name")
    if isinstance(contract_name, str) and contract_name.strip():
        return contract_name.strip()

    return file_path.name.removesuffix(".yaml")


def load_product_definition(file_path: Path) -> ProductLoadResult:
    """Load one product definition from contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return ProductLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read product file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return ProductLoadResult(
            definition=None,
            is_valid=False,
            error="Product definition must contain non-empty 'schema_version'.",
        )

    product_id = _extract_product_id(payload, file_path)
    if product_id is None:
        return ProductLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive product_id.",
        )

    definition = ProductDefinition(
        product_id=product_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return ProductLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_product_definitions() -> list[ProductLoadResult]:
    """Load all product definitions."""
    return [load_product_definition(file_path) for file_path in collect_product_files()]
