from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.memory_engine.memory_models import (
    MemoryEntityDefinition,
    MemoryLoadResult,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def collect_memory_files() -> list[Path]:
    """Collect memory contract files."""
    root = PATHS.memory_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_entity_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical memory entity id from payload or filename."""
    entity_id = payload.get("entity_id")
    if isinstance(entity_id, str) and entity_id.strip():
        return entity_id.strip()

    contract_name = payload.get("contract_name")
    if isinstance(contract_name, str) and contract_name.strip():
        return contract_name.strip()

    return file_path.name.removesuffix(".yaml")


def load_memory_definition(file_path: Path) -> MemoryLoadResult:
    """Load one memory definition from memory contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return MemoryLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read memory file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return MemoryLoadResult(
            definition=None,
            is_valid=False,
            error="Memory definition must contain non-empty 'schema_version'.",
        )

    entity_id = _extract_entity_id(payload, file_path)
    if entity_id is None:
        return MemoryLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive entity_id.",
        )

    definition = MemoryEntityDefinition(
        entity_id=entity_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return MemoryLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_memory_definitions() -> list[MemoryLoadResult]:
    """Load all memory definitions."""
    return [load_memory_definition(file_path) for file_path in collect_memory_files()]
