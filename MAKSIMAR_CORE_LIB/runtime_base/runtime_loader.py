from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_json, safe_read_yaml
from MAKSIMAR_CORE_LIB.runtime_base.runtime_models import RuntimeDocument, RuntimeLoadResult


def _extract_runtime_name(file_path: Path) -> str:
    """Extract logical runtime document name from filename."""
    if file_path.name.endswith(".json"):
        return file_path.name.removesuffix(".json")
    if file_path.name.endswith(".yaml"):
        return file_path.name.removesuffix(".yaml")
    return file_path.stem


def _load_payload(file_path: Path) -> dict[str, object]:
    """Load one runtime payload from JSON or YAML."""
    if file_path.suffix == ".json":
        return safe_read_json(file_path)
    if file_path.suffix == ".yaml":
        return safe_read_yaml(file_path)
    raise ValueError(f"Unsupported runtime file extension: {file_path}")


def load_runtime_document(file_path: Path) -> RuntimeLoadResult:
    """Load one runtime document from file.

    Args:
        file_path: Runtime file path.

    Returns:
        Runtime load result.
    """
    try:
        payload = _load_payload(file_path)
    except (AtomicIOError, ValueError) as exc:
        return RuntimeLoadResult(
            document=None,
            is_valid=False,
            error=str(exc),
        )

    version = payload.get("schema_version")
    if not isinstance(version, str) or not version.strip():
        return RuntimeLoadResult(
            document=None,
            is_valid=False,
            error="Runtime document must contain non-empty 'schema_version'.",
        )

    document = RuntimeDocument(
        name=_extract_runtime_name(file_path),
        version=version,
        file_path=file_path,
        payload=payload,
    )

    return RuntimeLoadResult(
        document=document,
        is_valid=True,
    )


def collect_runtime_files(root: Path) -> list[Path]:
    """Collect supported runtime files under root.

    Args:
        root: Runtime root directory.

    Returns:
        Sorted list of runtime files.
    """
    if not root.exists() or not root.is_dir():
        return []

    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".json", ".yaml"}
    ]
    return sorted(files)


def load_runtime_root(root: Path) -> list[RuntimeLoadResult]:
    """Load all runtime documents under root.

    Args:
        root: Runtime root directory.

    Returns:
        Per-file runtime load results.
    """
    return [load_runtime_document(file_path) for file_path in collect_runtime_files(root)]
