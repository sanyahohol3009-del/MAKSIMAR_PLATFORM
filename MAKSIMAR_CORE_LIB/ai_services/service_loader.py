from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.ai_services.service_models import (
    AIServiceDefinition,
    AIServiceLoadResult,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def collect_service_files() -> list[Path]:
    """Collect AI service config files."""
    root = PATHS.ai_services / "config"
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_service_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical service id from payload or filename."""
    service_id = payload.get("service_id")
    if isinstance(service_id, str) and service_id.strip():
        return service_id.strip()

    schema_version = payload.get("schema_version")
    if isinstance(schema_version, str) and schema_version.strip():
        return schema_version.strip().split(".v", maxsplit=1)[0]

    return file_path.name.removesuffix(".yaml")


def load_service_definition(file_path: Path) -> AIServiceLoadResult:
    """Load one AI service definition from YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return AIServiceLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read AI service file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return AIServiceLoadResult(
            definition=None,
            is_valid=False,
            error="AI service definition must contain non-empty 'schema_version'.",
        )

    service_id = _extract_service_id(payload, file_path)
    if service_id is None:
        return AIServiceLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive service_id.",
        )

    definition = AIServiceDefinition(
        service_id=service_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return AIServiceLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_service_definitions() -> list[AIServiceLoadResult]:
    """Load all AI service definitions."""
    return [load_service_definition(file_path) for file_path in collect_service_files()]
