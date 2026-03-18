from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS
from MAKSIMAR_CORE_LIB.voice_layer.voice_models import (
    VoiceLoadResult,
    VoicePolicyDefinition,
)


def collect_voice_files() -> list[Path]:
    """Collect voice config files."""
    root = PATHS.voice_layer / "config"
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_policy_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical policy id from payload or filename."""
    policy_id = payload.get("policy_id")
    if isinstance(policy_id, str) and policy_id.strip():
        return policy_id.strip()

    schema_version = payload.get("schema_version")
    if isinstance(schema_version, str) and schema_version.strip():
        return schema_version.strip().split(".v", maxsplit=1)[0]

    return file_path.name.removesuffix(".yaml")


def load_voice_definition(file_path: Path) -> VoiceLoadResult:
    """Load one voice definition from YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return VoiceLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read voice file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return VoiceLoadResult(
            definition=None,
            is_valid=False,
            error="Voice definition must contain non-empty 'schema_version'.",
        )

    policy_id = _extract_policy_id(payload, file_path)
    if policy_id is None:
        return VoiceLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive policy_id.",
        )

    definition = VoicePolicyDefinition(
        policy_id=policy_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return VoiceLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_voice_definitions() -> list[VoiceLoadResult]:
    """Load all voice definitions."""
    return [load_voice_definition(file_path) for file_path in collect_voice_files()]
