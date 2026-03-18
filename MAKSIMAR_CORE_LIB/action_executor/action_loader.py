from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_executor.action_models import (
    ActionDefinition,
    ActionLoadResult,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def collect_action_files() -> list[Path]:
    """Collect action contract files."""
    root = PATHS.action_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_action_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical action id from payload or filename."""
    action_id = payload.get("action_id")
    if isinstance(action_id, str) and action_id.strip():
        return action_id.strip()

    contract_name = payload.get("contract_name")
    if isinstance(contract_name, str) and contract_name.strip():
        return contract_name.strip()

    return file_path.name.removesuffix(".yaml")


def load_action_definition(file_path: Path) -> ActionLoadResult:
    """Load one action definition from action contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return ActionLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read action file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return ActionLoadResult(
            definition=None,
            is_valid=False,
            error="Action definition must contain non-empty 'schema_version'.",
        )

    action_id = _extract_action_id(payload, file_path)
    if action_id is None:
        return ActionLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive action_id.",
        )

    definition = ActionDefinition(
        action_id=action_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return ActionLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_action_definitions() -> list[ActionLoadResult]:
    """Load all action definitions."""
    return [load_action_definition(file_path) for file_path in collect_action_files()]
