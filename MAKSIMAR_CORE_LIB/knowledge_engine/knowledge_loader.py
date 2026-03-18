from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_models import (
    KnowledgeLoadResult,
    KnowledgeObjectDefinition,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def collect_knowledge_files() -> list[Path]:
    """Collect knowledge contract files."""
    root = PATHS.knowledge_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_object_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical knowledge object id from payload or filename."""
    object_id = payload.get("object_id")
    if isinstance(object_id, str) and object_id.strip():
        return object_id.strip()

    contract_name = payload.get("contract_name")
    if isinstance(contract_name, str) and contract_name.strip():
        return contract_name.strip()

    return file_path.name.removesuffix(".yaml")


def load_knowledge_definition(file_path: Path) -> KnowledgeLoadResult:
    """Load one knowledge definition from contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return KnowledgeLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read knowledge file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return KnowledgeLoadResult(
            definition=None,
            is_valid=False,
            error="Knowledge definition must contain non-empty 'schema_version'.",
        )

    object_id = _extract_object_id(payload, file_path)
    if object_id is None:
        return KnowledgeLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive object_id.",
        )

    definition = KnowledgeObjectDefinition(
        object_id=object_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return KnowledgeLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_knowledge_definitions() -> list[KnowledgeLoadResult]:
    """Load all knowledge definitions."""
    return [load_knowledge_definition(file_path) for file_path in collect_knowledge_files()]
