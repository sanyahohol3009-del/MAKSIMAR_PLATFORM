from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.contract_validation.errors import (
    ContractDiscoveryError,
    ContractLoadError,
)
from MAKSIMAR_CORE_LIB.contract_validation.models import ContractDocument
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml


def collect_contract_files(root: Path) -> list[Path]:
    """Collect YAML contract files recursively under root.

    Args:
        root: Root contracts directory.

    Returns:
        Sorted list of YAML files.

    Raises:
        ContractDiscoveryError: If root is missing or not a directory.
    """
    if not root.exists():
        raise ContractDiscoveryError(f"Contracts root does not exist: {root}")

    if not root.is_dir():
        raise ContractDiscoveryError(f"Contracts root is not a directory: {root}")

    files = [path for path in root.rglob("*.yaml") if path.is_file()]
    return sorted(files)


def load_contract_document(file_path: Path) -> ContractDocument:
    """Load one YAML contract file.

    Args:
        file_path: Contract YAML path.

    Returns:
        Loaded contract document.

    Raises:
        ContractLoadError: If loading fails.
    """
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        raise ContractLoadError(f"Failed to load contract file: {file_path}") from exc

    return ContractDocument(file_path=file_path, payload=payload)


def load_contract_documents(root: Path) -> list[ContractDocument]:
    """Load all contract documents under root.

    Args:
        root: Contracts root directory.

    Returns:
        Loaded contract documents.
    """
    return [load_contract_document(file_path) for file_path in collect_contract_files(root)]
