from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.errors import ConfigDiscoveryError, ConfigLoadError
from MAKSIMAR_CORE_LIB.config_loaders.models import ConfigDocument
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml


def collect_yaml_files(root: Path) -> list[Path]:
    """Collect YAML files recursively under root."""
    if not root.exists():
        raise ConfigDiscoveryError(f"Config root does not exist: {root}")

    if not root.is_dir():
        raise ConfigDiscoveryError(f"Config root is not a directory: {root}")

    files = [path for path in root.rglob("*.yaml") if path.is_file()]
    return sorted(files)


def load_config_document(file_path: Path) -> ConfigDocument:
    """Load one config YAML file."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        raise ConfigLoadError(f"Failed to load config file: {file_path}") from exc

    schema_version = payload.get("schema_version")
    return ConfigDocument(
        file_path=file_path,
        schema_version=schema_version if isinstance(schema_version, str) else None,
        payload=payload,
    )


def load_config_documents(root: Path) -> list[ConfigDocument]:
    """Load all config YAML documents under root."""
    return [load_config_document(file_path) for file_path in collect_yaml_files(root)]
